import json
d=[x for x in json.load(open('decomp_b.json')) if x['v0u']>0]
def A(r,f): return sum(f(x) for x in r)
print("LEG BOOK: v0 %.0f  price %.0f  F %.0f  excess %.0f"%(A(d,lambda x:x['v0']),A(d,lambda x:x['s6_price']),A(d,lambda x:x['s6_F']),A(d,lambda x:x['s6_price']-x['s6_F'])))
fl=[x for x in d if x['s6_price']-x['e1']>1.0]
print("B5 floor: %d rows lifted, total lift %.0f pts = %.2f%% of the leg book"%(len(fl),A(fl,lambda x:x['s6_price']-x['e1']),100*A(fl,lambda x:x['s6_price']-x['e1'])/A(d,lambda x:x['s6_price'])))
cp=[x for x in d if x['e1']-x['s6_price']>1.0]
print("caps cut: %d rows, total cut %.0f pts (%s)"%(len(cp),A(cp,lambda x:x['e1']-x['s6_price']),', '.join(sorted(set(x['pos'] for x in cp)))))
print("pole credit total %.0f = %.2f%% of the leg book"%(A(d,lambda x:x['y1']['pole_credit']*x['y1']['iso']),100*A(d,lambda x:x['y1']['pole_credit']*x['y1']['iso'])/A(d,lambda x:x['s6_price'])))
print()
print("=== WORKED EXAMPLES (year-1 rows) ===")
print(f"{'key':24s}{'pos':5s}{'pk':>4s}{'yr1 sa':>7s}{'g':>4s}{'v0raw':>7s}{'v0':>6s}{'R':>6s}{'band0':>7s}{'band1':>7s}{'pole':>6s}{'price':>7s}{'F':>7s}{'mkup':>6s}{'F1':>6s}{'excess':>8s}")
names=['jacob-weitering','michael-hurley','jake-lever','harris-andrews','steven-may',
       'rhys-palmer','jack-trengove','paddy-dow','stephen-coniglio',
       'toby-greene','darcy-wilson-1','justin-sherman',
       'alex-witherden','braeden-campbell','tyson-goldsack',
       'lance-franklin','travis-cloke','aaron-cadman','jarryd-roughead',
       'nicholas-naitanui','matthew-kreuzer','brodie-grundy','sean-darcy']
for k in names:
    x=[z for z in d if z['key']==k]
    if not x: continue
    x=x[0]
    print(f"{x['key']:24s}{x['pos']:5s}{x['pk']:4d}{x['sa']:7.1f}{x['gcum']:4.0f}{x['v0u']:7.0f}{x['v0']:6.0f}{x['v0']/x['v0u']:6.3f}{x['y0']['pr']*x['y0']['iso']:7.0f}{x['y1']['pr']*x['y1']['iso']:7.0f}{x['y1']['pole_credit']:6.0f}{x['s6_price']:7.0f}{x['s6_F']:7.0f}{x['s6_price']/x['v0']:6.2f}{x['s6_F']/x['s6_price']:6.2f}{x['s6_price']-x['s6_F']:8.0f}")
