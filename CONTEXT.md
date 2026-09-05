# hackforla/HomeUniteUs context
> refreshed 2026-09-05 | upstream default: main @ a58ec988

## Identity & policies
- upstream: hackforla/HomeUniteUs, default branch `main`, primary language Python (FastAPI backend) + React/TS frontend, English-first (yes — issues, docs, UI all English)
- CLA/DCO: none (no CLA bot, no DCO requirement)
- AI-assisted PR policy: unstated (no ban, no disclosure requirement found in repo or org `.github`)
- signed commits required: no (no branch protection on upstream or fork `main`; repo policy passport `signed_commits_required: false`)
- PR template: `.github/pull_request_template.md` (Closes #..., What changes, Rationale, Testing done, optional learnings, screenshots)
- external tracker: github

## Conventions (verified from merged PRs)
- branch naming: mixed — feature-style (`incubator-v2`, `host_contact_form_status_716`, `host-intake-forms-validation-720`) and `fix/` prefix (`fix/sign-up`). Use `<type>/<kebab-description>`.
- test command: `cd backend && poetry run pytest` (Python 3.12, poetry). Frontend: `npm run test`.
- CI: `.github/workflows/run-tests-v1.yml` — `test-api` (poetry pytest) + `test-frontend` (npm test + Cypress e2e) on PRs to `main`.
- outside PRs get merged; repo is active (recent merges, dependabot churn).

## Maintainer picture
- hackforla is a volunteer civic-tech org; maintainer response is paced, not instant.
- active areas (in-flight branches): coordinator dashboard, intake profile endpoints, auth/invite flow, multi-step form — avoid overlapping those.

## Issue-area health
- open issues are mostly PM/design/agenda items, not actionable code bugs.
- `#903` landing-page link error — frontend/deploy, not locally verifiable.
- `#757` generated users not assigned roles — references a removed `api/openapi_server` path; not directly actionable.
- `#933` PostgreSQL 15 compatibility — ops task.
- health endpoint area is quiet (no redesign talk, no in-flight PRs).

## Gap ledger (dedupe — READ FIRST, never re-pick)
- 2026-09-05 self-found gap (health.py nginx error-log path) — outcome: pr-opened — literal `'{nginx_logs_dir}/nginx-error.log'` instead of f-string; verified + fixed + test added.

## Mined gaps (discovered, not yet attempted)
- 2026-09-05 clean-code `backend/app/health.py` `nginx_logs` reads error log from literal path `{nginx_logs_dir}/nginx-error.log` (single quotes) instead of the f-string used for the access log; repro: call endpoint with `HUU_ENVIRONMENT` set and a real access log present -> `FileNotFoundError` on the literal path; expected: read from `/var/log/<env>.homeunite.us/nginx-error.log`; proposed test: monkeypatch `open`, assert both paths use the env dir; dedupe: no upstream issue/PR found — status: attempted (this run)
- 2026-09-05 clean-code `backend/app/modules/workflow/` `UnmatchedCaseRepository.delete_case_for_guest` queries `UnmatchedGuestCaseStatus` instead of `UnmatchedGuestCase` — real bug, needs DB setup — status: proposed
- 2026-09-05 clean-code `backend/app/modules/deps.py` `requires_auth` does `auth_header.split(" ")[1]` -> `IndexError` on a header with no space — minor — status: proposed
