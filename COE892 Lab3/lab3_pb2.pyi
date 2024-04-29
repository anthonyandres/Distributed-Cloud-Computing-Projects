from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class filename(_message.Message):
    __slots__ = ("f",)
    F_FIELD_NUMBER: _ClassVar[int]
    f: str
    def __init__(self, f: _Optional[str] = ...) -> None: ...

class MapArray(_message.Message):
    __slots__ = ("ma", "columns", "rows")
    MA_FIELD_NUMBER: _ClassVar[int]
    COLUMNS_FIELD_NUMBER: _ClassVar[int]
    ROWS_FIELD_NUMBER: _ClassVar[int]
    ma: str
    columns: int
    rows: int
    def __init__(self, ma: _Optional[str] = ..., columns: _Optional[int] = ..., rows: _Optional[int] = ...) -> None: ...

class botID(_message.Message):
    __slots__ = ("bi",)
    BI_FIELD_NUMBER: _ClassVar[int]
    bi: int
    def __init__(self, bi: _Optional[int] = ...) -> None: ...

class moveString(_message.Message):
    __slots__ = ("ms",)
    MS_FIELD_NUMBER: _ClassVar[int]
    ms: str
    def __init__(self, ms: _Optional[str] = ...) -> None: ...

class mineRand(_message.Message):
    __slots__ = ("mr",)
    MR_FIELD_NUMBER: _ClassVar[int]
    mr: str
    def __init__(self, mr: _Optional[str] = ...) -> None: ...

class mineSerialInt(_message.Message):
    __slots__ = ("msi",)
    MSI_FIELD_NUMBER: _ClassVar[int]
    msi: int
    def __init__(self, msi: _Optional[int] = ...) -> None: ...

class notify(_message.Message):
    __slots__ = ("n",)
    N_FIELD_NUMBER: _ClassVar[int]
    n: str
    def __init__(self, n: _Optional[str] = ...) -> None: ...

class confirmation(_message.Message):
    __slots__ = ("c",)
    C_FIELD_NUMBER: _ClassVar[int]
    c: str
    def __init__(self, c: _Optional[str] = ...) -> None: ...
