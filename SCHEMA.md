# Field guide

The machine-readable rules are in `schema/card.schema.json` and `schema/tool.schema.json`. This page explains them.
Run `make check` (or `python3 scripts/check.py`) to test a file against them.

## What counts as an AlgoGen

From *Introduction to Algogens: Integrating Generative AI with Algorithmic Frameworks* (Shachar, 2024,
arXiv:2403.01426): "a blend of generative artificial intelligence and traditional algorithms". Algorithms are the
backbone and the guide rails, and generative AI explores solutions inside them.

The library lists the more involved kind: a model proposes candidates, an algorithm or another authority judges
them, and the judgment steers the next proposals. That loop is the admission test for a card.

An agent harness is the software around a language model that makes it an agent (tools, memory, state, sandbox,
feedback loops). A harness can be an AlgoGen. The `beyond_harness` field records the ways a system goes further.

## Cards (`cards/<slug>.json`)

One file per research system. Example:

```json
{
  "slug": "funsearch",
  "name": "FunSearch",
  "org": "Google DeepMind",
  "year": 2023,
  "domain": "math",
  "family": "program-evolution",
  "parent": null,
  "one_liner": "An LLM writes small programs, an evaluator runs them, and the best ones seed the next round.",
  "loop": {
    "proposes": "Python functions that build cap sets or pack bins",
    "judged_by": "An evaluator that runs each program and scores the result",
    "steers": "Top-scoring programs go back into the prompt for the next generation"
  },
  "headline_result": "Exact wording the primary source supports, with its numbers and conditions.",
  "caveat": "What this does not prove, in one or two sentences.",
  "beyond_harness": ["algorithm-is-solver", "population-search", "output-outlives-model"],
  "beyond_harness_note": "One sentence: how this goes beyond an agent harness.",
  "proposal_object": "program",
  "generative_model": "Pretrained LLM, frozen",
  "algorithmic_authority": "Program evaluator in a sandbox",
  "feedback_payload": "score",
  "update_target": "population+context",
  "loop_stage": "inference",
  "validity_scope": "empirical",
  "evidence_level": "experiment",
  "lineage": "origin",
  "direct_algogen_link": "conceptual-fit",
  "sources": [
    {"title": "Paper title", "url": "https://...", "kind": "paper", "supports": "headline_result, loop"}
  ],
  "youtube_id": null,
  "verification": {"status": "verified", "checked_on": "2026-11-03", "notes": "What was opened and what was corrected."}
}
```

Allowed values:

- `domain`: math, optimization, proofs, code-verification, chemistry, materials, engineering, robotics, security,
  science, ml-systems.
- `family`: formalize-and-solve, program-evolution, proof-state-search, verifier-guided-repair,
  oracle-trained-generation, active-learning-generation, offline-solver-discovery.
- `parent`: the slug of the parent system for a variant (for example `alphageometry` for AlphaGeometry2), else null.
- `beyond_harness`, one or more, only what the source supports:
  - `algorithm-is-solver`: the algorithm solves the problem; the model is one part of it.
  - `inverted-control`: the algorithm is in charge and calls the model as a subroutine.
  - `output-outlives-model`: the product (an algorithm, heuristic, proof, molecule, crystal) is useful without the model.
  - `domain-authority-judge`: a formal or physical authority (proof assistant, verifier, docking, DFT, simulator) decides validity.
  - `retrains-generator`: feedback updates the generator's weights (reinforcement learning, fine-tuning, active learning).
  - `population-search`: the loop runs over a population, archive or search tree.
  - `non-llm-generator`: the generative model is not an LLM (diffusion, VAE, SMILES RNN, and so on).
  - `design-time`: AI is used offline to discover a solver; the deployed result runs without it.
  - `formal-kernel`: a proof assistant or formal verifier checks every step.
  - `multi-fidelity`: candidates pass from cheap filters to expensive high-fidelity checks.
  - `neuro-symbolic`: the model formulates the problem and an exact solver finishes it.
  - `meta-evolution`: the loop searches over agent architectures, workflows or search operators.
  - `physical-grounding`: the loop commands lab instruments, robots or physical hardware.
  - `intra-algorithmic`: the model works inside the inner loop of a classical algorithm (A* heuristics, MCTS
    branching, genetic operators) while the outer algorithm keeps control.
- `proposal_object`: specification, program, heuristic, proof, tactic, construction, molecule, crystal, protein,
  reward-function, patch, fuzz-target, equation, kernel, search-operator.
- `feedback_payload`: score, ranking, verbal-reflection, verifier-errors, proof-state, reward, new-data,
  multi-fidelity, coverage, test-results.
- `update_target`: context, population, search-tree, weights, training-data, or several joined by `+`.
- `loop_stage`: training, inference, offline-design, continuous-operation.
- `validity_scope`: formal, empirical, surrogate, approximate-physical.
- `evidence_level`: description, code, experiment, independent-replication, deployment.
- `lineage`: origin, derivative, successor, application.
- `direct_algogen_link`: `conceptual-fit` unless the source itself cites arXiv:2403.01426 (`explicit-citation`) or
  uses the word Algogen (`uses-term`); then quote it in `verification.notes`.
- `sources[].kind`: paper, code, blog, news, docs, video, dataset.
- `verification.status`: `submitted` for a new contribution; maintainers change it to `verified` or `corrected`
  after checking every claim against its sources.
- `video_notes` (optional): short facts, each with its source, used to script a card video.

## Tools (`tools/<slug>.json`)

One file per installable open-source tool. Fields: `slug`, `name`, `author`, `kind` (library, tool or loop),
`repo_url`, `install`, `one_liner`, `loop` (`proposes`, `judged_by`, `steers`), `not_proved`, `license`,
`sources` (`title`, `url`), `checked_on` (YYYY-MM-DD).

## Writing rules

- Plain English, short sentences, no hype words.
- `headline_result` states only what the primary source states, with its numbers and conditions.
- `caveat` (cards) and `not_proved` (tools) are required and specific: budget, benchmark scope, self-reported
  numbers, docking is not activity, and so on.
- Never claim a system was inspired by or builds on the Algogens book unless its source shows that.
