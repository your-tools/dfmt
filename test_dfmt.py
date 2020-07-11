import pytest

from dfmt import reindent


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


@pytest.mark.xfail(reason="Need the 'region' feauture")
def test_pound_paragraphs():
    text = """\
    # this is a pretty big line in a Python comment that is indented
    #
    # and this is a second big line in a Python comment that is indented
"""
    expected = """\
    # this is a pretty big
    # line in a Python comment
    # that is indented
    #
    # and this is a second big
    # line in a Python comment
    # that is indented
"""
    actual = reindent(text, width=20)
    assert actual == expected, actual
