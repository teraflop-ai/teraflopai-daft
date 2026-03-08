## Installation
```bash
uv pip install teraflopai-daft
```

## Usage

Text Segmentation
```python
import daft
from teraflopai_daft import attach_teraflopai_provider
from teraflopai_daft.expressions import segment_text

attach_teraflopai_provider()

df = daft.from_pydict(
    {
        "text": [
            "City of Houma",
            "UNITED STATES of America, Appellee, v. Daniel Dee VEON, Appellant.",
        ]
    }
)

df = df.with_column("segments", segment_text(df["text"], provider="teraflopai"))
df.show()
```

Search
```python
import daft
from teraflopai_daft import attach_teraflopai_provider
from teraflopai_daft.expressions import search_text

attach_teraflopai_provider()

df = daft.from_pydict(
    {
        "text": [
            "City of Houma",
            "Daniel Dee VEON",
        ]
    }
)

df = df.with_column("search", search_text(df["text"], provider="teraflopai"))
df.show()
```