import argparse
from dataclasses import dataclass
import re
import sys
import textwrap

PREFIX_RE = re.compile(r"(\s*)(#|//|///|//!|\*|-|)? ")


def get_prefix(text):
    match = PREFIX_RE.match(text)
    if match is None:
        return ""
    return match.group()


def is_blank(line):
    return all(x == " " for x in line[:-1])


@dataclass
class Region:
    text: str
    prefix: str


def split_regions(text):
    res = []
    current_prefix = None
    current_text = ""
    current_region = None
    for line in text.splitlines(keepends=False):
        prefix = get_prefix(line)
        if prefix != current_prefix:
            current_region = Region(text=line + "\n", prefix=prefix)
            res.append(current_region)
            current_prefix = prefix
        else:
            current_region.text += line + "\n"
    return res


def reformat_region(region, *, width):
    text = region.text
    prefix = region.prefix
    if is_blank(text):
        return "\n"
    lines = text.splitlines()
    prefix_length = len(prefix)
    to_wrap = "\n".join(x[prefix_length:] for x in text.splitlines())
    wrapped = textwrap.wrap(
        to_wrap, width=width - prefix_length, break_long_words=False
    )
    res = ""
    for line in wrapped:
        res += prefix + line + "\n"
    return res


def reformat(text, *, width=80):
    if text in ("", "\n"):
        return "\n"
    regions = split_regions(text)
    res = ""
    for region in regions:
        res += reformat_region(region, width=width)
    return res


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--width", default=80, type=int)
    args = parser.parse_args()
    text = sys.stdin.read()
    wrapped = reformat(text, width=args.width)
    sys.stdout.write(wrapped)
