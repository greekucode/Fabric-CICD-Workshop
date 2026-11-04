# GH9 - Ship empty-input handling

**Time:** 20 minutes. **Starting point:** GH7 changes on `main`, clean working tree.
The optional GH6 filter is not required.
**Goal:** complete a small plan-to-PR workflow yourself.

## 1. Check Your Starting Point

This lab makes a real code change and takes it through planning, tests, review
and a merged PR. Unlike GH8, it does not use only a disposable practice file.

Keep your **fork root** (`Fabric-CICD-Workshop`) open in VS Code. In your terminal,
enter that repository and run:

```text
git status --short
git branch --show-current
```

Start from clean `main` with GH7 completed. If changes appear, preserve them
before proceeding; do not discard earlier code or documentation work. If you
are on another branch, switch to `main` only after handling those changes.
If Git says "not a git repository", check your terminal location: a parent
folder such as `Fabric` is not the workshop repository.

## 2. Activate Python and Verify Your Fork

From your fork root, enter the starter folder:

```text
cd ws-part1-github-copilot/labs/starter
```

Complete [GH2's virtual environment setup](./02-setup.md#2-create-a-virtual-environment)
if needed. Activate the starter environment in this terminal. In Bash:

```bash
source .venv/bin/activate
```

For other shells, use GH2's activation instructions. Then check:

```text
python -c "import sys; print(sys.executable)"
python -m pip install -r requirements-dev.txt
python -m pytest --version
```

The interpreter should belong to `starter/.venv`, and the version check should
report `pytest 8.4.2` for the supplied requirements. `No module named pytest`
means the active interpreter is missing the test dependency; install it with the
command above before continuing. Do not install globally or assume the `(.venv)`
prompt proves the correct environment is active.

Run `gh repo set-default --view`: it must name your fork. If necessary use
`gh repo set-default origin` and verify `gh repo view --json nameWithOwner,url`.
Replace `YOUR_GITHUB_LOGIN` below with your GitHub username. Issues and PRs must
stay in your fork; do not send workshop exercises to the upstream repository.

## 3. Run the Baseline

Run these commands from `starter`:

```text
python -m pytest -q
python summarize.py data/sales.csv
```

Existing tests should pass, and the normal average should be **158.33**. Expect
the validated GH7 behavior. If GH7 was skipped, finish its local validation
fallback first; the capstone must preserve validation, not replace it.
If GitHub is unavailable, work from that reviewed local commit and record the
PR/merge steps as blocked instead of claiming full completion.

## 4. Request a Plan

Start a new chat in **Plan mode** and send this message:

```text
Plan only; do not edit files or run write commands.
Work only in ws-part1-github-copilot/labs/starter and read its README
and current tests. Do not read presenter answers or edit Part 2.
Run Python and pytest from starter using its .venv interpreter.

Handle a CSV containing the correct header but no sales rows:
the summary function should return ({}, 0.0), and the CLI should print only
"Average per region: 0.00" followed by a newline, with empty stderr and exit 0.
A zero-byte file without a header must remain invalid.

Preserve existing validation, normal results, and any optional region filter.
Keep data/empty.csv unchanged. Plan function and subprocess regression tests,
plus a tmp_path test that rejects a zero-byte CSV without a traceback.
Retain GH7 invalid-input tests and any GH6 East and unknown-region tests.
The empty-report requirement uses no region filter.

List proposed files and checks, then stop and wait.
```

**Expected:** a scoped plan listing the implementation and test changes, with
no file edits. Review the proposed files and checks before continuing.

## 5. Create the Branch and Implement

In your terminal, create the feature branch yourself:

```text
git switch -c fix/empty-input
```

If the branch already exists, inspect it or choose a fresh name and use that
name consistently in later commands. Do not delete or reset the existing branch.

Switch the chat to **Agent mode** and send:

```text
Implement the reviewed plan on the current feature branch.
Use the starter/.venv interpreter and run tests from starter.
Keep changes limited to the agreed starter files.
Do not stage, commit, push, or create a PR.
Show the changed files and test results, then stop for my review.
```

## 6. Verify and Review the Changes

Run from `starter`:

```text
python summarize.py data/empty.csv
```

Immediately check the exit code: `echo $?` in Bash or `$LASTEXITCODE` in
PowerShell. It must be `0`. The report must contain only:

```text
Average per region: 0.00
```

Then run:

```text
python summarize.py data/sales.csv
python -m pytest -q
git diff
```

Normal output must remain:

```text
East: 150.00
North: 75.00
West: 250.00
Average per region: 158.33
```

Inspect `data/empty.csv`: it must still contain the `region,amount` header and
no rows. Inspect the regression tests, not just the passing test count:

- A function test requires `({}, 0.0)` for no sales rows.
- A subprocess test requires exact stdout, empty stderr and exit 0 for the
  header-only CSV, with no region filter.
- A separate `tmp_path` test requires a zero-byte CSV to fail without a traceback.
- GH7 invalid-input tests still pass. If GH6 was completed, the East and
  unknown-region tests also remain and pass.

If the checks fail, ask Agent to repair only the agreed changes and rerun these
checks before proceeding.

## 7. Stage Only Reviewed Files

Use `git add` with the specific changed filenames you have inspected; do not
stage unrelated files. Then run this yourself:

```text
git diff --cached
```

Supply the staged diff to `/review-changes` if available, or the read-only
reviewer from GH5. Resolve findings, rerun tests and inspect the staged diff
again after any changes. Do not commit until you have reviewed it.

## 8. Commit and Open the PR

After reviewing the staged diff and findings, run the following, replacing
`YOUR_GITHUB_LOGIN` with your GitHub username. Preserve your team's Copilot
coauthor policy when committing.

```text
git commit -m "Handle header-only sales CSV"
git push -u origin fix/empty-input
gh pr create --repo YOUR_GITHUB_LOGIN/Fabric-CICD-Workshop --base main --head fix/empty-input --title "Handle header-only sales CSV" --body "Return an empty summary with a zero average; add regression tests."
```

Confirm the PR page's **base repository is your fork** and base branch is
`main`. Fork PRs can otherwise target upstream; do not omit `--repo`.

Request Copilot review if available; otherwise review manually. Wait for the
**tests** check to pass: a review comment is not a test run. Approve a pending
Actions run only after inspecting its code. If required approving reviews
cannot come from the PR author, obtain an authorized reviewer; do not bypass
the repository's merge rules.

## 9. Merge and Verify Main

Merge using your repository's allowed method. In your local terminal, check:

```text
git status --short
```

Continue only if the tree is clean. From `starter`, run:

```text
git switch main
git pull --ff-only origin main
python -m pytest -q
python summarize.py data/empty.csv
python summarize.py data/sales.csv
```

Stop if the tree is dirty, a pull fails, or the branch diverged. Check each
command's result before continuing. The final success criterion is the merged
local `main`, not only your feature branch.

**Done when:** the PR is merged and the local `main` passes all tests.
If GitHub is unavailable, a locally reviewed/tested branch is a partial completion;
finish the PR steps when access is restored.

## Cleanup After a Rehearsal

Unlike GH8, this lab ends with a committed, merged change. Removing that change
later requires a deliberate reviewed revert, not deleting application or test
files. Do not reset the repository or discard other workshop work. Stopping
before merge is a rehearsal or partial completion, not the full lab outcome.

## Handoff

Carry only the reviewed repository instructions, review prompt and reviewer agent
into Part 2. The prompt references the reviewer, so keep both files together.
Remove sales-specific rules. Part 2 has its own Azure/Fabric setup and data.
Copy the kit from your fork root into Part 2's **separate private attendee
repository**. Do not use the public Part 1 fork as the Fabric Git-sync repository.
Remove starter-specific paths and rewrite the reviewer's README reference too.

Keep or archive your fork for reference. Do not delete anything
automatically. Remove only workshop-only MCP connections if you added them.
