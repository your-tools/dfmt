import argparse
import re
import sys
import textwrap


def get_prefix(text):
    match = re.match(r"\s*# ", text)
    if match:
        return match.group()
    match = re.match(r"(\s+)\* ", text)
    if match:
        return match.group()
    match = re.match(r"(\s+)", text)
    if match:
        return match.group()
    return ""


def reindent(text, *, width=80):
    lines = text.splitlines()
    prefix = get_prefix(lines[0])
    if any(not x.startswith(prefix.rstrip()) for x in lines):
        prefix = ""
    prefix_length = len(prefix)
    to_wrap = "\n".join(x[prefix_length:] for x in text.splitlines())
    wrapped = textwrap.wrap(to_wrap, width=width - prefix_length)
    res = ""
    for line in wrapped:
        res += prefix + line + "\n"
    return res


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--width", default=80, type=int)
    args = parser.parse_args()
    text = sys.stdin.read()
    wrapped = reindent(text, width=args.width)
    sys.stdout.write(wrapped)
