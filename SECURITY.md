# Security Policy

GridWM-Judge is academic research software for simulator-based dataset generation, model API inference, and diagnostic scoring. This policy explains how to report security issues in the repository; it does **not** claim that the code has undergone a formal security audit.

## Supported versions

| Version / branch | Security maintenance |
| --- | --- |
| Current `main` branch | Best-effort review of reported security issues |
| Older commits, forks, and unmaintained versions | Not actively maintained |

There is currently no separately announced long-term-support release or guaranteed remediation timeline.

## Reporting a vulnerability

**Please do not open a public GitHub issue or pull request for an undisclosed security vulnerability.**

Send a private report to **qinanzhang@mail.ustc.edu.cn** with the subject `GridWM-Judge security report`. If GitHub's *Report a vulnerability* feature is enabled on this repository, that private channel may also be used.

Where possible, include:

- A short explanation of the issue and potential impact.
- The affected file, code path, commit SHA, and environment or dependency versions.
- Minimal steps or a proof of concept that does not expose private data or harm external systems.
- Any suggested mitigation or workaround.
- A safe way for the maintainers to request further information.

Do not attach real API credentials, private datasets, personal information, or other sensitive material. Redact them before sharing logs and screenshots.

The maintainers will review reports on a **best-effort** basis and may coordinate a fix or disclosure with the reporter. No guaranteed acknowledgement, fix, or response SLA is promised.

## Security boundaries and good practices

- Inference workflows may communicate with **third-party model API providers**. Review provider URLs and data-handling terms before sending requests.
- Use environment variables or local, untracked configuration to supply credentials; do not commit `.env` files or tokens.
- Generated data, API responses, and logs can contain prompts or provider metadata. Review and redact them before sharing.
- MiniGrid, MiniWorld, Habitat-Sim, and HSSD are **external dependencies/assets** with their own update and license terms; this policy does not cover vulnerabilities in third-party services or projects.
- Avoid executing untrusted code, shell commands, or model-generated text as commands without review.

For reproducibility problems, broken scripts, documentation errors, or non-sensitive bugs, use the public [Bug Report form](https://github.com/xinyuw922-pixel/Towards-Reliable-VLM-Judge/issues/new/choose) instead.
