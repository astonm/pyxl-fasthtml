# coding: pyxl_fasthtml
from pyxl_fasthtml import html

def test():
    assert str(<frag><if cond="{True}">true</if><else>false</else></frag>) == "true"
    assert str(<frag><if cond="{False}">true</if><else>false</else></frag>) == "false"
