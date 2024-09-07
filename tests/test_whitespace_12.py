# coding: pyxl_fasthtml
from pyxl_fasthtml import html
def test():
    # Presence of comments should not affect contents of tags. (In old pyxl_fasthtml, this led to differences
    # in whitespace handling.)
    assert str(get_frag1()) == str(get_frag2())

def get_frag1():
    return <frag>{'foo'}
    </frag>

def get_frag2():
    return <frag>{'foo'} # lol
    </frag>
