# coding: pyxl_fasthtml
from fasthtml.common import *
def test():
    assert to_xml(<div>{' "<br /> '}</div>) == '''<div> &quot;&lt;br /&gt; </div>\n'''
