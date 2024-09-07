# coding: pyxl_fasthtml
from fasthtml.common import *

def test():
    assert to_xml(<img src="barbaz{'foo'}" />) == """<img src="barbazfoo">\n"""
