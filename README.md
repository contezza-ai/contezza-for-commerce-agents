# contezza-for-commerce-agents

**Contezza AI - trusted merchant knowledge for AI agents.** A governed data source for
Anthropic's [commerce-agents](https://github.com/anthropics/commerce-agents) blueprint —
citations, evidence validation, and audit trails built in.

Part of **Contezza for Commerce Agents — verified brand answers and data for AI shopping agents**,
from [contezza.ai](https://contezza.ai).

## Why

### Your website is becoming training data, retrieval data, and storefront data for AI — but you don't control what AI learns from it.

Shoppers are increasingly asking AI what to buy, what it costs, and what happens if they
return it. When an AI agent gives the wrong answer, the problem isn't always hallucination.

Often, the agent is doing exactly what it was designed to do: **it finds a real page on the
merchant's site and faithfully repeats what that page says.**

The problem is that the merchant's own information may be **inconsistent, outdated, or
incomplete.**

Two things break:

**1. Your own pages can disagree.**

The same money-critical fact can appear differently across your FAQ, returns policy,
warranty page, product page, or other content. In our audits of DTC ecommerce brands, a
majority published different numbers for the same money fact.

One page says a **20% restocking fee**. Another says **15%**. Both are live. An AI agent
has no reliable way to know which one represents the current policy — so it answers with
whichever source it happens to retrieve.

**2. Your published information can become stale.**

Prices, promotions, product availability, shipping terms, and policies change. But AI
training data, crawled content, caches, and other copies of your site don't necessarily
change with them.

The result is an AI answer that may have been **accurate once — but is wrong when the
shopper asks.**

And when AI becomes part of the buying journey, a wrong answer isn't just an AI problem:

- A misquoted price can lose the sale.
- A wrong fee can create a support ticket.
- A bad warranty answer can create a return or chargeback.
- Repeated contradictions can erode trust in the brand.

### The fundamental problem

**AI agents can only be as reliable as the merchant knowledge they can access.**

Better models can reduce hallucination. They cannot resolve contradictions that exist in
the source material, determine which version of a policy is authoritative, or know that a
previously indexed page is no longer current.

**Contezza fixes the data — so AI can get the answer right.** We check what AI assistants
say about a brand against the brand's own published pages; the brand approves one official
answer per question; the answers are served as a feed with source citations. Where the
brand's pages contradict each other, the answer states the contradiction instead of picking
a side. Sources are re-checked on a schedule, so when a page changes, the affected answer
is flagged before an agent repeats it.

The difference, in Anthropic's blueprint agent — same agent, unmodified, same question,
two backends:

> **Raw pages:** "The returns policy states a **15% restocking fee**…"
> **Verified feed:** "The store's published pages currently show two different figures —
> the FAQ cites **20%** and the returns policy page cites **15%** — and that discrepancy
> hasn't been resolved yet…"

Reproduced across independent runs. The first answer is confident and contradicted by the
brand's own site. The second states the contradiction and doesn't guess.

This adapter is the plug-in: a drop-in `StorefrontBackend` that serves the verified feed
to the same agent.

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
