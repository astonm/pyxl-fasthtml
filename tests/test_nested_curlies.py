# coding: pyxl_fasthtml
from fasthtml.common import *
def test():
    assert to_xml(<div>{'{text}'}</div>) == """<div>{text}</div>\n"""
