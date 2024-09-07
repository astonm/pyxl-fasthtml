# coding: pyxl_fasthtml
from fasthtml.common import *
def test():
    assert to_xml(<div>"{'"foobar"'}"</div>) == '''<div>\n&quot;\n&quot;foobar&quot;\n&quot;\n</div>\n'''
