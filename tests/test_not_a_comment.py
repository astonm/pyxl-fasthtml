# coding: pyxl_fasthtml
from fasthtml.common import *

# This weird circumstance could cause extra spaces to get inserted...
def a():
    return <div>
               some stuff
               $'{"#"}'
           </div>
def b():
    return (<div>
                some stuff
                $'{"#"}'
            </div>)

def test():
    assert to_xml(a()) == "<div>\nsome stuff $&#x27;\n#\n&#x27;\n</div>\n"
    assert to_xml(b()) == "<div>\nsome stuff $&#x27;\n#\n&#x27;\n</div>\n"
