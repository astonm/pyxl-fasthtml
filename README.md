# pyxl-fasthtml

This is a [fork](https://github.com/astonm/pyxl-fasthtml) of a [port](https://github.com/gvanrossum/pyxl3) of a [fork](https://github.com/dropbox/pyxl) of [Pyxl](https://github.com/awable/pyxl), an early implementation of the pattern made popular now by React, allowing the use of HTML-like markup inside of a Python file. Pyxl was itself inspired by the [XHP](https://github.com/facebook/xhp/wiki) project at Facebook.

With the appearance of [FastHTML](https://docs.fastht.ml/) there's a newfound reason to want this sort of capability. The built-in component library
is a powerful abstraction for generating HTML, but nothing quite matches the real thing. Rather than writing

```py
from fasthtml.common import *

app,rt = fast_app()

@rt('/')
def get(): return Div(P('Hello World!'))

serve()
```

With this library, you can write

```py
# coding: pyxl-fasthtml
from fasthtml.common import *

app,rt = fast_app()

@rt('/')
def get(): return <div><p>Hello World!</p></div>

serve()
```

## Installation

Clone the repo and run the following commands from the directory you cloned to.  (Sudo not needed if you use a virtualenv.)

```sh
sudo python3 -m pip install .
sudo python3 finish_install.py
```

To confirm that pyxl-fasthtml was correctly installed, run the following command from the same directory:

```sh
python3 pyxl_fasthtml/examples/hello_world.py
```

You should see the output
```html
<html>
  <body>Hello World!</body>
</html>
```
printed out. Thats it! You're ready to use pyxl-fasthtml.

## Running the tests

```sh
python3 -m pip install pytest python-fasthtml
python3 -m pytest
```

Note: This test suite is borrowed from [gvanrossum/pyxl3](https://github.com/gvanrossum/pyxl3) with some tactical deletions for features that are no longer supported (e.g. if/else tags, or specific promises about whitespace output).

## How it works

pyxl-fasthtml converts HTML tags into Python object syntax before the file is run through the interpreter, so the code that actually runs is regular Python. For example, the `hello_world.py` example above is converted into:

```py
print(to_xml(Html(Body("Hello World!"))))
```

pyxl-fasthtml's usefulness comes from being able to write HTML rather than unwieldy object instantiations and function calls. Note that pyxl-fasthtml relies on [FastHTML's components](https://docs.fastht.ml/api/components.html), so it's easiest to start your file with `from fasthtml.common import *` (as is convention).

The conversion to Python is relatively straightforward: Opening tags are converted into object instantiations for the respective tag, nested tags and text content are passed in as positional arguments to that method call, and any tag attributes are passed as keyword arguments. To learn more about how pyxl-fasthtml does this, see the **Implementation Details** section below.

## Documentation

All Python files with inline HTML must have the following first line:

```py
# coding: pyxl-fasthtml
```

With that, you can start using HTML in your Python file.

### Inline Python Expressions

Within markup, anything wrapped with `{` and `}`'s is evaluated as a Python expression. Please note that attribute values must be wrapped inside quotes, regardless of whether it contains a Python expression or not. When used in attribute values, the Python expression must evaluate to something that can be cast to `str`. When used inside a tag, the expression can evaluate to anything that can be cast to `str`, an HTML tag, or a list containing those two types. This is demonstrated in the example below:

```py
image_name = "bolton.png"
image = <img src="/static/images/{image_name}" />

text = "Michael Bolton"
block = <div>{image}{text}</div>

element_list = [image, text]
block2 = <div>{element_list}</div>
```
### Escaping

pyxl-fasthtml does no special work to escape any data within your markup. However, the `FastHTML` library does automatically escape everything, meaning your markup is XSS safe by default.

## Implementation Details

### Parsing

pyxl-fasthtml uses support for specifying source code encodings as described in [PEP 263](http://www.python.org/dev/peps/pep-0263/) to do what it does. The functionality was originally provided so that Python developers could write code in non-ASCII languages (eg. Chinese variable names). pyxl-fasthtml creates a custom encoding called `pyxl-fasthtml` which allows it to convert XML into regular Python before the file is compiled. Once the `pyxl-fasthtml` codec is registered, any file starting with `# coding: pyxl-fasthtml` is run through the pyxl-fasthtml parser before compilation.

To register the `pyxl-fasthtml` codec, one must import the [`pyxl_fasthtml.codec.register`](https://github.com/astonm/pyxl-fasthtml/blob/master/pyxl_fasthtml/codec/register.py) module. The **Installation Process** makes it so that this always happens at Python startup via the final `python3 finish_install.py` step. What this step is doing is adding a file called `pyxl_fasthtml.pth` in your Python `site-packages` directory, which imports the `pyxl.codec.register` module. Anything with a `.pth` extension in the site-packages directory is run automatically at Python startup. Read more about that [here](http://docs.python.org/library/site.html).

Some people may prefer avoiding adding `pyxl_fasthtml.pth` to their `site-packages` directory, in which case they should skip the final step of the installation process and explicitly import `pyxl.codec.register` in the entry point of their application.

The `pyxl-fasthtml` encoding is a wrapper around `utf-8`, but every time it encounters a blob of HTML in the file, it runs it through Python's [`HTMLParser`](http://docs.python.org/library/htmlparser.html) and replaces the HTML with Python objects. As explained above, opening tags are converted into object instantiations for the respective tag, nested tags are passed as positional arguments, and attributes are keyword arguments. The code for these conversions can be seen [here](https://github.com/astonm/pyxl-fasthtml/blob/master/pyxl_fasthtml/codec/parser.py).

## Editor Support

### Emacs (untested)

Grab pyxl-mode.el from the cloned repository under `emacs/pyxl-mode.el` or copy it from [here](https://github.com/astonm/pyxl-fasthtml/blob/master/emacs/pyxl-mode.el). To install, drop the file anywhere on your load path, and add the following to your ~/.emacs file (GNU Emacs) or ~/.xemacs/init.el file (XEmacs):

```py
(autoload 'pyxl-mode "pyxl-mode" "Major mode for editing pyxl" t)
(setq auto-mode-alist
     (cons '("\\.py\\'" . pyxl-mode) auto-mode-alist))
```

### Vim (untested)

Pyxl detection, syntax, and indent files are in the `vim` directory. The easiest way to install the vim support is via [pathogen](https://github.com/tpope/vim-pathogen); with pathogen, you can simply link or copy the directory into your bundle directory. Without pathogen, place the various files in the corresponding subdirectories of your .vim directory.

### Pycharm (untested)

See [pycharm-pyxl](https://github.com/christoffer/pycharm-pyxl).

### Sublime Text (untested)

See [sublime-pyxl](https://github.com/yyjhao/sublime-pyxl).

## Related Projects

- [pyxl](https://github.com/awable/pyxl) (Cove): The original Pyxl implementation, for Python 2 (unmaintained)
- [pyxl](https://github.com/dropbox/pyxl) (Dropbox): An updated version of Pyxl used at Dropbox, for Python 2 (unmaintained)
- [pyxl3](https://github.com/gvanrossum/pyxl3): A Python 3 port of Pyxl used at Dropbox (unmaintained)
- [pyxl4](https://github.com/pyxl4/pyxl4): A fork of `pyxl3` that supports both Python 2 and 3, and also is hosted on PyPI for easy installation
- [mixt](https://github.com/twidi/mixt/): A fork of `pyxl3` that uses Python 3 type annotations for validation and supports various React-like features
