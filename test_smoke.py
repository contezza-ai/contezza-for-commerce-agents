# Smoke test against the fictional example feed. Requires the commerce-agents
# blueprint on PYTHONPATH (for its backend/type contracts) plus pyyaml.
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from contezza_governed_backend import ContezzaGovernedBackend

FEED = Path(__file__).parent / "examples/acme-outdoors.yaml"


def test_routes():
    b = ContezzaGovernedBackend.from_feed(FEED)

    q1 = asyncio.run(b.search_policies(None, "restocking fee change of mind return"))
    assert q1[0].policy_id == "policy.returns.fee" and "NEEDS_RECONCILIATION" in q1[0].content

    q2 = asyncio.run(b.search_policies(None, "is there a lifetime warranty on the tent"))
    assert any(p.policy_id == "policy.warranty.term" for p in q2)

    q3 = asyncio.run(b.search_policies(None, "how long do I have to return an item"))
    assert q3[0].policy_id == "policy.returns.window"

    prods = asyncio.run(b.search_products(None, "four person summit tent"))
    assert prods and prods[0].product_id == "summit-tent-4p"

    details = asyncio.run(b.get_product_details(None, "summit-tent-4p"))
    assert details is not None and "499" in str(details)


if __name__ == "__main__":
    test_routes()
    print("ok")
