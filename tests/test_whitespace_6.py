# coding: pyxl_fasthtml
from fasthtml.common import *
import pytest

def test():
    pytest.skip()
    assert to_xml(<div>
                   {'foo'}
                   <if cond="{True}">
                       {'foo'}
                   </if>
               </div>) == "foofoo"
