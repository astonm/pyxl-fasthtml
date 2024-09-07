# coding: pyxl_fasthtml
from fasthtml.common import *
def test():
    assert to_xml(<div>{'<img src="foo" />'}</div>) == """<div>&lt;img src=&quot;foo&quot; /&gt;</div>\n"""
