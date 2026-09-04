# contezza-for-commerce-agents

**Contezza AI - trusted merchant knowledge for AI commerce agents.** 

A governed merchant data source for Anthropic's [commerce-agents](https://github.com/anthropics/commerce-agents) blueprint —
with citations, evidence validation, and audit trails built in.


## Why

### Shopping agents increasingly rely on merchant websites for product, pricing, and policy information — through model training, information retrieval, and real-time shopping data.

That makes a brand's website a critical source of truth for AI, but the merchant information itself may be **contradictory, outdated, or incomplete.**

When a shopping agent gets a product, pricing, or policy fact wrong — a restocking fee, warranty term, shipping cost, or product price — the problem isn't always hallucination.

Often, the agent is doing exactly what it was designed to do: finding a real piece of merchant information and faithfully repeating it.

Two common failure modes:

**1. Your own pages can contradict each other.**

In our audits of DTC brands, a majority published different numbers for the same product or policy fact. 
One brand's FAQ states a 20% restocking fee; its returns page states 15%. Both are live. An agent answers with whichever source it retrieves.

**2. Your published information becomes stale.**

Prices and policies change regularly, but AI training data, crawls, caches, and other copies of merchant content can lag behind. An agent may return a number that was once correct but is no longer.

The result is an AI answer that can be factually **grounded in the brand's own website — and still be wrong when the shopper asks.**

- A misquoted fee becomes a support ticket.
- A wrong warranty answer becomes a return or chargeback.
- An outdated price can lose the sale.
- Repeated contradictions erode trust in the brand.

The problem isn't only whether AI can find the right information. It's whether the information itself is ready to be trusted by AI.

Contezza AI makes merchant knowledge trustworthy for AI agents. Contezza continuously evaluates merchant content, identifies contradictions and stale information, and maintains a verified knowledge feed for each brand. This adapter performs one specific function: it serves that feed to agents built on the commerce-agents blueprint, as a drop-in `StorefrontBackend`.

See the live demonstration and audit findings at [contezza.ai/agents.html](https://contezza.ai/agents.html).

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
brand-approved and served per tenant — feed URLs (api.contezza.ai) and the MCP surface
(`mcp.contezza.ai/ecommerce/mcp` — "Contezza AI for Merchants") carry the same contract.

Working in Claude Code? The
[contezza-for-merchants plugin](https://github.com/contezza-ai/contezza-plugins) bundles
a feed-authoring skill, a quickstart skill for this adapter, and that MCP surface.

[contezza.ai](https://contezza.ai) · hello@contezza.ai · Apache-2.0
