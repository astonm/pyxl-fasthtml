# coding: pyxl_fasthtml
from pyxl_fasthtml import html
def test():
    assert str(<frag>{'<img src="foo" />'}</frag>) == """&lt;img src=&quot;foo&quot; /&gt;"""
