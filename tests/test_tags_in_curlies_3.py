# coding: pyxl_fasthtml
from pyxl_fasthtml import html
def test():
    assert str(<frag>{'<div> foobar </div>'}</frag>) == """&lt;div&gt; foobar &lt;/div&gt;"""
