# coding: pyxl_fasthtml
from fasthtml.common import *
import pytest

def test():
    pytest.skip()
    assert to_xml(<span>
                   <div>Test</div>\
               </span>) == "<span><div>Test</div></span>"
