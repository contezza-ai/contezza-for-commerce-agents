# Copyright 2026 TechMatrix AI Systems LLC
# SPDX-License-Identifier: Apache-2.0
"""contezza-governed-backend — a governed source-of-truth backend for Anthropic's
commerce-agents blueprint (github.com/anthropics/commerce-agents).

Routes the blueprint's shopping agent to brand-verified answers with citations,
evidence validation, and audit trails, instead of crawled-and-paraphrased pages:

    from contezza_governed_backend import ContezzaGovernedBackend
    backend = ContezzaGovernedBackend.from_feed("feeds/<brand>.yaml")
    agent = ShoppingAgent(backend=backend, config=..., client=...)

Feed source today: a Contezza Verified Answers feed file (YAML). Coming: HTTP feed URL
(api.contezza.ai) and per-tenant MCP endpoints (mcp.contezza.ai) — same contract.

Behavior guarantees this backend adds to any fork:
- Policy answers are the brand's APPROVED canonical text, served with their citations.
- Where the brand's own surfaces disagree and the brand hasn't reconciled them, the
  entry says so explicitly (status: needs_reconciliation) — the agent never inherits a
  coin-flip between contradicting pages.
- Every served answer traces to anchors that are re-verified on schedule (an entry whose
  source anchor disappears flags STALE upstream before it can mislead a shopper).
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from shopping_agent.backend import NotOffered, StorefrontBackend
from shopping_agent.types import Cart, Policy, ProductDetails, UserPreferences


import re as _re


_STOP = {"what", "the", "with", "and", "how", "does", "it", "is", "a", "an", "do",
         "you", "to", "of", "my", "i", "for", "in", "on", "there", "comes", "your",
         "can", "much", "if", "me", "long"}


def _terms(text: str) -> set[str]:
    return set(_re.sub(r"[^a-z0-9$%]+", " ", text.lower()).split()) - _STOP


def _rank(policies: list[Policy], query: str, limit: int = 3) -> list[Policy]:
    q = _terms(query)
    scored = [
        (len(q & _terms(p.title + " " + (p.category or "") + " " + p.content))
         + 2 * len(q & _terms(p.title)), p)   # title hits count double
        for p in policies
    ]
    return [p for s, p in sorted(scored, key=lambda x: -x[0]) if s][:limit]


class ContezzaGovernedBackend(StorefrontBackend):
    """StorefrontBackend over a Contezza governed answer feed. Catalog + policies are
    served; cart/orders/checkout are NotOffered (wire your own systems for those, or
    disable them in ShoppingAgentConfig)."""

    def __init__(self, feed: dict[str, Any]) -> None:
        self.brand = feed.get("brand", "")
        self._catalog = [
            ProductDetails(
                product_id=c["product_id"], title=c["title"], brand=self.brand,
                price=float(c.get("price", 0.0)),
                long_description=c.get("description"),
                specs={k: str(v) for k, v in (c.get("specs") or {}).items()},
            )
            for c in feed.get("catalog", [])
        ]
        self._policies = []
        for e in feed.get("entries", []):
            cites = ", ".join(c["url"] for c in e.get("citations", []))
            status = ("" if e.get("status") == "verified"
                      else f" [STATUS: {e.get('status', 'draft').upper()} — brand review pending]")
            self._policies.append(Policy(
                policy_id=e["id"],
                title=(e.get("intents") or [e["id"]])[0],
                category=(e.get("topics") or ["general"])[0],
                content=f"{e['answer']['text']}{status} (Verified against: {cites})",
            ))

    @classmethod
    def from_feed(cls, path: str | Path) -> "ContezzaGovernedBackend":
        return cls(yaml.safe_load(Path(path).read_text()))

    # -- governed surface --------------------------------------------------------
    async def search_policies(self, session, query):  # noqa: ANN001
        return _rank(self._policies, query)

    async def search_products(self, session, query, filters=None, limit=10):  # noqa: ANN001
        q = query.lower()
        hits = [p for p in self._catalog if any(w in p.title.lower() for w in q.split())]
        return (hits or list(self._catalog))[:limit]

    async def get_product_details(self, session, product_id):  # noqa: ANN001
        return next((p for p in self._catalog if p.product_id == product_id), None)

    # -- not offered here: wire your own systems or disable in config ------------
    async def get_cart(self, session) -> Cart:  # noqa: ANN001
        raise NotOffered("cart")

    async def add_to_cart(self, session, product_id, quantity=1):  # noqa: ANN001
        raise NotOffered("cart")

    async def update_cart_item(self, session, product_id, quantity):  # noqa: ANN001
        raise NotOffered("cart")

    async def remove_from_cart(self, session, product_id):  # noqa: ANN001
        raise NotOffered("cart")

    async def get_preferences(self, session) -> UserPreferences:  # noqa: ANN001
        return UserPreferences()

    async def checkout_handoff(self, session, *a: Any, **k: Any):  # noqa: ANN001
        raise NotOffered("checkout")

    async def get_account_context(self, session):  # noqa: ANN001
        return None

    async def get_orders(self, session, limit=5):  # noqa: ANN001
        return []

    async def get_order(self, session, order_id):  # noqa: ANN001
        return None

    async def get_disclosure(self, session, *a: Any, **k: Any):  # noqa: ANN001
        raise NotOffered("disclosures")

    async def get_fulfillment_options(self, session, *a: Any, **k: Any):  # noqa: ANN001
        raise NotOffered("fulfillment")
