from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from teraflopai import TeraflopAI

from .protocols import (
    SearchEngine,
    SearchEngineDescriptor,
    TextSegmenter,
    TextSegmenterDescriptor,
)

DEFAULT_SEGMENTATION_URL = "https://api.segmentation.teraflopai.com/v1/segmentation/free"
DEFAULT_SEARCH_URL = "https://api.caselaw.teraflopai.com/v1/search/free"


@dataclass
class TeraflopAITextSegmenterDescriptor(TextSegmenterDescriptor):
    url: str = DEFAULT_SEGMENTATION_URL

    def instantiate(self) -> TextSegmenter:
        return TeraflopAITextSegmenter(url=self.url)


@dataclass
class TeraflopAISearchEngineDescriptor(SearchEngineDescriptor):
    url: str = DEFAULT_SEARCH_URL

    def instantiate(self) -> SearchEngine:
        return TeraflopAISearchEngine(url=self.url)


@dataclass
class TeraflopAITextSegmenter(TextSegmenter):
    url: str

    def __post_init__(self) -> None:
        self.client = TeraflopAI(url=self.url)

    def segment_text(self, text: list[str]) -> list[Any]:
        out: list[Any] = []
        for item in text:
            resp = self.client.segment(item)
            out.append(resp.get("results"))
        return out


@dataclass
class TeraflopAISearchEngine(SearchEngine):
    url: str

    def __post_init__(self) -> None:
        self.client = TeraflopAI(url=self.url)

    def search_text(self, query: list[str]) -> list[Any]:
        out: list[Any] = []
        for item in query:
            resp = self.client.search(item)
            out.append(resp.get("results"))
        return out