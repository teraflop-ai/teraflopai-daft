from dataclasses import dataclass, field
from typing import Any

from teraflopai import TeraflopAI

from .protocols import (
    SearchEngine,
    SearchEngineDescriptor,
    TextEmbedding,
    TextEmbeddingDescriptor,
    TextSegmenter,
    TextSegmenterDescriptor,
)

DEFAULT_SEGMENTATION_URL = (
    "https://api.segmentation.teraflopai.com/v1/segmentation/free"
)
DEFAULT_SEARCH_URL = "https://api.caselaw.teraflopai.com/v1/search/free"
DEFAULT_EMBEDDING_URL = "https://api.teraflopai.com/v1/embeddings/free"


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
class TeraflopAIEmbeddingDescriptor(TextEmbeddingDescriptor):
    url: str = DEFAULT_EMBEDDING_URL
    model: str | None = None

    def instantiate(self) -> TextEmbedding:
        return TeraflopAIEmbeddings(url=self.url, model=self.model)


@dataclass
class TeraflopAIEmbeddings(TextEmbedding):
    url: str
    model: str | None = None

    def __post_init__(self) -> None:
        self.client = TeraflopAI(url=self.url)

    def embed_text(self, text: list[str]) -> list[Any]:
        out: list[Any] = []
        for item in text:
            resp = self.client.embeddings(item, self.model) if self.model else self.client.embeddings(item)
            out.append(resp["data"][0]["embedding"])
        return out


@dataclass
class TeraflopAITextSegmenter(TextSegmenter):
    url: str
    client: TeraflopAI = field(init=False)

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
    client: TeraflopAI = field(init=False)

    def __post_init__(self) -> None:
        self.client = TeraflopAI(url=self.url)

    def search_text(self, query: list[str]) -> list[Any]:
        out: list[Any] = []
        for item in query:
            resp = self.client.search(item)
            out.append(resp.get("results"))
        return out