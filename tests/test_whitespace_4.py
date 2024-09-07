# coding: pyxl_fasthtml
from pyxl_fasthtml import html
def test():
    assert str(<div class="{ 'foo' }">foo</div>) == '<div class="foo">foo</div>'
