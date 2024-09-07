# coding: pyxl_fasthtml
from fasthtml.common import *

def test():
    title = "hi"
    x, y, z = 1, 2, 3
    assert to_xml(
        <div>
            {title}
            {x, y, z}
        </div>
    ) == "<div>\nhi\n \n1\n2\n3\n</div>\n"
