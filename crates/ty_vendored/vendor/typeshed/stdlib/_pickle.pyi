"""Optimized C implementation for the Python pickle module."""

from _typeshed import ReadableBuffer, SupportsWrite
from collections.abc import Callable, Iterable, Iterator, Mapping
from pickle import PickleBuffer as PickleBuffer
from typing import Any, Protocol, type_check_only
from typing_extensions import TypeAlias

class _ReadableFileobj(Protocol):
    def read(self, n: int, /) -> bytes: ...
    def readline(self) -> bytes: ...

_BufferCallback: TypeAlias = Callable[[PickleBuffer], Any] | None

_ReducedType: TypeAlias = (
    str
    | tuple[Callable[..., Any], tuple[Any, ...]]
    | tuple[Callable[..., Any], tuple[Any, ...], Any]
    | tuple[Callable[..., Any], tuple[Any, ...], Any, Iterator[Any] | None]
    | tuple[Callable[..., Any], tuple[Any, ...], Any, Iterator[Any] | None, Iterator[Any] | None]
)

def dump(
    obj: Any,
    file: SupportsWrite[bytes],
    protocol: int | None = None,
    *,
    fix_imports: bool = True,
    buffer_callback: _BufferCallback = None,
) -> None:
    """Write a pickled representation of obj to the open file object file.

    This is equivalent to ``Pickler(file, protocol).dump(obj)``, but may
    be more efficient.

    The optional *protocol* argument tells the pickler to use the given
    protocol; supported protocols are 0, 1, 2, 3, 4 and 5.  The default
    protocol is 5. It was introduced in Python 3.8, and is incompatible
    with previous versions.

    Specifying a negative protocol version selects the highest protocol
    version supported.  The higher the protocol used, the more recent the
    version of Python needed to read the pickle produced.

    The *file* argument must have a write() method that accepts a single
    bytes argument.  It can thus be a file object opened for binary
    writing, an io.BytesIO instance, or any other custom object that meets
    this interface.

    If *fix_imports* is True and protocol is less than 3, pickle will try
    to map the new Python 3 names to the old module names used in Python
    2, so that the pickle data stream is readable with Python 2.

    If *buffer_callback* is None (the default), buffer views are serialized
    into *file* as part of the pickle stream.  It is an error if
    *buffer_callback* is not None and *protocol* is None or smaller than 5.
    """

def dumps(obj: Any, protocol: int | None = None, *, fix_imports: bool = True, buffer_callback: _BufferCallback = None) -> bytes:
    """Return the pickled representation of the object as a bytes object.

    The optional *protocol* argument tells the pickler to use the given
    protocol; supported protocols are 0, 1, 2, 3, 4 and 5.  The default
    protocol is 5. It was introduced in Python 3.8, and is incompatible
    with previous versions.

    Specifying a negative protocol version selects the highest protocol
    version supported.  The higher the protocol used, the more recent the
    version of Python needed to read the pickle produced.

    If *fix_imports* is True and *protocol* is less than 3, pickle will
    try to map the new Python 3 names to the old module names used in
    Python 2, so that the pickle data stream is readable with Python 2.

    If *buffer_callback* is None (the default), buffer views are serialized
    into *file* as part of the pickle stream.  It is an error if
    *buffer_callback* is not None and *protocol* is None or smaller than 5.
    """

def load(
    file: _ReadableFileobj,
    *,
    fix_imports: bool = True,
    encoding: str = "ASCII",
    errors: str = "strict",
    buffers: Iterable[Any] | None = (),
) -> Any:
    """Read and return an object from the pickle data stored in a file.

    This is equivalent to ``Unpickler(file).load()``, but may be more
    efficient.

    The protocol version of the pickle is detected automatically, so no
    protocol argument is needed.  Bytes past the pickled object's
    representation are ignored.

    The argument *file* must have two methods, a read() method that takes
    an integer argument, and a readline() method that requires no
    arguments.  Both methods should return bytes.  Thus *file* can be a
    binary file object opened for reading, an io.BytesIO object, or any
    other custom object that meets this interface.

    Optional keyword arguments are *fix_imports*, *encoding* and *errors*,
    which are used to control compatibility support for pickle stream
    generated by Python 2.  If *fix_imports* is True, pickle will try to
    map the old Python 2 names to the new names used in Python 3.  The
    *encoding* and *errors* tell pickle how to decode 8-bit string
    instances pickled by Python 2; these default to 'ASCII' and 'strict',
    respectively.  The *encoding* can be 'bytes' to read these 8-bit
    string instances as bytes objects.
    """

def loads(
    data: ReadableBuffer,
    /,
    *,
    fix_imports: bool = True,
    encoding: str = "ASCII",
    errors: str = "strict",
    buffers: Iterable[Any] | None = (),
) -> Any:
    """Read and return an object from the given pickle data.

    The protocol version of the pickle is detected automatically, so no
    protocol argument is needed.  Bytes past the pickled object's
    representation are ignored.

    Optional keyword arguments are *fix_imports*, *encoding* and *errors*,
    which are used to control compatibility support for pickle stream
    generated by Python 2.  If *fix_imports* is True, pickle will try to
    map the old Python 2 names to the new names used in Python 3.  The
    *encoding* and *errors* tell pickle how to decode 8-bit string
    instances pickled by Python 2; these default to 'ASCII' and 'strict',
    respectively.  The *encoding* can be 'bytes' to read these 8-bit
    string instances as bytes objects.
    """

