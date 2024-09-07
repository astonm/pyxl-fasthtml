# coding: pyxl_fasthtml
from pyxl_fasthtml import html
def test():
    # kannan thinks this should be different
    assert str(<frag><img src="{'foo'}" /></frag>) == """<img src="foo" />"""
