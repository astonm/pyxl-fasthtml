# coding: pyxl_fasthtml
from pyxl_fasthtml import html

def test():
    assert str(<frag><img src="barbaz{'foo'}" /></frag>) == """<img src="barbazfoo" />"""
