# coding: pyxl_fasthtml
from fasthtml.common import *
def test():
    assert to_xml(<div>{'<img src="{cond}" />'}</div>) == """<div>&lt;img src=&quot;{cond}&quot; /&gt;</div>\n"""
