# coding: pyxl_fasthtml
from fasthtml.common import *
import pytest

def test():
    pytest.skip()
    assert to_xml(<div id={
                        True or\
                        False } />) == '<div id="True"></div>'
