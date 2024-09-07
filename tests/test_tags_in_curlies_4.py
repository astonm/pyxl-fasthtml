# coding: pyxl_fasthtml
from fasthtml.common import *
def test():
    assert to_xml(<div>{'<div class="foo"> foobar </div>'}</div>) == """<div>&lt;div class=&quot;foo&quot;&gt; foobar &lt;/div&gt;</div>\n"""
