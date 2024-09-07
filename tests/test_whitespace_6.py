# coding: pyxl_fasthtml
from pyxl_fasthtml import html
def test():
    assert str(<frag>
                   {'foo'}
                   <if cond="{True}">
                       {'foo'}
                   </if>
               </frag>) == "foofoo"
