import codecs, io, encodings
import sys
import traceback
from encodings import utf_8
from pyxl_fasthtml.codec.tokenizer import (
    pyxl_fasthtml_invert_tokenize, pyxl_fasthtml_tokenize, pyxl_fasthtml_untokenize,
    PyxlFasthtmlUnfinished,
)

def pyxl_fasthtml_transform(stream, invertible=False, str_function='str'):
    try:
        output = pyxl_fasthtml_untokenize(pyxl_fasthtml_tokenize(stream.readline, invertible, str_function))
    except Exception as ex:
        print(ex)
        traceback.print_exc()
        raise

    return output


def pyxl_fasthtml_invert(stream):
    try:
        output = pyxl_fasthtml_untokenize(pyxl_fasthtml_invert_tokenize(stream.readline))
    except PyxlFasthtmlUnfinished:
        raise
    except Exception as ex:
        print(ex)
        traceback.print_exc()
        raise

    return output


def pyxl_fasthtml_transform_string(input, invertible=False, str_function='str'):
    stream = io.StringIO(input)
    return pyxl_fasthtml_transform(stream, invertible, str_function)


def pyxl_fasthtml_invert_string(input):
    stream = io.StringIO(input)
    return pyxl_fasthtml_invert(stream)


def pyxl_fasthtml_encode(input, errors='strict'):
    # FIXME: maybe we should actually be able to consume partial results
    # instead of this O(n^2) retry thing?
    try:
        return pyxl_fasthtml_invert_string(input).encode('utf-8'), len(input)
    except PyxlFasthtmlUnfinished:
        return b'', 0


def pyxl_fasthtml_decode(input, errors='strict', invertible=False):
    return pyxl_fasthtml_transform_string(bytes(input).decode('utf-8'), invertible), len(input)


class PyxlFasthtmlIncrementalDecoder(codecs.BufferedIncrementalDecoder):
    invertible = False

    def decode(self, input, final=False):
        self.buffer += input
        if final:
            buff = self.buffer
            self.buffer = b''
            return pyxl_fasthtml_transform_string(buff.decode('utf-8'), self.invertible)
        else:
            return ''


class PyxlFasthtmlIncrementalDecoderInvertible(PyxlFasthtmlIncrementalDecoder):
    invertible = True


class PyxlFasthtmlIncrementalEncoder(codecs.BufferedIncrementalEncoder):
    def _buffer_encode(self, input, errors, final):
        return pyxl_fasthtml_encode(input, errors)


class PyxlFasthtmlStreamReader(utf_8.StreamReader):
    decode = pyxl_fasthtml_decode


class PyxlFasthtmlStreamReaderInvertible(utf_8.StreamReader):
    decode = lambda input, errors='strict': pyxl_fasthtml_decode(input, errors, invertible=True)


class PyxlFasthtmlStreamWriter(codecs.StreamWriter):
    encode = pyxl_fasthtml_encode
