# GH6 - Add a filter with Copilot CLI

**Time:** 15 minutes, optional. **Starting point:** GH5 committed.
**Goal:** make one small change through the terminal agent.

## 1. Check Your Starting Point

Keep your **fork root** (`Fabric-CICD-Workshop`) open in VS Code. In the terminal,
enter that repository and run:

```text
git status --short
copilot --version
```

Start with GH5 committed. Preserve unrelated work before continuing; do not
discard earlier code or documentation changes. If Git says "not a git
repository", enter your cloned workshop repository, not a parent folder such
as `Fabric`.

Use the current standalone **Copilot CLI**, not the retired `gh copilot`
suggest/explain flow. If it is missing, use the
[main guide's tool setup](../workshop-part1-github-copilot.md#21-tools-to-install).
Skip this optional lab if installation or organization policy blocks it.

## 2. Activate Python and Run the Baseline

From your fork root, enter the application folder:

```text
cd ws-part1-github-copilot/labs/starter
```

Activate its virtual environment. In Bash:

```bash
source .venv/bin/activate
```

If the environment is missing or you use another shell, follow
[GH2 setup](./02-setup.md#2-create-a-virtual-environment). Then run:

```text
python -c "import sys; print(sys.executable)"
python -m pip install -r requirements-dev.txt
python -m pytest --version
python -m pytest -q
python summarize.py data/sales.csv
```

The interpreter must belong to `starter/.venv`, and the supplied requirements
should give `pytest 8.4.2`. Do not install globally or assume the environment
name in the prompt proves the correct interpreter is active.

**Expected:** existing tests pass, and the normal report shows all three regions
with an average of **158.33**. If the average is wrong, finish GH4 before
continuing. If the filter is already implemented, review and test it rather
than asking the agent to add it a second time.

## 3. Launch Copilot CLI from the Fork Root

Keep the starter environment active. From `starter`, run:

```text
cd ../../..
copilot
```

Launching from the fork root lets the CLI discover the GH5 repository kit.
Sign in if prompted and trust only your reviewed fork. Use the CLI's displayed
help if needed; controls vary by version. Never paste passwords or tokens into
chat. The following messages go into **Copilot CLI**, not the Bash or PowerShell
prompt and not VS Code Chat.

## 4. Send the Scope and Context Prompts

Send each message separately and wait for its response.

**Message 1 - scope:**

```text
Work on the sales application in ws-part1-github-copilot/labs/starter only.
Read its README for business rules and run Python commands from that folder
using its .venv interpreter. Do not use a virtual environment at the fork root.
Do not read or copy presenter solutions, edit Part 2, or finish later labs.
Use read-only checks first and ask before overwriting files.
Do not commit, push, create a PR, or create other remote resources.
```

**Message 2 - understand the current code:**

```text
Explain the sales project in ws-part1-github-copilot/labs/starter and its
current tests. Identify where an optional region filter would fit.
Do not edit anything or read presenter answers. Stop after your explanation.
```

**Expected:** the CLI explains the starter code and tests without editing files.
Check that it refers to the starter README and script, not presenter files.

## 5. Request the Scoped Change

Send **Message 3 - implement the filter:**

```text
Add an optional --region argument to summarize.py in the starter folder.
Filter loaded rows before summarizing. Keep existing behavior when omitted.
Treat region names as case-sensitive. Do not add a top-region line.
Unknown regions must exit nonzero with a useful error, not a traceback;
their stdout must be empty and stderr must explain the unknown region.

Add regression tests for East, an unknown region, and the unchanged default.
Include subprocess-based tests that exercise argument parsing, stdout,
stderr and exit codes, not just the filtering expression.
Do not change validation or empty-input behavior; those belong to later labs.
Preserve any validation or empty-input fixes already present.

Use starter/.venv and run the tests from starter.
Ask before overwriting files. Show the diff and test results, then stop.
Do not stage, commit, push, or create a PR.
```

Read proposed changes and commands before approving them. Approve only those
needed for this task. If the agent proposes unrelated work, deny it and narrow
the request. Do not enable broad automatic approval to finish the exercise.

## 6. Exit the CLI and Check the Reports Yourself

Exit the CLI session using its documented exit control. Wait until your normal
shell prompt returns before entering the commands below. From the fork root,
return to the application folder; keep the starter environment active:

```text
cd ws-part1-github-copilot/labs/starter
python summarize.py data/sales.csv --region East
```

**Expected East output:**

```text
East: 150.00
Average per region: 150.00
```

Then run the default report:

```text
python summarize.py data/sales.csv
```

**Expected default output:**

```text
East: 150.00
North: 75.00
West: 250.00
Average per region: 158.33
```

## 7. Check the Expected Failure and Regression Tests

Run the unknown-region command separately:

```text
python summarize.py data/sales.csv --region Unknown
```

Immediately check the exit code: `echo $?` in Bash or `$LASTEXITCODE` in
PowerShell. It must be nonzero. This is an **expected failure**, not a reason to
stop the lab. Stdout should be empty, stderr should explain the unknown region,
and there must be no traceback. Exact error wording may vary.

Do not combine this expected failure with other commands using `&&`; inspect
its exit code before running anything else. Then run:

```text
python -m pytest -q
git diff
git status --short
```

Inspect the regression tests and diff yourself. Require coverage of East, an
unknown region and the unchanged default, including CLI behavior through a
subprocess. Existing tests must still pass, and only the intended starter files
should have changed. If checks fail, return to the CLI, restate the scope and
request a focused repair before repeating verification.

## 8. Review, Stage and Commit

Use `git add` with only the changed filenames you have reviewed. Then inspect
the staged diff yourself:

```text
git diff --cached
```

Commit only after the tests and staged diff are satisfactory. For example:

```text
git commit -m "Add optional region filter"
git status --short
```

Follow your team's Copilot coauthor policy. Do not stage unrelated changes or
create a PR for this optional lab. Before GH7, follow the
[working conventions](./README.md#working-conventions) to ensure completed labs
are on your fork's `main` and pushed to your fork.

**Done when:** East filtering works, the default report is unchanged, an unknown
region fails cleanly, regression tests pass, and the reviewed change is committed.

## Cleanup After a Rehearsal

This lab changes application code and tests, not only a disposable file.
Keep the filter for later labs if desired. To remove a committed rehearsal
change, use a deliberate reviewed revert rather than deleting files or resetting
the repository. Preserve other workshop work. GH7 and GH9 must work without
requiring this optional filter.

**If blocked:** skip this optional feature. GH7 and GH9 use no filter.
Next: [GH7 GitHub](./07-github.md).
