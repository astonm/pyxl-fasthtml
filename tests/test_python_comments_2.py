# coding: pyxl_fasthtml
from fasthtml.common import *
def test():
    assert to_xml(<div style="background-color: #1f75cc;"></div>) == """<div style="background-color: #1f75cc;"></div>\n"""
