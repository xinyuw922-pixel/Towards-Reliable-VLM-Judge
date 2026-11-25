# Contributing to GridWM-Judge

Thank you for your interest in improving **GridWM-Judge**, the diagnostic benchmark accompanying *Towards Reliable VLM Judges: State-Conditional Invariance and Presentation-Aware Diagnostics* (NeurIPS 2026 Evaluations and Datasets Track).

We welcome well-scoped contributions to documentation, reproducibility, simulator-based data generation, inference interfaces, diagnostics, and scoring. As this repository accompanies a published research result, changes affecting the evaluation protocol require particular care.

## Before you start

- Read the [README](README.md) for the supported workflows, task definitions, installation instructions, and expected outputs.
- Search [existing issues](https://github.com/xinyuw922-pixel/Towards-Reliable-VLM-Judge/issues) and [pull requests](https://github.com/xinyuw922-pixel/Towards-Reliable-VLM-Judge/pulls) to avoid duplicate work.
- Use the **Bug Report** or **Feature Request** issue form for substantive changes. Small typo fixes can be proposed directly.
- Be respectful and follow the [Code of Conduct](CODE_OF_CONDUCT.md).
- For **potential security vulnerabilities**, follow [SECURITY.md](SECURITY.md) rather than opening a public issue.

## What kinds of contributions are useful?

- Clearer installation instructions, examples, diagrams, and accessibility improvements.
- Deterministic bug fixes and reproducibility improvements.
- New diagnostics or controlled probes with clearly specified semantics and ground truth.
- Improvements to inference providers, response validation, scoring, and error reporting.
- Carefully isolated support for other environments or third-party dependencies.

**Benchmark integrity:** Please do not silently alter the canonical tasks, group construction, ground-truth labels, scoring denominators, prompts, output schemas, or reported experimental cohorts. If any of these must change, explain the scientific motivation, identify affected protocols and metrics (e.g., `p_active`, `IDR_raw`, `IDR_cond`, NS/JCR), document compatibility, and provide before/after evidence. Treat new protocols or benchmark versions as additions unless maintainers explicitly approve a change to an existing protocol.

## Development setup

The project uses Python with separate **core** and **Habitat** Conda environments. Start with the core environment:

```bash
conda env create -f environments/core.yml
conda run -n gridwm-repro-core python -m pip install -r requirements/core.lock.txt
conda run -n gridwm-repro-core python -m pip check
conda activate gridwm-repro-core
```

Run commands from the repository root. The README lists the system OpenGL/EGL/GLU requirements and the separate Habitat installation instructions. Habitat/HSSD scenes require separately licensed external assets; do not commit or redistribute them with a PR.

## Validate your changes

There is no requirement to make paid model API calls to propose a fix. Choose checks that match the files changed and describe what you actually ran.

For documentation-only contributions, inspect Markdown links and code examples; mark runtime checks **N/A** in the PR template. For Python changes, at minimum check that modified modules import/compile, and run an appropriate deterministic or small smoke workflow where practical:

```bash
python -m compileall -q tools utils

export RUN_ROOT="$HOME/gridwm-runs"
bash scripts/generate_minigrid.sh --profile smoke \
  --output "$RUN_ROOT/contrib-smoke"
```

For request-format or inference changes, validate generated requests and, if applicable, use `bash scripts/infer.sh ... --dry-run` as documented in the README. **Do not make live API calls without deliberately configuring your provider credentials and accepting the associated cost.** For scoring changes, compare results against an unchanged baseline on the same response data, with a fresh scoring output directory. Preserve failure and missing-response handling and group-level matching.

For reproducibility-sensitive changes:

- State the dataset, task, commit SHA, seed, environment, renderer (when applicable), and exact commands.
- Use fresh output directories for comparisons. Resume only when code, configuration, seed, interpreter, and renderer are compatible with the original run.
- Document any changes to pinned environments or requirement lock files.
- Supply a minimal reproduction, regression check, or representative output difference whenever possible.

## Code and repository conventions

- Keep changes focused. Use the existing launcher layer (`scripts/`), task implementation (`tools/`), and common helper modules (`utils/`) instead of creating parallel pathways without explanation.
- Prefer readable Python, explicit configuration, deterministic seeds, and informative errors.
- Keep authoritative simulator state and answer keys out of model-facing inputs except in explicitly designated controlled experiments (such as Oracle-State); document any such exception.
- Do not commit generated output, response JSONL, logs, checkpoints, credentials, large media, or licensed third-party assets. Check `.gitignore` and review `git status` before committing.
- Never disclose API keys or private credentials in Issues, PRs, screenshots, stack traces, or logs; redact any sensitive values.
- Follow the [MIT License](LICENSE) for contributed source code and documentation. Third-party source and dataset licenses remain their own; see [third-party/README.md](third-party/README.md).

## Opening a pull request

1. Fork the repository (or work on an appropriate feature branch), and keep your branch updated with `main`.
2. Make the smallest coherent change, including documentation and evidence where relevant.
3. Run relevant checks; record the commands, outputs, and any limitations.
4. Open a PR against `main` and complete the [PR template](.github/PULL_REQUEST_TEMPLATE.md). Mark inapplicable items **N/A** rather than checking tests you did not run.
5. Allow maintainers to review scientific assumptions, protocol compatibility, and test evidence before merging.

We cannot guarantee that every requested feature or contribution will be merged, particularly if it changes the published benchmark protocol or increases maintenance burden substantially.
