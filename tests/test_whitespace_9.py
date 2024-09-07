# coding: pyxl_fasthtml
from pyxl_fasthtml import html
def test():
    assert str(<div class="foo
                           bar">
               </div>) == '<div class="foo bar"></div>'
