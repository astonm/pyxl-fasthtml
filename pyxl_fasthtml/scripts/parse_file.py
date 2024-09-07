#!/usr/bin/env python

import sys
from pyxl_fasthtml.codec.transform import pyxl_fasthtml_invert_string, pyxl_fasthtml_transform_string


if __name__ == '__main__':
    invert = invertible = False
    if sys.argv[1] == '-i':
        invertible = True
        fname = sys.argv[2]
    elif sys.argv[1] == '-r':
        invert = True
        fname = sys.argv[2]
    else:
        fname = sys.argv[1]
    with open(fname, 'r') as f:
        contents = f.read()
        if invert:
            print(pyxl_fasthtml_invert_string(contents), end='')
        else:
            print(pyxl_fasthtml_transform_string(contents, invertible), end='')
