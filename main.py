#!/usr/bin/env python3
"""The Absurd Clause Contest.

One original English sentence, phrased as a clause buried deep inside a
terms-of-service agreement, written to /output/entry.txt. The gate
accepts UTF-8 text of 1 to 200 characters that is not only white space;
this program enforces the same bounds before anything touches disk.
"""

import sys
from pathlib import Path

CLAUSE = (
    "Section 14.7: The Company may, at its sole discretion, replace your "
    "password with a riddle, and accepts no liability for quests "
    "undertaken to recover it."
)

OUT_FILE = Path("/output") / "entry.txt"
MAX_LEN = 200


def acceptable(sentence):
    """True when the sentence fits the gate, False otherwise."""
    if not sentence or sentence.isspace():
        return False
    if len(sentence) > MAX_LEN:
        return False
    if "\n" in sentence or "\r" in sentence:
        return False
    try:
        sentence.encode("utf-8")
    except UnicodeEncodeError:
        return False
    return True


def deliver(sentence, destination=OUT_FILE):
    """Write the sentence to destination via a temp sibling, then verify."""
    destination.parent.mkdir(parents=True, exist_ok=True)
    pending = destination.with_name(destination.name + ".pending")
    pending.write_text(sentence, encoding="utf-8", newline="")
    pending.replace(destination)
    echoed = destination.read_text(encoding="utf-8")
    if echoed != sentence:
        raise RuntimeError("output mismatch: %r" % echoed)
    return destination


def main():
    if not acceptable(CLAUSE):
        print("clause rejected by the local gate", file=sys.stderr)
        return 1
    written = deliver(CLAUSE)
    print("clause filed (%d chars) at %s" % (len(CLAUSE), written))
    return 0


if __name__ == "__main__":
    sys.exit(main())
