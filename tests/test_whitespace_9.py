# coding: pyxl_fasthtml
from fasthtml.common import *
import pytest

def test():
    pytest.skip()
    assert to_xml(<div class="foo
                           bar">
               </div>) == '<div class="foo bar"></div>'
