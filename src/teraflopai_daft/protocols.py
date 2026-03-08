from __future__ import annotations

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class TextSegmenter(Protocol):
    def segment_text(self, text: list[str]) -> list[Any]:
        ...


@runtime_checkable
class SearchEngine(Protocol):
    def search_text(self, query: list[str]) -> list[Any]:
        ...


class TextSegmenterDescriptor:
    def instantiate(self) -> TextSegmenter:
        raise NotImplementedError


class SearchEngineDescriptor:
    def instantiate(self) -> SearchEngine:
        raise NotImplementedError