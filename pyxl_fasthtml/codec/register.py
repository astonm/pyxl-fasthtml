import codecs


def search_function(encoding):
    if encoding != 'pyxl_fasthtml': return None

    import encodings
    from pyxl_fasthtml.codec.transform import pyxl_fasthtml_decode, PyxlFasthtmlIncrementalDecoder, PyxlFasthtmlStreamReader

    # Assume utf8 encoding
    utf8=encodings.search_function('utf8')
    return codecs.CodecInfo(
        name = 'pyxl_fasthtml',
        encode = utf8.encode,
        decode = pyxl_fasthtml_decode,
        incrementalencoder = utf8.incrementalencoder,
        incrementaldecoder = PyxlFasthtmlIncrementalDecoder,
        streamreader = PyxlFasthtmlStreamReader,
        streamwriter = utf8.streamwriter)


codecs.register(search_function)
