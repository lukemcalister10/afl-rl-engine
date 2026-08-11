# What I found — plain summary

I opened the app in a real browser and looked at every screen, on a big screen and on a phone screen.
I took 50 pictures. I measured the colours, the text sizes and the spacing. I changed no file in your project.

**The short answer.** The app does not look like a generic AI app. It has a real look of its own.
But it is not yet finished to the standard you asked for. The look is good. The discipline is not.

**The five best things.** The numbers are handled properly: they line up in columns and use commas.
Every rise and fall shows an arrow as well as a colour, so colour is never the only signal.
When data is missing, the app says so and shows nothing rather than a made-up number.
The Movers screen is well thought out. The trade result sentence — "you give up 280, about pick 57" — is excellent.

**The worst problem: the small grey text is too faint to read.** One grey colour carries almost every
label in the app: column headings, units, footnotes, the pick and year, the AFL club name.
It is about half as strong as the accepted minimum. This one colour makes the whole app look unfinished.

**The app has no chosen font.** It asks the computer for "Arial Narrow" and takes whatever it gets.
On a Mac it looks one way, on Windows another, and on Linux or Android the narrow look is lost completely.
There are also 41 different text sizes. A designed product uses about seven.

**The player list cannot be searched or sorted.** There are 804 players and no search box.
The list is 51,000 pixels long. The column headings scroll away after eight rows.
There is only one order — most valuable first — so many fair questions cannot be asked at all.

**Three columns are empty on purpose.** The app starts with the "change since last round" setting turned on,
but that data does not exist yet. So 804 rows show a dash. One click on "bake" fills the same column
with real numbers. The app ships pointed at the empty setting.

**The trade desk cannot be cleared.** It opens with an example trade already loaded.
There is no way to delete a player or a pick, and no reset button. The bars meant to compare the two sides
do not appear at all — they are in the code but have zero width on screen.

**The player card promises an answer it does not give.** Its biggest heading says "why the price is what it is".
Under it is a note written for programmers about a missing data field. The two graphs below have no scale,
so you cannot tell what any point is worth.

**On a phone, the first player is two screens down.** The header, the version codes, the tabs and the filters
fill the whole first screen. The phone view also hides each player's position — which matters — but keeps
an empty dash that does not.

**Keyboard users are lost.** There is no visible highlight when you tab through the app.
Hovering a row barely changes it, so it does not look clickable.

**My top three fixes, in order.** One: lighten the grey label colour. Two: pick and ship one real font
and one set of text sizes. Three: add a search box and sortable columns to the player list.
The first is an afternoon. The second is a day. The third is the one that changes how the app is used.

Full detail, with pictures and measurements, is in UI_DESIGN_REVIEW.md beside this file.
