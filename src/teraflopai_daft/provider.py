from __future__ import annotations

from typing import Any

import daft

from .terafloapai_impl import (
    DEFAULT_EMBEDDING_URL,
    DEFAULT_SEARCH_URL,
    DEFAULT_SEGMENTATION_URL,
    TeraflopAIEmbeddingDescriptor,
    TeraflopAISearchEngineDescriptor,
    TeraflopAITextSegmenterDescriptor,
)


class TeraflopAIProvider:
    """
    Third-party Daft provider for TeraflopAI.

    Shape this to match the provider hooks Daft expects.
    """

    def get_embeddings(
        self,
        model: str | None = None,
        **options: Any,
    ):
        return TeraflopAIEmbeddingDescriptor(
            url=options.get("url", DEFAULT_EMBEDDING_URL),
            model=model,
        )

    def get_text_segmenter(
        self,
        model: str | None = None,
        **options: Any,
    ) -> TeraflopAITextSegmenterDescriptor:
        return TeraflopAITextSegmenterDescriptor(
            url=options.get("url", DEFAULT_SEGMENTATION_URL),
            # model=model,
        )

    def get_search_engine(
        self,
        model: str | None = None,
        **options: Any,
    ) -> TeraflopAISearchEngineDescriptor:
        return TeraflopAISearchEngineDescriptor(
            url=options.get("url", DEFAULT_SEARCH_URL)
        )


def attach_teraflopai_provider(name: str = "teraflopai") -> None:
    daft.attach_provider(TeraflopAIProvider(), name)
