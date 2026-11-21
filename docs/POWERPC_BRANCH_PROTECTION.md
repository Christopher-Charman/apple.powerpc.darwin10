# PowerPC development branch protection

The active GitHub ruleset PowerPC Development Protection (ruleset ID 27802286) applies to refs/heads/PowerPC. On 21 November 2026 its unsupported code_scanning and code_quality rule entries were removed after verifying no corresponding CodeQL or code-quality workflow supplied those requirements. Deletion, non-fast-forward, pull-request, required-status-check and Copilot code-review protections were retained, with no bypass actors. Required checks remain source-graph and verify-source-lock.

This repository record describes the protection configuration at the time of the change. GitHub's live ruleset API remains authoritative for its current state. The rule adjustment did not relax source provenance, source-lock verification or the requirement to merge through PRs.
