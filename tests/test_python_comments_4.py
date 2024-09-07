# coding: pyxl_fasthtml
from pyxl_fasthtml import html


def test():
    assert (
        str(
            (
                <div>
                {
                    # test
                    0
                }
                </div>
            )
        )
        == "<div>0</div>"
    )
