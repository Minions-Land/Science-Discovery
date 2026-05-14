# Project-Level Exploration DAG for Autonomous Scientific Discovery

## Abstract

This proposal defines a project-level exploration DAG for autonomous scientific discovery. Here, DAG means directed acyclic graph, not retrieval-augmented generation (RAG). RAG can help retrieve evidence for a node, but the DAG is the durable project memory: it records what a team asked, tried, verified, rejected, and promoted.

The core thesis is simple: autonomous research needs a shared discovery graph that stores questions, assumptions, hypotheses, experiments, citations, decisions, dead ends, and receipts. A final paper should be extracted from the highest-value supported path or subgraph, not invented after the fact as a polished narrative.

## Why Existing Systems Are Not Enough

Adjacent systems solve important slices of the problem, but not the whole operating layer.

| System family | What it contributes | What remains open |
|---|---|---|
| ARA | Artifact layout, claim bindings, traces, evidence folders, dead-end awareness. | A project-wide team graph with path scoring, cross-project reuse, and paper-path extraction. |
| GStack | Stage gates, role separation, review, testing, shipping, reflection. | Scientific evidence semantics and claim-to-receipt bindings. |
| LLM-as-a-Verifier | Better selection among many agent trajectories through fine-grained repeated verification. | Hard evidence receipts. A verifier score is not proof. |
| PROV, RO-Crate, OpenLineage | Standard provenance vocabulary for entities, activities, agents, and lineage. | Scientific novelty, branch value, and paper composition. |
| MLflow, DVC, LangSmith, Langfuse | Runs, metrics, prompts, traces, artifacts, and evaluation records. | Research-level reasoning structure and failed-branch retention as scientific memory. |
| ResearchRabbit, Litmaps | Literature graph navigation. | Internal team exploration and experiment evidence. |
| ELNs such as eLabFTW or Benchling Notebook | Lab records, timestamps, protocols, and review workflows. | Turning a branching investigation history into a supported paper path. |

The gap is not another note-taking tool. The gap is a project-native graph that can absorb all of these signals and keep the research process auditable.

## Proposed System

The proposed system is a persistent graph per project. Nodes represent scientific objects and workflow events. Edges represent dependency, support, contradiction, refinement, execution, citation, or decision relationships. Receipts bind nodes and edges to external evidence or local artifacts.

The system should support both a tree-like view for humans and a DAG model for implementation. A strict tree is too weak because two branches can share the same dataset, citation, failed baseline, or methodological decision. A DAG lets knowledge converge without duplicating records.

## Data Model

```yaml
project:
  id: ASD-001
  root_question: "Can hard-gated agent postures reduce unsupported scientific claims?"

nodes:
  - id: Q-001
    type: question
    text: "What bias does each posture reduce?"
    status: open

  - id: H-003
    type: hypothesis
    text: "A four-posture agent reduces premise and citation errors."
    support_status: tentative

  - id: E-008
    type: experiment
    command: "run benchmark against baseline agents"
    receipt: receipts/experiments/E-008.json

  - id: C-014
    type: citation
    claim: "ARA records dead ends in a trace layer."
    receipt: evidence/citations/C-014.json
    support_status: verified

edges:
  - from: Q-001
    to: H-003
    relation: motivates
  - from: H-003
    to: E-008
    relation: tested_by
  - from: C-014
    to: H-003
    relation: background_support
```

Recommended node types:

- `question`: an unresolved research question.
- `assumption`: a premise that must be made explicit.
- `hypothesis`: a claim that can be tested or falsified.
- `experiment`: an executable test, simulation, benchmark, or analysis.
- `result`: a measured output, table, figure, or failure.
- `citation`: a verified literature support object.
- `decision`: a branch promotion, revision, pause, or rejection.
- `dead_end`: a negative path that should not be repeated without new evidence.

Recommended support states:

- `unverified`: recorded but not checked.
- `tentative`: plausible, but missing complete evidence.
- `verified`: backed by a receipt and linked evidence.
- `refuted`: contradicted by evidence.
- `blocked`: cannot proceed because data, tools, or permissions are missing.
- `out_of_scope`: intentionally excluded.

## Workflow

1. Branch: create a node for every meaningful question, assumption, hypothesis, experiment, citation, or decision.
2. Record: attach actor, timestamp, prompt or command, input artifacts, and output artifacts.
3. Verify: require receipts for citations, experiments, datasets, and major claims.
4. Score: use decomposed criteria, not a single vague quality score.
5. Promote: move only supported branches into the paper path.
6. Retain: keep failed and negative branches with their reason for stopping.
7. Extract: generate a paper or ARA-like artifact from the highest-value supported path or subgraph.

## Minimal Implementation

The first version should avoid becoming a platform. It can be a file-backed artifact that extends the existing ARA style:

```text
artifact/
  logic/
    claims.md
    hypotheses.yaml
  trace/
    exploration_dag.yaml
    team_journal.jsonl
  evidence/
    citations/
      verified.bib
      verification-ledger.jsonl
    receipts/
      searches/*.json
      experiments/*.json
      reviews/*.json
    tables/
    figures/
  views/
    exploration-dag.json
    paper-path.json
```

MVP behavior:

- Append-only event log for team actions.
- YAML or JSON DAG file with typed nodes and edges.
- Citation verification ledger.
- Experiment receipt ledger with command, config, seed, environment, and output hash.
- Simple HTML or React graph view.
- A path extraction command that exports a supported narrative skeleton.

## Evaluation Plan

The proposal should be tested experimentally before any strong claim is made.

| Evaluation question | Possible metric |
|---|---|
| Does the DAG reduce unsupported claims? | Unsupported-claim rate before and after graph gates. |
| Does it prevent repeated failed work? | Number of repeated dead-end attempts per project. |
| Does it improve audit speed? | Time for a new agent or human to verify a claim path. |
| Does it help paper writing? | Fraction of final paper claims linked to verified nodes. |
| Does it preserve novelty? | Path overlap between extracted paper candidates. |
| Does it stay usable? | Duplicate-node rate, graph size, retrieval success, user correction rate. |

Baselines should include ordinary multi-agent chat, ARA-only artifact packaging, and a run-tracker-only workflow. The system should be revised or rejected if it creates impressive diagrams without improving evidence quality, reproducibility, or auditability.

## Non-Goals and Risks

Non-goals:

- It is not a replacement for human scientific judgment.
- It is not a claim that every research process is a clean tree.
- It is not a general RAG product.
- It is not a proof engine that turns verifier scores into truth.

Risks:

- The graph may become a museum of logs that nobody uses.
- Agents may overfit to producing well-formed nodes instead of better science.
- Weak receipt schemas may create false confidence.
- Cross-project reuse may spread mistakes if provenance is shallow.
- Too much friction may slow exploration before the value is visible.

## Closing

The strongest version of this proposal is not a prettier research dashboard. It is a discipline for zero-hallucination scientific work. Agents may explore broadly, but promotion into a paper requires evidence. The DAG is the shared memory that lets the team see not only the final path, but also the abandoned branches, missing receipts, and negative results that made the final path credible.
