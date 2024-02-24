"""
/*****************************************************************************/

Hey there!

This file doesn't contain any code that's relevant to the example. It's just a
helper file to make the example look better!

If you're here to see the example, you can skip this file and go to `main.py`!

/*****************************************************************************/
"""

from inspect import getframeinfo, stack
import re
from colors import color

last_linenos: dict[str, int] = {}
file_lines: dict[str, list[str]] = {}


def fprint(*args):
    global last_linenos
    global file_lines

    msg = " ".join([str(arg) for arg in args])

    caller = getframeinfo(stack()[1][0])
    lineno = caller.lineno
    filename = caller.filename

    lines = file_lines.get(filename)
    if not lines:
        lines = source_lines(filename)
        file_lines[filename] = lines

    last_lineno = last_linenos.get(filename, 0)
    lines = lines[last_lineno:lineno]
    last_linenos[filename] = lineno

    indent_str, _ = extract_indent(lines[-1])

    print(color("\n".join(lines), style="faint"))
    print(indent_str + color("┃", fg="cyan", style="faint"), end=" ")
    print(color(msg, fg="cyan", style="bold"))


def source_lines(filename: str) -> list[str]:
    def line_style(line: str):
        line = line.lstrip()
        if line.startswith("#"):
            return {"style": "faint"}
        if re.match(r"^fprint\(.*\)$", line):
            return {"fg": "cyan"}
        return {}

    def format_line(line: str, **kwargs):
        indent, line = extract_indent(line)
        return indent + color(line, **kwargs)

    lines = open(filename).read().split("\n")
    lines = [format_line(line, **line_style(line)) for line in lines]
    return lines


def extract_indent(line: str) -> tuple[str, str]:
    indent = line[: len(line) - len(line.lstrip())]
    return indent, line[len(indent) :]
