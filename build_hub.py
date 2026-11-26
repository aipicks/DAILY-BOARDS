"""Copy the three latest boards into hub/ as the Daily Boards sections (nba.html, nfl.html, nhl.html).

The combined artifact is hub/index.html (sport switcher) plus these three pages. Each sport's daily run rebuilds its own board,
runs this script with its sport name, and republishes the hub artifact with only its own file in `files`
(files left out are kept on the artifact). Usage: python hub/build_hub.py [nba|nfl|nhl ...]   (no args = all three)
       python hub/build_hub.py --site   refresh docs/ (GitHub Pages copy for aipicks/DAILY-BOARDS) from the hub files, then commit + push docs/
"""
import pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
HUB = ROOT / "hub"
SRC = {"nba": ROOT / "nba-props-research-main/workspace/board_build/nba_prop_board.html",
       "nfl": ROOT / "nfl-board/board.html",
       "nhl": ROOT / "nhl-tim/board.html"}
HEAD = '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'


def page(sport):
    s = SRC[sport].read_text(encoding="utf-8")
    if not s.lstrip().lower().startswith("<!doctype"):          # the NBA board is written for the artifact skeleton: give it its own
        s = HEAD + "<style>body{margin:0}</style></head><body>\n" + s + "\n</body></html>"
    (HUB / f"{sport}.html").write_text(s, encoding="utf-8")
    print(f"hub/{sport}.html <- {SRC[sport].relative_to(ROOT)} ({len(s) // 1024} KB)")


def site():
    """docs/ = the GitHub Pages copy: index.html gets a full document (the artifact version relies on the artifact skeleton)."""
    d = HUB / "docs"; d.mkdir(exist_ok=True)
    idx = (HUB / "index.html").read_text(encoding="utf-8")
    head, body = idx.split('<div class="top">', 1)
    (d / "index.html").write_text(HEAD + head + '</head><body>\n<div class="top">' + body + "\n</body></html>", encoding="utf-8")
    (d / ".nojekyll").write_text("", encoding="utf-8")
    for sp in SRC:
        src = HUB / f"{sp}.html"
        if src.exists():
            (d / f"{sp}.html").write_text(src.read_text(encoding="utf-8"), encoding="utf-8")
    print("docs/ refreshed")


if __name__ == "__main__":
    if sys.argv[1:] == ["--site"]:
        site()
    else:
        for sp in (sys.argv[1:] or list(SRC)):
            page(sp)
