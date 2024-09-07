from pyxl_fasthtml.codec.transform import pyxl_fasthtml_transform_string, pyxl_fasthtml_invert_string

import os
import ast

dir_path = os.path.dirname(os.path.abspath(__file__))

def _roundtrip(file_name):
    path = os.path.join(dir_path, file_name)
    with open(path, "r", encoding='utf8') as f:
        contents = f.read()
        depyxl_fasthtmled = pyxl_fasthtml_transform_string(contents, invertible=True)

        # Make sure the transformed string parses
        try:
            ast.parse(depyxl_fasthtmled)
        except Exception as e:
            raise Exception("Parse error in file %s" % file_name)
        # Verify that it round trips without change
        assert contents == pyxl_fasthtml_invert_string(depyxl_fasthtmled), (
            "Could not round-trip file %s" % file_name)

# TODO: it would be better if each file was automatically a separate test case...
def test_roundtrips():
    cases = sorted(os.listdir(dir_path))
    for file_name in cases:
        if file_name.endswith('.py'):
            _roundtrip(file_name)
