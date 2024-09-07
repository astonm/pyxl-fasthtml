# coding: pyxl_fasthtml
from fasthtml.common import *
def test():
    assert to_xml(<div>Im cool # lol
</div>) == """<div>Im cool </div>\n"""
