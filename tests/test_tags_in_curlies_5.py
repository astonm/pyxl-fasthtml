# coding: pyxl_fasthtml
from pyxl_fasthtml import html
def test():
    assert str(<frag> {'<img src="{cond}" />'} </frag>) == """ &lt;img src=&quot;{cond}&quot; /&gt; """
