#!/usr/bin/env python3
"""The Writer setup state's document (9.5 changelog D22) as the attachment of Thunderbird's `send` (D31): the same
100 sections of five 100-word paragraphs with a picture every tenth section, written as HTML with the ten pictures
inline as data URIs, so the document LibreOffice converts carries them embedded (the setup state's own HTML links
them from files beside it).

writer_doc.py <dir>    reads <dir>/pic-0.png … pic-9.png, prints the HTML
"""

import base64
import os
import sys

WORDS = ("the quick brown fox jumps over the lazy dog while the office desktop schedules its interactive work and the "
         "writer keeps typing").split()


def html(pics):
    out = ["<html><body>"]
    for page in range(100):
        out.append(f"<h2>Section {page + 1}</h2>")
        for para in range(5):
            seed = page * 5 + para
            out.append("<p>" + " ".join(WORDS[(seed * 7 + k * 13) % len(WORDS)] for k in range(100)) + ".</p>")
        if page % 10 == 0:
            out.append(f'<p><img src="data:image/png;base64,{pics[page // 10]}" width="480" height="360"></p>')
    out.append("</body></html>")
    return "\n".join(out)


def main():
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    d = sys.argv[1]
    pics = [base64.b64encode(open(os.path.join(d, f"pic-{k}.png"), "rb").read()).decode() for k in range(10)]
    print(html(pics))
    return 0


if __name__ == "__main__":
    sys.exit(main())
