# coding: pyxl_fasthtml
from fasthtml.common import *
import pytest

def test():
    pytest.skip()
    a = (<br />)
    b = (<div>
             foo
         </div>)
    assert to_xml(b) == "<div>foo</div>"
    assert a  # pacify lint
