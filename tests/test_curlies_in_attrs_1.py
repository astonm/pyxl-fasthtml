# coding: pyxl_fasthtml
from fasthtml.common import *
def test():
    # kannan thinks this should be different
    assert to_xml(<img src="{'foo'}" />) == """<img src="foo">\n"""
