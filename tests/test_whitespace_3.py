# coding: pyxl_fasthtml
from pyxl_fasthtml import html
def test():
    a = (<br />)
    b = (<div>
             foo
         </div>)
    assert str(b) == "<div>foo</div>"
    assert a  # pacify lint
