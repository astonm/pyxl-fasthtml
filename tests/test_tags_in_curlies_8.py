# coding: pyxl_fasthtml
from fasthtml.common import *
def test():
    assert to_xml(<div>{<br />}</div>) == '''<div>\n  <br>\n</div>\n'''
