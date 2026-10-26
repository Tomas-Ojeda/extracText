from typing import Protocol


class TextExtractor(Protocol):
    def extract(self, data: bytes, filename: str) -> str: ...


class ChecksumCalculator(Protocol):
    def compute(self, data: bytes) -> str: ...