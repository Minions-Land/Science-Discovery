# MinionsOS Memory Benchmark Adapter Architecture

## Overview

The adapter layer bridges the four memory benchmarks (LoCoMo, MemBench, MemoryAgentBench, MemoryArena) to MinionsOS's native memory APIs (`mos_draft_*`, `mos_book_*`, `mos_reel_*`, `mos_shelf_*`). Each benchmark has distinct data shapes and evaluation protocols; adapters normalize them into a unified interface.

---

## Core Abstractions

### `BenchmarkAdapter` (base class)

```python
# outline/memory/adapters/base.py

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Iterator

@dataclass
class BenchmarkSample:
    """Normalized sample fed to MinionsOS memory APIs."""
    sample_id: str
    context: str          # Long text / conversation history
    query: str            # The question / probe
    gold_answer: Any      # Expected output (str, list, dict)
    metadata: dict        # Benchmark-specific extras

@dataclass
class EvalResult:
    sample_id: str
    predicted: Any
    gold: Any
    score: float          # 0.0 – 1.0
    latency_ms: float
    tokens_used: int
    metadata: dict

class BenchmarkAdapter(ABC):
    """Abstract base for all four benchmark adapters."""

    name: str                  # e.g. "locomo"
    version: str               # dataset version tag

    # --- Data loading ---
    @abstractmethod
    def iter_samples(self, split: str = "test") -> Iterator[BenchmarkSample]:
        """Yield normalized samples from the benchmark dataset."""

    # --- Memory population ---
    @abstractmethod
    def populate_memory(self, sample: BenchmarkSample) -> str:
        """
        Write sample context into MinionsOS memory.
        Returns a session_id / memory_key for later retrieval.
        """

    # --- Inference ---
    @abstractmethod
    def run_inference(self, sample: BenchmarkSample, session_id: str) -> Any:
        """Query MinionsOS with sample.query; return raw model output."""

    # --- Scoring ---
    @abstractmethod
    def score(self, predicted: Any, gold: Any) -> float:
        """Compute benchmark-specific metric (F1, EM, ranking score…)."""

    # --- Cleanup ---
    def cleanup(self, session_id: str) -> None:
        """Optional: purge memory entries created for this sample."""
        pass
```

---

## MinionsOS API Mapping

| Benchmark | Primary API | Rationale |
|-----------|-------------|-----------|
| LoCoMo | `mos_reel_*` | Long conversational histories → reel (sequential episodes) |
| MemBench | `mos_book_*` + `mos_shelf_*` | Structured fact storage + retrieval |
| MemoryAgentBench | `mos_draft_*` + `mos_reel_*` | Agent task scratchpads + episode logs |
| MemoryArena | `mos_shelf_*` | Preference ranking over stored responses |

---

## Concrete Adapters

### 1. LoCoMo Adapter

```python
# outline/memory/adapters/locomo_adapter.py

from .base import BenchmarkAdapter, BenchmarkSample, EvalResult
from minions.tools.reel import mos_reel_append, mos_reel_query, mos_reel_clear

class LoCoMoAdapter(BenchmarkAdapter):
    name = "locomo"
    version = "v1.0"

    def populate_memory(self, sample: BenchmarkSample) -> str:
        session_id = f"locomo_{sample.sample_id}"
        for turn in self._parse_turns(sample.context):
            mos_reel_append(session_id=session_id, turn=turn)
        return session_id

    def run_inference(self, sample: BenchmarkSample, session_id: str) -> str:
        return mos_reel_query(session_id=session_id, query=sample.query)

    def score(self, predicted: str, gold: str) -> float:
        return _token_f1(predicted, gold)

    def cleanup(self, session_id: str) -> None:
        mos_reel_clear(session_id=session_id)

    def _parse_turns(self, context: str) -> list[dict]:
        # Split on speaker markers; return list of {role, content} dicts
        ...
```

### 2. MemBench Adapter

```python
# outline/memory/adapters/membench_adapter.py

from .base import BenchmarkAdapter, BenchmarkSample
from minions.tools.book import mos_book_write, mos_book_read
from minions.tools.shelf import mos_shelf_store, mos_shelf_fetch

class MemBenchAdapter(BenchmarkAdapter):
    name = "membench"
    version = "v1.0"

    def populate_memory(self, sample: BenchmarkSample) -> str:
        session_id = f"membench_{sample.sample_id}"
        facts = self._extract_facts(sample.context)
        for fact in facts:
            mos_book_write(key=f"{session_id}:{fact['id']}", value=fact['text'])
        mos_shelf_store(tag=session_id, payload={"fact_ids": [f['id'] for f in facts]})
        return session_id

    def run_inference(self, sample: BenchmarkSample, session_id: str) -> str:
        index = mos_shelf_fetch(tag=session_id)
        # retrieve relevant facts then answer
        relevant = [mos_book_read(key=f"{session_id}:{fid}") for fid in index["fact_ids"]]
        return self._answer(sample.query, relevant)

    def score(self, predicted: str, gold: str) -> float:
        return float(predicted.strip().lower() == gold.strip().lower())  # EM

    def _extract_facts(self, context: str) -> list[dict]:
        ...

    def _answer(self, query: str, facts: list[str]) -> str:
        ...
```

### 3. MemoryAgentBench Adapter

