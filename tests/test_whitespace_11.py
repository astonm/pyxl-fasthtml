# coding: pyxl_fasthtml
from fasthtml.common import *
import pytest

def test():
    pytest.skip()
    # Presence of paretheses around html should not affect contents of tags. (In old pyxl_fasthtml,
    # this led to differences in whitespace handling.)
    assert to_xml(get_frag1()) == str(get_frag2())

def get_frag1():
    return <div>
        {'foo'}
    </div>

def get_frag2():
    return (<div>
        {'foo'}
    </div>)
