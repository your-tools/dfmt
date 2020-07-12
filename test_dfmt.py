import pytest

from dfmt import reindent, split_regions


def test_empty_selection():
    assert reindent("") == "\n"


def test_empty_line():
    assert reindent("\n") == "\n"


def test_keep_small_lines():
    assert reindent("this is small", width=20) == "this is small\n"


def test_into_two_lines():
    assert reindent("aaa bbb", width=3) == "aaa\nbbb\n"


def test_into_three_lines():
    assert reindent("aaa bb ccc", width=3) == "aaa\nbb\nccc\n"


def test_long_sentence():
    assert (
        reindent("this is a pretty big sentence in two pretty big parts", width=12)
        == "this is a\npretty big\nsentence in\ntwo pretty\nbig parts\n"
    )


def test_pound_comment_1_to_2():
    assert (
        reindent("# this is a pretty big comment, isn't it?", width=20)
        == "# this is a pretty\n# big comment, isn't\n# it?\n"
    )


def test_pound_comment_2_to_3():
    text = """\
# aaa bbb
# ccc
"""
    expected = """\
# aaa
# bbb
# ccc
"""
    assert reindent(text, width=5) == expected


def test_doxygen():
    text = """\
 * this is a pretty big line in a doxygen comment
"""
    expected = """\
 * this is a pretty
 * big line in a
 * doxygen comment
"""
    assert reindent(text, width=20) == expected


def test_preserve_leading_indent():
    text = " aaa bbb"
    assert reindent(text, width=4) == " aaa\n bbb\n"


def test_indented_pound_comment():
    text = """\
    # this is a pretty big line in a Python comment that is indented
"""
    expected = """\
    # this is a
    # pretty big
    # line in a
    # Python comment
    # that is
    # indented
"""
    assert reindent(text, width=20) == expected


def test_pound_paragraphs():
    text = """\
    # this is a pretty big line in a Python comment that is indented
    #
    # and this is a second big line in a Python comment that is indented
"""
    expected = """\
    # this is a
    # pretty big
    # line in a
    # Python comment
    # that is
    # indented
    #
    # and this is a
    # second big
    # line in a
    # Python comment
    # that is
    # indented
"""
    actual = reindent(text, width=20)
    assert actual == expected, actual


class TestRegions:
    @staticmethod
    def test_one_line():
        text = "hello"
        regions = split_regions(text)
        assert len(regions) == 1
        actual = regions[0]
        assert actual.prefix == ""
        assert actual.text == "hello\n"

    @staticmethod
    def test_two_lines():
        text = "hello\nworld"
        regions = split_regions(text)
        assert len(regions) == 1
        actual = regions[0]
        assert actual.prefix == ""
        assert actual.text == "hello\nworld\n"

    @staticmethod
    def test_one_indented_paragraph():
        text = """\
  hello
  world
"""
        regions = split_regions(text)
        assert len(regions) == 1
        actual = regions[0]
        assert actual.prefix == "  "
        assert actual.text == "  hello\n  world\n"

    @staticmethod
    def test_two_indented_paragraphs():
        text = """\
  hello
  world

  goodbye
  world
"""
        regions = split_regions(text)
        one, two, three = regions
        assert two.prefix == ""
        assert two.text == "\n"

    @staticmethod
    def test_two_paragraphs_in_pound_comment():
        text = """\
  # this is the
  # first paragraph
  #
  # this is the
  # second paragraph
"""
        regions = split_regions(text)
        one, two, three = regions
        assert two.prefix == "  "
        assert two.text == "  #\n"
