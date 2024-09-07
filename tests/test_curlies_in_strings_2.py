# coding: pyxl_fasthtml
from fasthtml.common import *
def test():
    assert to_xml(<div>"{'foobar'}"</div>) == '''<div>\n&quot;\nfoobar\n&quot;\n</div>\n'''
