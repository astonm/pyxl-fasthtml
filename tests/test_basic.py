# coding: pyxl_fasthtml
import pytest
import re
import unittest

from fasthtml.common import *

class PyxlFasthtmlTests(unittest.TestCase):
    def assertEqualHTML(self, elm, s):
        elm_s = re.sub(r"\n\s*", "", to_xml(elm))
        return self.assertEqual(elm_s, s)

    def test_basics(self):
        self.assertEqualHTML(<div />, '<div></div>')
        self.assertEqualHTML(<img src="blah" />, '<img src="blah">')
        self.assertEqualHTML(<div cls="c"></div>, '<div class="c"></div>')
        self.assertEqualHTML(<div><span></span></div>, '<div><span></span></div>')
        self.assertEqualHTML(<div><span /><span /></div>, '<div><span></span><span></span></div>')

    def test_escaping(self):
        self.assertEqualHTML(<div cls="&">{'&'}</div>, '<div class="&amp;">&amp;</div>')
        self.assertEqualHTML(<div>{NotStr('&')}</div>, '<div>&</div>')

    def test_multiline(self):
        div = (
            <div>
                text
            </div>
        )
        self.assertEqualHTML(div, '<div>text</div>')

        div2 = (
            <div attr="attr">
                text
            </div>
        )
        self.assertEqualHTML(div2, '<div attr="attr">text</div>')

    def test_python_comment(self):
        with_comment = (
            <div cls="blah">
                # comment
                text
            </div>
        )
        self.assertEqualHTML(with_comment, '<div class="blah">text</div>')

    def test_html_comment(self):
        with pytest.raises(NameError):
            comment = <!-- comment -->

    def test_cond_comment(self):
        with pytest.raises(NameError):
            cdata = <!--[if lt IE 8]>blahblah<![endif]-->

    def test_decl(self):
        with pytest.raises(NameError):
            cdata = <script><![CDATA[<div><div>]]></script>

    def test_if(self):
        with pytest.raises(NameError):
            if_tag = <if cond="{True}"></if>

    def test_if_else(self):
        with pytest.raises(NameError):
            else_tag = <else>lol</else>


if __name__ == '__main__':
    unittest.main()
