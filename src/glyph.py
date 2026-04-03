from abc import ABC, abstractmethod
from config import FontConfig as fc


class Glyph(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...

    @property
    @abstractmethod
    def unicode(self) -> str: ...

    @property
    @abstractmethod
    def offset(self) -> int: ...

    @abstractmethod
    def draw(self, pen, dc) -> None: ...
