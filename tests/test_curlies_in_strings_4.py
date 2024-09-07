# coding: pyxl_fasthtml
from fasthtml.common import *
def test():
    assert to_xml(<div>"</div>) + '{}' == '''<div>&quot;</div>\n{}'''
