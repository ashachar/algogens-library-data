# AlgoGens Library dataset

The open data behind [algogens.org/library](https://algogens.org/library/): published systems in which a
generative model proposes candidates, an algorithm or another authority judges them, and that judgment steers the
next proposals. FunSearch, AlphaEvolve, AlphaProof and about a hundred others, each checked against its primary
sources.

## What is in here

- `cards/`: one JSON file per research system (99 at v1.0.0). Each card records the loop (what is proposed, what
  judges it, how the judgment steers the next round), the headline result as the source states it, what the result
  does not prove, a fixed classification, and the sources that were checked.
- `tools/`: one JSON file per installable open-source tool built on the same pattern (19 at v1.0.0).
- `schema/`: JSON Schemas for both (`card.schema.json`, `tool.schema.json`).
- `SCHEMA.md`: the field guide, with every allowed value explained.
- `scripts/check.py`: a dependency-free validator. `tests/fixtures/` holds valid and broken samples.

## Use it

```bash
git clone https://github.com/ashachar/algogens-library-data
cd algogens-library-data
make check
```

```python
import json, pathlib
cards = [json.loads(p.read_text()) for p in pathlib.Path("cards").glob("*.json")]
print(sum(c["validity_scope"] == "formal" for c in cards), "systems with a formal judge")
```

## Submit your system or tool

- Easiest: open an issue with the
  [Submit your system or tool](https://github.com/ashachar/algogens-library-data/issues/new?template=submit.yml)
  form. If you paste a JSON entry, a bot checks it against the schema and comments with the result.
- Or open a pull request that adds `cards/<slug>.json` or `tools/<slug>.json`. Run `make check` first; the same
  check runs on every pull request.

Every claim needs a public source. New cards come in as `"status": "submitted"`, and every new card or tool is
checked against its sources before it is merged.

## Cite it

Citation details are in [`CITATION.cff`](CITATION.cff) (GitHub shows a "Cite this repository" button). Releases
are archived on Zenodo, which gives each one a DOI.

The idea behind the library comes from Amir Shachar, *Introduction to Algogens: Integrating Generative AI with
Algorithmic Frameworks* (2024), [arXiv:2403.01426](https://arxiv.org/abs/2403.01426).

## License

The data and documentation are under [CC BY 4.0](LICENSE). You may share and adapt them with attribution. The
systems described belong to their authors; the cards describe and cite them, and the library is not affiliated
with them.
