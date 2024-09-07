# coding: pyxl_fasthtml
from fasthtml.common import *
import pytest

def test():
    pytest.skip()
    assert to_xml(<div>
                   foo
                   {'foo'}
               </div>) == "foo foo"
