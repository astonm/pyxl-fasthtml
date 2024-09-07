# coding: pyxl_fasthtml
from fasthtml.common import *
def test():
    assert to_xml(<div>'{'foobar'}'</div>) == """<div>\n&#x27;\nfoobar\n&#x27;\n</div>\n"""
