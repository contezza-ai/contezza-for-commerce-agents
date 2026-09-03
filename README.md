# contezza-for-commerce-agents

**Verified ecommerce answers for AI shopping agents.** A governed data source for
Anthropic's [commerce-agents](https://github.com/anthropics/commerce-agents) blueprint —
citations, evidence validation, and audit trails built in.

Part of **Contezza for Commerce Agents — verified brand answers and data for AI shopping agents**,
from [contezza.ai](https://contezza.ai).

## Why

Shopping agents built on crawled merchant pages inherit those pages' problems. Across our
audits of DTC brands, brands' own surfaces disagreed on money facts — one brand's FAQ
states a **20% restocking fee** while its returns policy page states **15%**, both live.
Run on raw pages, the blueprint agent confidently picks ONE number. Run on a governed
feed, the same agent — unmodified — answers honestly:

> **Raw pages:** "The returns policy states a **15% restocking fee**…"
> **Governed feed:** "The store's published pages currently show two different figures —
> the FAQ cites **20%** and the returns policy page cites **15%** — and that discrepancy
> hasn't been resolved yet…"

Same agent, unmodified — reproduced across independent runs.

## Use

```python
from contezza_governed_backend import ContezzaGovernedBackend

backend = ContezzaGovernedBackend.from_feed("examples/acme-outdoors.yaml")
agent = ShoppingAgent(backend=backend, config=ShoppingAgentConfig(...), client=...)
```

The backend serves `search_policies`, `search_products`, and `get_product_details` from a
Contezza Verified Answers feed; cart, orders, and checkout raise `NotOffered` — wire your
own systems for those, or disable them in `ShoppingAgentConfig`.

**Behavior guarantees:**
- Policy answers are the brand's **approved canonical text**, served with citations.
- Where a brand's surfaces disagree and the brand hasn't reconciled them, the entry says
  so explicitly (`needs_reconciliation`) — your agent never inherits a coin-flip between
  contradicting pages.
- Every answer traces to source anchors that are re-verified on schedule; an entry whose
  anchor disappears flags STALE upstream before it can mislead a shopper.

`examples/acme-outdoors.yaml` is a fictional demonstration feed. Live brand feeds are
brand-approved and served per tenant — feed URLs (api.contezza.ai) and MCP endpoints
(mcp.contezza.ai) carry the same contract.

[contezza.ai](https://contezza.ai) · hello@contezza.ai · Apache-2.0
