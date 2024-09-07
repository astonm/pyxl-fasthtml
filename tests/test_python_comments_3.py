# coding: pyxl_fasthtml
from fasthtml.common import *
def test():
    assert to_xml(<div #style="display: none;"
               ></div>) == "<div></div>\n"