```python
# outline/memory/adapters/agent_bench_adapter.py

from .base import BenchmarkAdapter, BenchmarkSample
from minions.tools.draft import mos_draft_create, mos_draft_update, mos_draft_read
from minions.tools.reel import mos_reel_append, mos_reel_query

class MemoryAgentBenchAdapter(BenchmarkAdapter):
    name = "memory_agent_bench"
    version = "v1.0"

    def populate_memory(self, sample: BenchmarkSample) -> str:
        session_id = f"mab_{sample.sample_id}"
        draft_id = mos_draft_create(session_id=session_id, content=sample.context)
        for step in self._parse_steps(sample.context):
            mos_reel_append(session_id=session_id, turn=step)
        return session_id

    def run_inference(self, sample: BenchmarkSample, session_id: str) -> Any:
        scratchpad = mos_draft_read(session_id=session_id)
        history = mos_reel_query(session_id=session_id, query=sample.query)
        return self._agent_step(sample.query, scratchpad, history)

    def score(self, predicted: Any, gold: Any) -> float:
        return _task_success(predicted, gold)

    def _parse_steps(self, context: str) -> list[dict]:
        ...

    def _agent_step(self, query, scratchpad, history) -> Any:
        ...
```

### 4. MemoryArena Adapter

```python
# outline/memory/adapters/arena_adapter.py

from .base import BenchmarkAdapter, BenchmarkSample
from minions.tools.shelf import mos_shelf_store, mos_shelf_fetch, mos_shelf_rank

class MemoryArenaAdapter(BenchmarkAdapter):
    name = "memory_arena"
    version = "v1.0"

    def populate_memory(self, sample: BenchmarkSample) -> str:
        session_id = f"arena_{sample.sample_id}"
        for i, response in enumerate(sample.metadata["candidates"]):
            mos_shelf_store(tag=f"{session_id}:cand_{i}", payload={"text": response})
        return session_id

    def run_inference(self, sample: BenchmarkSample, session_id: str) -> list[int]:
        n = len(sample.metadata["candidates"])
        candidates = [mos_shelf_fetch(tag=f"{session_id}:cand_{i}") for i in range(n)]
        return mos_shelf_rank(query=sample.query, items=candidates)

    def score(self, predicted: list[int], gold: list[int]) -> float:
        return _kendall_tau(predicted, gold)
```

---

## Runner

```python
# outline/memory/runner.py

import time
from typing import Type
from .adapters.base import BenchmarkAdapter, BenchmarkSample, EvalResult

class BenchmarkRunner:
    def __init__(self, adapter: BenchmarkAdapter, split: str = "test"):
        self.adapter = adapter
        self.split = split

    def run(self, max_samples: int | None = None) -> list[EvalResult]:
        results = []
        for i, sample in enumerate(self.adapter.iter_samples(self.split)):
            if max_samples and i >= max_samples:
                break
            t0 = time.perf_counter()
            session_id = self.adapter.populate_memory(sample)
            predicted = self.adapter.run_inference(sample, session_id)
            latency_ms = (time.perf_counter() - t0) * 1000
            score = self.adapter.score(predicted, sample.gold_answer)
            self.adapter.cleanup(session_id)
            results.append(EvalResult(
                sample_id=sample.sample_id,
                predicted=predicted,
                gold=sample.gold_answer,
                score=score,
                latency_ms=latency_ms,
                tokens_used=0,   # filled by adapter if tracking
                metadata={"benchmark": self.adapter.name},
            ))
        return results

    def summarize(self, results: list[EvalResult]) -> dict:
        scores = [r.score for r in results]
        latencies = [r.latency_ms for r in results]
        return {
            "benchmark": self.adapter.name,
            "n": len(results),
            "mean_score": sum(scores) / len(scores) if scores else 0,
            "mean_latency_ms": sum(latencies) / len(latencies) if latencies else 0,
        }
```

---

## Directory Layout

```
outline/memory/
├── ADAPTER_ARCHITECTURE.md   ← this file
├── API_REFERENCE.md
├── adapters/
│   ├── __init__.py
│   ├── base.py
│   ├── locomo_adapter.py
│   ├── membench_adapter.py
│   ├── agent_bench_adapter.py
│   └── arena_adapter.py
├── runner.py
├── datasets/                  ← Task #4 will populate this
│   ├── locomo/
│   ├── membench/
│   ├── memory_agent_bench/
│   └── memory_arena/
└── smoke_tests/               ← Task #5
```

---

## Metric Helpers (shared)

```python
# outline/memory/adapters/metrics.py

from collections import Counter
import math

def _token_f1(pred: str, gold: str) -> float:
    p_toks = Counter(pred.lower().split())
    g_toks = Counter(gold.lower().split())
    common = sum((p_toks & g_toks).values())
    if common == 0:
        return 0.0
    precision = common / sum(p_toks.values())
    recall    = common / sum(g_toks.values())
    return 2 * precision * recall / (precision + recall)

def _kendall_tau(pred: list[int], gold: list[int]) -> float:
    n = len(pred)
    concordant = discordant = 0
    for i in range(n):
        for j in range(i + 1, n):
            p = (pred[i] - pred[j])
            g = (gold[i] - gold[j])
            if p * g > 0:
                concordant += 1
            elif p * g < 0:
                discordant += 1
    denom = n * (n - 1) / 2
    return (concordant - discordant) / denom if denom else 0.0

def _task_success(pred: Any, gold: Any) -> float:
    # Benchmark-specific; override in subclass if needed
    return float(pred == gold)
```

---

## Design Decisions

1. **One adapter per benchmark** — isolation makes it easy to swap datasets or metrics without touching other benchmarks.
2. **API affinity** — each adapter maps to the MinionsOS API that best fits the benchmark's memory access pattern (sequential → reel, structured → book/shelf, scratchpad → draft).
3. **session_id namespacing** — prefixing prevents key collisions across concurrent runs.
4. **Cleanup by default** — `cleanup()` is called after every sample to avoid memory contamination between samples.
5. **Runner is benchmark-agnostic** — the same `BenchmarkRunner` works with all four adapters; benchmark-specific logic stays in the adapter.
