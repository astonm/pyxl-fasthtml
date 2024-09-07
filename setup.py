#!/usr/bin/env python

import distutils.core
import sys

version = "1.4"

distutils.core.setup(
    name="pyxl-fasthtml",
    version=version,
    packages=[
        "pyxl_fasthtml",
        "pyxl_fasthtml.codec",
        "pyxl_fasthtml.scripts",
    ],
    url="http://github.com/astonm/pyxl-fasthtml",
    license="http://www.apache.org/licenses/LICENSE-2.0",
    description="""
        A Python 3 extension for writing structured and reusable inline HTML for FastHTML projects
    """,
)
