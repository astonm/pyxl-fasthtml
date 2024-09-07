# coding: pyxl_fasthtml
from fasthtml.common import *


def test():
    assert (
        to_xml(
            (
                <div>
                {
                    # test
                    0
                }
                </div>
            )
        )
        == "<div>0</div>\n"
    )
