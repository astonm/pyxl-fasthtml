# coding: pyxl_fasthtml
from pyxl_fasthtml import html
def test():
    assert str(<frag>{<br /> if False else <div></div>}</frag>) == '''<div></div>'''