class PickleError(Exception): ...
class PicklingError(PickleError): ...
class UnpicklingError(PickleError): ...

@type_check_only
class PicklerMemoProxy:
    def clear(self, /) -> None: ...
    def copy(self, /) -> dict[int, tuple[int, Any]]: ...

class Pickler:
    """This takes a binary file for writing a pickle data stream.

    The optional *protocol* argument tells the pickler to use the given
    protocol; supported protocols are 0, 1, 2, 3, 4 and 5.  The default
    protocol is 5. It was introduced in Python 3.8, and is incompatible
    with previous versions.

    Specifying a negative protocol version selects the highest protocol
    version supported.  The higher the protocol used, the more recent the
    version of Python needed to read the pickle produced.

    The *file* argument must have a write() method that accepts a single
    bytes argument. It can thus be a file object opened for binary
    writing, an io.BytesIO instance, or any other custom object that meets
    this interface.

    If *fix_imports* is True and protocol is less than 3, pickle will try
    to map the new Python 3 names to the old module names used in Python
    2, so that the pickle data stream is readable with Python 2.

    If *buffer_callback* is None (the default), buffer views are
    serialized into *file* as part of the pickle stream.

    If *buffer_callback* is not None, then it can be called any number
    of times with a buffer view.  If the callback returns a false value
    (such as None), the given buffer is out-of-band; otherwise the
    buffer is serialized in-band, i.e. inside the pickle stream.

    It is an error if *buffer_callback* is not None and *protocol*
    is None or smaller than 5.
    """

    fast: bool
    dispatch_table: Mapping[type, Callable[[Any], _ReducedType]]
    reducer_override: Callable[[Any], Any]
    bin: bool  # undocumented
    def __init__(
        self,
        file: SupportsWrite[bytes],
        protocol: int | None = None,
        fix_imports: bool = True,
        buffer_callback: _BufferCallback = None,
    ) -> None: ...
    @property
    def memo(self) -> PicklerMemoProxy: ...
    @memo.setter
    def memo(self, value: PicklerMemoProxy | dict[int, tuple[int, Any]]) -> None: ...
    def dump(self, obj: Any, /) -> None:
        """Write a pickled representation of the given object to the open file."""

    def clear_memo(self) -> None:
        """Clears the pickler's "memo".

        The memo is the data structure that remembers which objects the
        pickler has already seen, so that shared or recursive objects are
        pickled by reference and not by value.  This method is useful when
        re-using picklers.
        """
    # this method has no default implementation for Python < 3.13
    def persistent_id(self, obj: Any, /) -> Any: ...

@type_check_only
class UnpicklerMemoProxy:
    def clear(self, /) -> None: ...
    def copy(self, /) -> dict[int, tuple[int, Any]]: ...

class Unpickler:
    """This takes a binary file for reading a pickle data stream.

    The protocol version of the pickle is detected automatically, so no
    protocol argument is needed.  Bytes past the pickled object's
    representation are ignored.

    The argument *file* must have two methods, a read() method that takes
    an integer argument, and a readline() method that requires no
    arguments.  Both methods should return bytes.  Thus *file* can be a
    binary file object opened for reading, an io.BytesIO object, or any
    other custom object that meets this interface.

    Optional keyword arguments are *fix_imports*, *encoding* and *errors*,
    which are used to control compatibility support for pickle stream
    generated by Python 2.  If *fix_imports* is True, pickle will try to
    map the old Python 2 names to the new names used in Python 3.  The
    *encoding* and *errors* tell pickle how to decode 8-bit string
    instances pickled by Python 2; these default to 'ASCII' and 'strict',
    respectively.  The *encoding* can be 'bytes' to read these 8-bit
    string instances as bytes objects.
    """

    def __init__(
        self,
        file: _ReadableFileobj,
        *,
        fix_imports: bool = True,
        encoding: str = "ASCII",
        errors: str = "strict",
        buffers: Iterable[Any] | None = (),
    ) -> None: ...
    @property
    def memo(self) -> UnpicklerMemoProxy: ...
    @memo.setter
    def memo(self, value: UnpicklerMemoProxy | dict[int, tuple[int, Any]]) -> None: ...
    def load(self) -> Any:
        """Load a pickle.

        Read a pickled object representation from the open file object given
        in the constructor, and return the reconstituted object hierarchy
        specified therein.
        """

    def find_class(self, module_name: str, global_name: str, /) -> Any:
        """Return an object from a specified module.

        If necessary, the module will be imported. Subclasses may override
        this method (e.g. to restrict unpickling of arbitrary classes and
        functions).

        This method is called whenever a class or a function object is
        needed.  Both arguments passed are str objects.
        """
    # this method has no default implementation for Python < 3.13
    def persistent_load(self, pid: Any, /) -> Any: ...
