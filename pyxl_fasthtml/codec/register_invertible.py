import codecs


def search_function(encoding):
    if encoding != 'pyxl_fasthtml': return None

    from pyxl_fasthtml.codec.transform import (
        pyxl_fasthtml_encode, pyxl_fasthtml_decode, PyxlFasthtmlIncrementalDecoderInvertible, PyxlFasthtmlIncrementalEncoder,
        PyxlFasthtmlStreamReaderInvertible, PyxlFasthtmlStreamWriter,
    )

    return codecs.CodecInfo(
        name = 'pyxl_fasthtml',
        encode = pyxl_fasthtml_encode,
        decode = lambda b: pyxl_fasthtml_decode(b, invertible=True),
        incrementalencoder = PyxlFasthtmlIncrementalEncoder,
        incrementaldecoder = PyxlFasthtmlIncrementalDecoderInvertible,
        streamreader = PyxlFasthtmlStreamReaderInvertible,
        streamwriter = PyxlFasthtmlStreamWriter,
    )


codecs.register(search_function)
