# coding: pyxl_fasthtml
from fasthtml.common import *
def test():
    assert to_xml(<div>{'<div> foobar </div>'}</div>) == """<div>&lt;div&gt; foobar &lt;/div&gt;</div>\n"""
