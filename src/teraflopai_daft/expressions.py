from __future__ import annotations

from typing import Any

from daft.ai.provider import Provider
from daft.datatype import DataType
from daft.expressions import Expression
from daft.functions.ai import _resolve_provider
from daft.udf import udf


def segment_text(
    text: Expression,
    *,
    provider: str | Provider | None = None,
    model: str | None = None,
    **options: Any,
) -> Expression:
    resolved_provider = _resolve_provider(provider, "teraflopai")
    descriptor = resolved_provider.get_text_segmenter(model=model, **options)

    expr_udf = udf(
        return_dtype=DataType.list(DataType.string()),
        concurrency=1,
        use_process=False,
    )

    expr = expr_udf(_TextSegmenterExpression)
    expr = expr.with_init_args(descriptor)
    return expr(text)


def search_text(
    query: Expression,
    *,
    provider: str | Provider | None = None,
    model: str | None = None,
    **options: Any,
) -> Expression:
    resolved_provider = _resolve_provider(provider, "teraflopai")
    descriptor = resolved_provider.get_search_engine(model=model, **options)

    expr_udf = udf(
        return_dtype=DataType.list(DataType.string()),
        concurrency=1,
        use_process=False,
    )

    expr = expr_udf(_SearchEngineExpression)
    expr = expr.with_init_args(descriptor)
    return expr(query)

def embed_text(
    text: Expression,
    *,
    provider: str | Provider | None = None,
    model: str | None = None,
    **options: Any,
) -> Expression:
    resolved_provider = _resolve_provider(provider, "teraflopai")
    descriptor = resolved_provider.get_embeddings(model=model, **options)

    expr_udf = udf(
        return_dtype=DataType.list(DataType.float64()),
        concurrency=1,
        use_process=False,
    )

    expr = expr_udf(_TextEmbeddingExpression)
    expr = expr.with_init_args(descriptor)
    return expr(text)


class _TextEmbeddingExpression:
    def __init__(self, descriptor):
        self.embedder = descriptor.instantiate()

    def __call__(self, text_series):
        values = text_series.to_pylist()
        return self.embedder.embed_text(values) if values else []


class _TextSegmenterExpression:
    def __init__(self, descriptor):
        self.segmenter = descriptor.instantiate()

    def __call__(self, text_series):
        values = text_series.to_pylist()
        return self.segmenter.segment_text(values) if values else []


class _SearchEngineExpression:
    def __init__(self, descriptor):
        self.searcher = descriptor.instantiate()

    def __call__(self, query_series):
        values = query_series.to_pylist()
        return self.searcher.search_text(values) if values else []
