"""Tiny dependency-free SVG line-plot helper for the rider artifacts (no matplotlib in env).

Deterministic, self-contained. Linear axes; caller supplies series as (label, xs, ys, color, dashed).
Not a general library — just enough for per-exact-pick calibration / dispersion / uncertainty curves.
"""
def _sci(v):
    return f"{v:.6g}"

def _esc(s):
    return (str(s).replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'))

def lineplot(series, xlabel, ylabel, title, subtitle='', W=900, H=460,
             xlim=None, ylim=None, hline=None, xmarks=None, notes=None):
    pad_l, pad_r, pad_t, pad_b = 70, 200, 54, 52
    plotW, plotH = W - pad_l - pad_r, H - pad_t - pad_b
    xs_all = [x for _, xs, ys, *_ in series for x in xs]
    ys_all = [y for _, xs, ys, *_ in series for y in ys]
    if hline is not None: ys_all = ys_all + [hline]
    xmin, xmax = (xlim or (min(xs_all), max(xs_all)))
    ymin, ymax = (ylim or (min(ys_all), max(ys_all)))
    if ymax == ymin: ymax = ymin + 1
    if xmax == xmin: xmax = xmin + 1
    def X(x): return pad_l + (x - xmin) / (xmax - xmin) * plotW
    def Y(y): return pad_t + (1 - (y - ymin) / (ymax - ymin)) * plotH
    out = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" font-family="monospace" font-size="12">']
    out.append(f'<rect width="{W}" height="{H}" fill="white"/>')
    out.append(f'<text x="{pad_l}" y="22" font-size="15" font-weight="bold">{_esc(title)}</text>')
    if subtitle:
        out.append(f'<text x="{pad_l}" y="40" font-size="11" fill="#555">{_esc(subtitle)}</text>')
    # axes box
    out.append(f'<rect x="{pad_l}" y="{pad_t}" width="{plotW}" height="{plotH}" fill="none" stroke="#000"/>')
    # gridlines + y ticks (5)
    for i in range(6):
        yv = ymin + (ymax - ymin) * i / 5
        yy = Y(yv)
        out.append(f'<line x1="{pad_l}" y1="{yy:.1f}" x2="{pad_l+plotW}" y2="{yy:.1f}" stroke="#eee"/>')
        out.append(f'<text x="{pad_l-8}" y="{yy+4:.1f}" text-anchor="end" fill="#333">{_sci(yv)}</text>')
    # x ticks
    xticks = xmarks or [xmin + (xmax - xmin) * i / 5 for i in range(6)]
    for xv in xticks:
        xx = X(xv)
        out.append(f'<line x1="{xx:.1f}" y1="{pad_t}" x2="{xx:.1f}" y2="{pad_t+plotH}" stroke="#f4f4f4"/>')
        out.append(f'<text x="{xx:.1f}" y="{pad_t+plotH+16}" text-anchor="middle" fill="#333">{xv:g}</text>')
    out.append(f'<text x="{pad_l+plotW/2}" y="{H-14}" text-anchor="middle">{_esc(xlabel)}</text>')
    out.append(f'<text x="18" y="{pad_t+plotH/2}" text-anchor="middle" transform="rotate(-90 18 {pad_t+plotH/2})">{_esc(ylabel)}</text>')
    if hline is not None:
        out.append(f'<line x1="{pad_l}" y1="{Y(hline):.1f}" x2="{pad_l+plotW}" y2="{Y(hline):.1f}" stroke="#999" stroke-dasharray="4 3"/>')
    # series
    ly = pad_t + 4
    for s in series:
        label, xs, ys, color = s[0], s[1], s[2], (s[3] if len(s) > 3 else '#1f77b4')
        dashed = s[4] if len(s) > 4 else False
        pts = ' '.join(f'{X(x):.1f},{Y(y):.1f}' for x, y in zip(xs, ys))
        da = ' stroke-dasharray="5 4"' if dashed else ''
        out.append(f'<polyline points="{pts}" fill="none" stroke="{color}" stroke-width="1.8"{da}/>')
        out.append(f'<rect x="{pad_l+plotW+14}" y="{ly}" width="16" height="3" fill="{color}"/>')
        out.append(f'<text x="{pad_l+plotW+34}" y="{ly+5}" font-size="11">{_esc(label)}</text>')
        ly += 20
    if notes:
        for i, n in enumerate(notes):
            out.append(f'<text x="{pad_l+plotW+14}" y="{ly+14+i*15}" font-size="10" fill="#666">{_esc(n)}</text>')
    out.append('</svg>')
    return '\n'.join(out)
