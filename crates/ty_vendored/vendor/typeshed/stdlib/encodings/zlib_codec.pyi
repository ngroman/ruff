"""Python 'zlib_codec' Codec - zlib compression encoding.

This codec de/encodes from bytes to bytes.

Written by Marc-Andre Lemburg (mal@lemburg.com).
"""

import codecs
from _typeshed import ReadableBuffer
from typing import ClassVar

# This codec is bytes to bytes.

def zlib_encode(input: ReadableBuffer, errors: str = "strict") -> tuple[bytes, int]: ...
def zlib_decode(input: ReadableBuffer, errors: str = "strict") -> tuple[bytes, int]: ...

class Codec(codecs.Codec):
    def encode(self, input: ReadableBuffer, errors: str = "strict") -> tuple[bytes, int]: ...  # type: ignore[override]
    def decode(self, input: ReadableBuffer, errors: str = "strict") -> tuple[bytes, int]: ...  # type: ignore[override]

class IncrementalEncoder(codecs.IncrementalEncoder):
    def encode(self, input: ReadableBuffer, final: bool = False) -> bytes: ...  # type: ignore[override]

class IncrementalDecoder(codecs.IncrementalDecoder):
    def decode(self, input: ReadableBuffer, final: bool = False) -> bytes: ...  # type: ignore[override]

class StreamWriter(Codec, codecs.StreamWriter):
    charbuffertype: ClassVar[type] = ...

class StreamReader(Codec, codecs.StreamReader):
    charbuffertype: ClassVar[type] = ...

def getregentry() -> codecs.CodecInfo: ...
