"""Claude API pricing (USD per Mtok). Source: anthropic.com/pricing as of 2026-05.

Prompt-caching pricing follows Anthropic's published multipliers:
  - Cache write (5m TTL):  1.25x base input price
  - Cache write (1h TTL):  2.00x base input price
  - Cache read:            0.10x base input price
"""
from dataclasses import dataclass

@dataclass
class Price:
    name: str
    input_per_mtok: float
    output_per_mtok: float

    @property
    def cache_write_5m(self): return self.input_per_mtok * 1.25
    @property
    def cache_write_1h(self): return self.input_per_mtok * 2.0
    @property
    def cache_read(self):      return self.input_per_mtok * 0.10

# Map both alias and full model id -> Price
_PRICES = {
    "claude-haiku-4-5-20251001":  Price("haiku-4.5",  1.0,  5.0),
    "claude-sonnet-4-6-20250929": Price("sonnet-4.6", 3.0, 15.0),
}

def price_for(model_id: str) -> Price | None:
    if model_id in _PRICES: return _PRICES[model_id]
    # fuzzy match on family
    for k, v in _PRICES.items():
        if model_id and (model_id in k or k in model_id):
            return v
    return None

def compute_cost_usd(model_id: str, usage: dict) -> dict:
    """Returns {cost_usd, breakdown:{input,output,cache_write_5m,cache_write_1h,cache_read}}.
    Falls back to None if model not in price table."""
    p = price_for(model_id)
    if p is None:
        return {"cost_usd": None, "breakdown": None, "price_model": None}
    inp  = usage.get("input_tokens", 0) or 0
    out  = usage.get("output_tokens", 0) or 0
    cr   = usage.get("cache_read_input_tokens", 0) or 0
    cw5  = usage.get("cache_creation", {}).get("ephemeral_5m_input_tokens", 0) or 0
    cw1  = usage.get("cache_creation", {}).get("ephemeral_1h_input_tokens", 0) or 0
    breakdown = {
        "input":          inp * p.input_per_mtok      / 1e6,
        "output":         out * p.output_per_mtok     / 1e6,
        "cache_read":     cr  * p.cache_read           / 1e6,
        "cache_write_5m": cw5 * p.cache_write_5m       / 1e6,
        "cache_write_1h": cw1 * p.cache_write_1h       / 1e6,
    }
    total = sum(breakdown.values())
    return {"cost_usd": total, "breakdown": breakdown, "price_model": p.name}
