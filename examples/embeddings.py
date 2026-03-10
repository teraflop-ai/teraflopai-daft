import daft

from teraflopai_daft import attach_teraflopai_provider
from teraflopai_daft.expressions import embed_text

attach_teraflopai_provider()

df = daft.from_pydict(
    {
        "text": [
            "City of Houma",
            "UNITED STATES of America, Appellee, v. Daniel Dee VEON, Appellant.",
        ]
    }
)

df = df.with_column("embeddings", 
    embed_text(
        df["text"], 
        model="concept-embedding-legal-nano", 
        provider="teraflopai"
    )
)
df.show()
