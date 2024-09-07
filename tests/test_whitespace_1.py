# coding: pyxl_fasthtml
from fasthtml.common import *
import pytest

def test():
    pytest.skip()
    assert to_xml(<div class="{'blah'}">
                   blah <a href="%(url)s">blah</a> blah.
               </div>) == """<div class="blah">blah <a href="%(url)s">blah</a> blah.</div>"""
