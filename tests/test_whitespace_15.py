# coding: pyxl_fasthtml
from pyxl_fasthtml import html
def test():
    assert str(<span>
                   <div>Test</div>\
               </span>) == "<span><div>Test</div></span>"
