# AFL end-of-season list changes (owner-couriered, 2026-10-14)

Source: the AFL's "Retirements and delistings" pages for 2025 and 2024
(https://www.afl.com.au/news/retirements-and-delistings/2025, …/2024), transcribed verbatim on 2026-10-14 on the
owner's instruction. Categories as the page states them: `ret` retired, `del` delisted, `trd` traded, `FA` free
agent, `DFA` delisted free agent. Tarryn Thomas (North Melbourne) carried no category on the 2024 page. Owner's word (2026-10-14): he was cut at the
END OF 2023, so he is no 2024 exit; his row carries `cut_2023` (ignored by the matcher) and `_last_listed = 2023`
is set from the override below.

Overrides (owner word, applied by the matcher ahead of the pages): `tarryn-thomas` last listed 2023.

Owner rule (2026-10-14): only `ret` and `del` are list exits. An exit at the end of Y is void if the player
re-appears later (plays or is listed in a later season, or appears on a later year's list), except that a
delisting at the end of 2024 followed by a re-appearance only in 2026 would still stand (no such case is known).
The valid exits set `_last_listed = Y` on the player's store row; this is the listing fact the as-at boards read.
