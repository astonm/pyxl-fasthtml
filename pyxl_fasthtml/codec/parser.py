#!/usr/bin/env python

import tokenize
from pyxl_fasthtml.utils import escape
from .html_tokenizer import (
    HTMLTokenizer,
    ParseError as TokenizerParseError,
    State,
)
from .pytokenize import Untokenizer


class ParseError(Exception):
    def __init__(self, message, pos=None):
        if pos is not None:
            super(ParseError, self).__init__(
                "%s at line %d char %d" % ((message,) + pos)
            )
        else:
            super(ParseError, self).__init__(message)


class PyxlFasthtmlParser(HTMLTokenizer):
    def __init__(self, row, col, str_function):
        super(PyxlFasthtmlParser, self).__init__()
        self.start = self.end = (row, col)
        self.output = []
        self.open_tags = []
        self.remainder = None
        self.next_thing_is_python = False
        self.last_thing_was_python = False
        self.str_function = str_function

    def delete_last_comma(self):
        for i in reversed(range(len(self.output))):
            stripped = self.output[i].rstrip()
            if stripped and not stripped[0] == "#":
                assert stripped[-1] == ",", (self.output, stripped, i)
                self.output[i] = (
                    self.output[i][: len(stripped) - 1]
                    + self.output[i][len(stripped) :]
                )
                return
        assert False, "couldn't find a comma"

    def start_element(self):
        """Mark the start of an element.

        This is to allow figuring out how many children exist.
        """
        if self.open_tags:
            self.open_tags[-1]["children"] += 1

    def feed(self, token):
        ttype, tvalue, tstart, tend, tline = token

        if ttype == tokenize.OP and tvalue == "\\":
            return
        # In certain circumstances the tokenizer will emit a bunch of spaces
        # as individual error tokens. Ignore these so that spaces get collapsed
        # properly.
        if ttype == tokenize.ERRORTOKEN and tvalue == " ":
            return

        assert tstart[0] >= self.end[0], "row went backwards"
        if tstart[0] > self.end[0]:
            self.output.append("\n" * (tstart[0] - self.end[0]))

        # interpret jumps on the same line as a single space
        elif tstart[1] > self.end[1]:
            super(PyxlFasthtmlParser, self).feed(" ")

        self.end = tstart

        if ttype != tokenize.INDENT:
            while tvalue and not self.done():
                c, tvalue = tvalue[0], tvalue[1:]
                if c == "\n":
                    self.end = (self.end[0] + 1, 0)
                else:
                    self.end = (self.end[0], self.end[1] + 1)
                try:
                    super(PyxlFasthtmlParser, self).feed(c)
                except TokenizerParseError:
                    raise ParseError("HTML Parsing error", self.end)
        if self.done():
            self.remainder = (ttype, tvalue, self.end, tend, tline)
        else:
            self.end = tend

    def feed_python(self, tokens):
        ttype, tvalue, tstart, tend, tline = tokens[0]
        assert tstart[0] >= self.end[0], "row went backwards"
        if tstart[0] > self.end[0]:
            self.output.append("\n" * (tstart[0] - self.end[0]))
        ttype, tvalue, tstart, tend, tline = tokens[-1]
        self.end = tend

        if self.state in [State.DATA, State.CDATA_SECTION]:
            self.next_thing_is_python = True
            self.emit_data()
            output = Untokenizer().untokenize(tokens)
            # If we have a generator comprehension, parenthesize it
            if has_bare_generator(tokens):
                self.output.append("(%s), " % output)
            else:
                self.output.append("%s, " % output)
            self.next_thing_is_python = False
            self.last_thing_was_python = True
            self.start_element()
        elif self.state in [
            State.BEFORE_ATTRIBUTE_VALUE,
            State.ATTRIBUTE_VALUE_DOUBLE_QUOTED,
            State.ATTRIBUTE_VALUE_SINGLE_QUOTED,
            State.ATTRIBUTE_VALUE_UNQUOTED,
        ]:
            super(PyxlFasthtmlParser, self).feed_python(tokens)
        else:
            self.start_element()

    def feed_position_only(self, token):
        """update with any whitespace we might have missed, and advance position to after the
        token"""
        ttype, tvalue, tstart, tend, tline = token
        self.feed((ttype, "", tstart, tstart, tline))
        self.end = tend

    def python_comment_allowed(self):
        """Returns true if we're in a state where a # starts a comment.

        <a # comment before attribute name
           class="bar"# comment after attribute value
           href="#notacomment">
            # comment in data
            Link text
        </a>
        """
        return self.state in (
            State.DATA,
            State.TAG_NAME,
            State.BEFORE_ATTRIBUTE_NAME,
            State.AFTER_ATTRIBUTE_NAME,
            State.BEFORE_ATTRIBUTE_VALUE,
            State.AFTER_ATTRIBUTE_VALUE,
            State.COMMENT,
            State.DOCTYPE_CONTENTS,
            State.CDATA_SECTION,
        )

    def python_mode_allowed(self):
        """Returns true if we're in a state where a { starts python mode.

        <!-- {this isn't python} -->
        """
        return self.state not in (State.COMMENT,)

    def feed_comment(self, token):
        ttype, tvalue, tstart, tend, tline = token
        self.feed((ttype, "", tstart, tstart, tline))
        self.output.append(tvalue)
        self.end = tend

    def get_remainder(self):
        return self.remainder

    def done(self):
        return len(self.open_tags) == 0 and self.state == State.DATA and self.output

    def get_token(self):
        return (tokenize.STRING, "".join(self.output), self.start, self.end, "")

    @staticmethod
    def safe_attr_name(name):
        if name == "class":
            return "cls"
        return name

    def _handle_attr_value(self, attr_value):
        def format_parts():
            prev_was_python = False
            for i, part in enumerate(attr_value):
                if type(part) == list:
                    yield part
                    prev_was_python = True
                else:
                    next_is_python = bool(
                        i + 1 < len(attr_value) and type(attr_value[i + 1]) == list
                    )
                    part = self._normalize_data_whitespace(
                        part, prev_was_python, next_is_python
                    )
                    if part:
                        yield part
                    prev_was_python = False

        attr_value = list(format_parts())
        if len(attr_value) == 1:
            part = attr_value[0]
            if type(part) == list:
                self.output.append(Untokenizer().untokenize(part))
            else:
                self.output.append(repr(part))
        else:
            self.output.append('u"".join((')
            for part in attr_value:
                if type(part) == list:
                    self.output.append("{}(".format(self.str_function))
                    self.output.append(Untokenizer().untokenize(part))
                    self.output.append(")")
                else:
                    self.output.append(repr(part))
                self.output.append(", ")
            self.output.append("))")

    @staticmethod
    def _normalize_data_whitespace(data, prev_was_py, next_is_py):
        if not data:
            return ""
        if "\n" in data and not data.strip():
            if prev_was_py and next_is_py:
                return " "
            else:
                return ""
        if prev_was_py and data.startswith("\n"):
            data = " " + data.lstrip("\n")
        if next_is_py and data.endswith("\n"):
            data = data.rstrip("\n") + " "
        data = data.strip("\n")
        data = data.replace("\r", " ")
        data = data.replace("\n", " ")
        return data

    def handle_starttag(self, tag, attrs):
        self.start_element()
        self.open_tags.append(
            {"tag": tag, "row": self.end[0], "attrs": attrs, "children": 0}
        )

        module, dot, identifier = tag.rpartition(".")
        identifier = tagname_to_tagclass(identifier)
        x_tag = module + dot + identifier

        self.output.append("%s(" % x_tag)
        self.last_thing_was_python = False

    def handle_endtag(self, tag_name):

        assert self.open_tags, (
            "got </%s> but tag stack empty; parsing should be over!" % tag_name
        )

        open_tag = self.open_tags.pop()
        if open_tag["tag"] != tag_name:
            raise ParseError(
                "<%s> on line %d closed by </%s> on line %d"
                % (open_tag["tag"], open_tag["row"], tag_name, self.end[0])
            )

        first_attr = True
        for attr_name, attr_value in open_tag["attrs"].items():
            if first_attr:
                first_attr = False
            else:
                self.output.append(", ")

            self.output.append(self.safe_attr_name(attr_name))
            self.output.append("=")
            self._handle_attr_value(attr_value)

        self.output.append(")")

        if len(self.open_tags):
            self.output.append(",")
        self.last_thing_was_python = False

    def handle_startendtag(self, tag_name, attrs):
        self.handle_starttag(tag_name, attrs)
        self.handle_endtag(tag_name)

    def handle_data(self, data):
        data = self._normalize_data_whitespace(
            data, self.last_thing_was_python, self.next_thing_is_python
        )
        if not data:
            return

        self.start_element()
        self.output.append(repr(data) + ", ")
        self.last_thing_was_python = False

    def handle_comment(self, data):
        self.handle_startendtag("html_comment", {"comment": [data.strip()]})
        self.last_thing_was_python = False

    def handle_doctype(self, data):
        self.handle_startendtag("html_decl", {"decl": ["DOCTYPE " + data]})
        self.last_thing_was_python = False

    def handle_cdata(self, data):
        self.handle_startendtag("html_marked_decl", {"decl": ["CDATA[" + data]})
        self.last_thing_was_python = False


def has_bare_generator(tokens):
    nesting = 0
    for token in tokens:
        tvalue = token[1]
        if tvalue in "({[":
            nesting += 1
        if tvalue in ")}]":
            nesting -= 1
        if tvalue == "for" and nesting == 0:
            return True
    return False


def tagname_to_tagclass(tag_name):
    return tag_name.capitalize()  # TODO 9/7/2024 CamelCase instead?
