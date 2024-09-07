# coding: pyxl_fasthtml
from fasthtml.common import *
def test():
    assert to_xml(<div>{<br /> if False else <div></div>}</div>) == '''<div>\n  <div></div>\n</div>\n'''
