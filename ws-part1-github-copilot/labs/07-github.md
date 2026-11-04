# GH7 - Delegate and review input validation

**Time:** 30 minutes. **Starting point:** GH5 (or GH6) committed and pushed to `main`.
**Goal:** turn an issue into a reviewed pull request.
Cloud agent, code review and Spaces depend on your account and organization policy.

## 1. Check Your Starting Point and Fork

Keep your **fork root** (`Fabric-CICD-Workshop`) open in VS Code. In your
terminal, enter that repository, then the application folder:

```text
cd ws-part1-github-copilot/labs/starter
git status --short
git branch --show-current
gh repo set-default --view
gh repo view --json nameWithOwner,isFork,url
```

Confirm a clean `main` and **your own public fork**, not `redhatpeter`'s upstream.
Preserve unrelated work before continuing; do not discard earlier code or
documentation changes. If Git says "not a git repository", enter your workshop
clone rather than a parent folder such as `Fabric`.

If the default repository is wrong, run `gh repo set-default origin` and repeat
the repository checks. Replace `YOUR_GITHUB_LOGIN` in later commands with your
GitHub username. Push the completed GH3-GH5 commits (and GH6 if done):

```text
git push origin main
```

Activate `starter/.venv` using [GH2 setup](./02-setup.md#2-create-a-virtual-environment).
In Bash, run `source .venv/bin/activate`, then check the baseline:

```text
python -c "import sys; print(sys.executable)"
python -m pip install -r requirements-dev.txt
python -m pytest -q
python summarize.py data/sales.csv
```

**Expected:** Python belongs to `starter/.venv`, existing tests pass, and the
normal report shows an average of **158.33**. Fix prerequisite problems before
delegating a new change. The optional region filter is not required.

## 2. Enable Issues and Actions in Your Fork

In the **GitHub portal**, open your fork and check the owner in the page header.

1. If **Issues** is missing, open **Settings > General > Features** and enable it.
2. Open **Actions** and enable workflows if GitHub asks. Forks may start with
   workflows disabled.
3. Confirm your account and organization allow cloud-agent delegation and
   Copilot review. Controls vary by account and policy.

Do not change upstream settings or broaden permissions to bypass policy.
If a feature is unavailable, use the local-agent fallback in step 10.

## 3. Ask the Local Agent to Prepare Workflows

Start a new **regular Agent chat in VS Code**, not the read-only reviewer.
Send this message; it is not a terminal command:

```text
Prepare only the GitHub workflows for GH7 at this fork's repository root.
Inspect existing workflow files first. If they already exist, propose only
needed changes; do not blindly replace them. Ask before overwriting files.

Create .github/workflows/tests.yml, triggered by push and pull_request,
with a job ID of tests. Use checkout and Python 3.12. Run
python -m pip install -r requirements-dev.txt and python -m pytest -q,
with working-directory ws-part1-github-copilot/labs/starter on both run steps.

Also create .github/workflows/copilot-setup-steps.yml with workflow_dispatch
and a single job ID exactly copilot-setup-steps. Check out the repository,
set up Python 3.12, and install requirements-dev.txt from the starter folder.
Use minimal read-only contents permissions in both workflows.

Do not read presenter answers, change application code, or edit Part 2.
Show both workflow files and explain the proposed checks, then stop.
Do not stage, commit, push, or create a PR.
```

**Expected:** two workflow files under the repository-root `.github/workflows`,
not `starter/.github`. The `tests` workflow checks code; the setup workflow
prepares the cloud agent's environment and is not itself a PR test check.
Each `run` step starts with its own working directory; a `cd` in a previous
step does not persist.

## 4. Review, Commit and Verify the Baseline Workflow

Inspect both files and the diff yourself. From `starter`, run:

```text
python -m pytest -q
git diff
git -C ../../.. add -- .github/workflows/tests.yml .github/workflows/copilot-setup-steps.yml
git diff --cached
```

Continue only if the staged diff contains the intended workflows and no
unrelated changes. Follow your team's Copilot coauthor policy, then run:

```text
git commit -m "Add workshop test and Copilot setup workflows"
git push origin main
```

If the workflows were already committed and correct, no new commit is needed.
In GitHub's **Actions** tab, open the test workflow run for the current commit
and verify the **tests** job succeeded before assigning the task. A file merely
existing does not prove it ran. If Actions or an action is disallowed, ask the
organizer rather than broadening permissions.

## 5. Create the Issue and Delegate It

In your fork's **Issues** tab, select **New issue**. Use this title:

```text
Validate sales CSV input with useful errors
```

Paste this **issue body**:

```text
Work only in ws-part1-github-copilot/labs/starter. Read its README for business
rules. Run python -m pytest -q from that folder using the interpreter prepared
by the setup workflow. Do not read/copy presenter solutions or edit Part 2.

Required columns are region and amount. Trim surrounding whitespace from
region names and reject blank regions. Reject nonnumeric, negative and
nonfinite amounts. Reject missing columns and malformed rows. Do not silently
skip bad rows. On invalid CSV input, print a helpful error to stderr and exit
nonzero without a traceback. Include the CSV line number for bad rows.
Invalid input must not produce a partial success report on stdout.

Use data/invalid-amount.csv and data/missing-column.csv without changing them.
Use tmp_path for additional fixtures. Add automated tests, including blank
regions, zero amounts, nonfinite amounts, zero-byte files and malformed rows.
Keep the normal sales report and existing tests working, including any
optional region filter. Do not implement header-only CSV handling yet;
that is a separate capstone. Preserve any header-only fix already present.
Do not add application dependencies.
```

Submit the issue, then assign or delegate it to **Copilot** using the available
portal controls. Creating an issue does **not** automatically delegate it.
Confirm the issue shows the assignment or an agent session before continuing.
If delegation is unavailable, use step 10 rather than waiting for an unstarted
task.

Alternatively, run this in the terminal and enter the same title and body:

```text
gh issue create --repo YOUR_GITHUB_LOGIN/Fabric-CICD-Workshop
```

Then return to the portal to delegate the issue.

## 6. Observe the Agent and Review Its PR

Open the agent session from the issue and inspect its log while it works.
When a PR is available, check its **base repository** is your fork and its
base branch is **main**, not upstream. Stop if either is wrong.

Read the code diff and tests before approving anything. Cloud-agent PRs may be
drafts, and workflow runs may require approval. Inspect the code before
approving a run; mark the PR ready when suitable. Check all these cases:

| Input | Expected behavior |
| --- | --- |
| Normal fixture | Same three totals and average 158.33 |
| ` East ` and `East`, with amounts 0 and 10 | One East total of 10; zero accepted |
| Blank/whitespace-only region | Error with CSV line number |
| Nonnumeric, negative, `nan`, `inf` or `1e999` amount | Error with CSV line number |
| Missing `amount` header or zero-byte input | Helpful missing-column/header error |
| Row with a missing/extra field, or unterminated quoted field | Error with CSV line number |

Use temporary test files (`tmp_path`) for additional cases; do not change the
supplied fixtures to make tests pass. Invalid input must produce no partial
success report on stdout. Header-only *success* remains for GH9.

Request Copilot code review if enabled; read each suggestion before applying
it. Add this focused follow-up comment, tagging Copilot if the UI requires it:

```text
Please confirm there is a regression test for a negative amount.
If it is missing, add one within the issue's scope and rerun the tests.
```

**Expected:** the agent identifies or adds the regression test. Inspect the
actual test and updated checks; a comment saying tests pass is not proof.

## 7. Wait for Tests and Merge

In the PR's checks, wait for the **tests** job to pass. A review comment or a
successful setup workflow is not a test run. Resolve findings before merging.

A PR author cannot submit an approving review on their own PR. Review changes
yourself and merge only if repository rules permit it; obtain another
authorized review when required. Do not bypass branch protection. Merge using
your fork's allowed method.

## 8. Pull and Verify Locally

In your local terminal, with the starter environment active, run:

```text
git status --short
```

Continue only if the working tree is clean. From `starter`, run these commands
one at a time and inspect each result:

```text
git switch main
git pull --ff-only origin main
python summarize.py data/sales.csv
```

Stop if a pull fails or Git reports divergent history. Normal output must be:

```text
East: 150.00
North: 75.00
West: 250.00
Average per region: 158.33
```

Run the first invalid fixture separately:

```text
python summarize.py data/invalid-amount.csv
```

Immediately check `echo $?` in Bash or `$LASTEXITCODE` in PowerShell. It must
be nonzero. Stderr must explain the invalid amount and identify **Line 3**,
without a traceback; stdout must contain no partial report.

Then run the second invalid fixture separately:

```text
python summarize.py data/missing-column.csv
```

Immediately check the exit code again. It must be nonzero, with a useful
missing-column error on stderr, no traceback and no partial report on stdout.
Exact error wording can vary. These are **expected failures**, not reasons to
stop the lab. Do not use an `&&` chain or run another command before checking
each exit code. Finally, run:

```text
python -m pytest -q
git status --short
```

**Expected:** all tests pass on the merged local `main`, and verification has
not introduced tracked changes.

## 9. Spaces: a Short Context Demo (Optional)

A Copilot Space collects reusable context for questions about a project. This
optional demo combines the documented business rules, implementation and sample
data so Copilot can explain the intended result and identify any mismatch.
It does not run the script, execute tests or deploy anything to Fabric.

### Create the Space in the GitHub portal

1. Sign in to GitHub with your Copilot-enabled account and open
   [Copilot Spaces](https://github.com/copilot/spaces). Spaces is separate from
   the repository's Code, Issues and Pull requests tabs.
2. Select **Create space** or **New space**. Name it `GCP-Workshop`, choose your
   personal account as owner if prompted, and leave sharing restricted for this
   exercise. Button names and available options can vary.
3. Add this description:

   > Explain the workshop sales report using its documented business rules,
   > implementation and synthetic sample data.

4. In **Instructions**, enter:

   > Use the attached sources to explain this workshop's sales report. Treat the
   > starter README as the intended business rules and the Python script as the
   > current implementation. Cite the sources you use. Flag differences between
   > the code and rules, and show calculations using the CSV. Do not claim to
   > have executed code or tests.

5. Select **Add sources**, choose repository files, and select **your fork** of
   `Fabric-CICD-Workshop`. Choose `main` for this demo if a branch picker appears.
   Add only these three files:

   | File Path in Your Fork | Purpose |
   | --- | --- |
   | `ws-part1-github-copilot/labs/starter/README.md` | Intended business rules |
   | `ws-part1-github-copilot/labs/starter/summarize.py` | Current implementation |
   | `ws-part1-github-copilot/labs/starter/data/sales.csv` | Normal synthetic sample data |

6. Click **Add 3** (or the equivalent confirmation) and verify that all three
   appear under **Sources**. Inspect the paths, not just the filenames. The
   README must be under `labs/starter`, not `labs` or the repository root. If
   you selected the wrong README, remove that source with its trash icon and
   add the starter README instead. Do not select the presenter solution.
7. Select **Start chat** and ask:

   > What does average per region mean here, and what is the expected value?
   > Cite your sources and flag any mismatch between the code and README.

The Space uses files from GitHub, not uncommitted local editor changes. Verify
that the selected branch contains the version you intend to discuss.

### Check the Answer

The documented rule averages **regional totals**, not individual sales. East
totals 150, West 250 and North 75: the expected average is `475 / 3`, approximately
**158.33**. The original starter divides by four sales rows and produces 118.75;
if your fork already contains the GH4 correction, the implementation should
match the rule. Check the answer's citations and arithmetic yourself.

**If Spaces is blocked:** skip this optional demo if it is unavailable under
your account or organization policy. If the portal shows **Unable to update
space** or an HTML/JSON error, refresh and check whether the sources were saved
before retrying. Do not assume the files were added until they appear under
**Sources**.

## 10. Use the Local-Agent Fallback if Needed

Use this route only if cloud delegation is unavailable; do not duplicate a
cloud-agent change already in progress or merged. If only Copilot review is
unavailable, review manually and continue the existing PR instead.

1. From clean local `main`, run `git switch -c fix/input-validation`. If that
   branch exists, inspect it or choose a fresh name and use it consistently.
   Do not delete or reset it.
2. Start a new regular Agent chat in VS Code. Paste the step 5 issue body,
   replacing the setup-workflow interpreter instruction with your local
   `starter/.venv` interpreter. Add this instruction:

   ```text
   Implement this issue on the current feature branch using starter/.venv.
   Ask before overwriting files. Run Python and pytest from starter.
   Show the diff and test results, then stop for my review.
   Do not stage, commit, push, or create a PR.
   ```

3. Review the diff and tests against the step 6 checklist. Run the normal and
   invalid reports and pytest as in step 8 on this feature branch; do not switch
   to `main` or pull during this pre-commit verification.
4. Stage only reviewed filenames with `git add`, then inspect `git diff --cached`.
   Commit the validation change following your team's Copilot coauthor policy.
   For example, use `git commit -m "Validate sales CSV input"`.
5. Push and open a PR with these terminal commands:

```text
git push -u origin fix/input-validation
gh pr create --repo YOUR_GITHUB_LOGIN/Fabric-CICD-Workshop --base main --head fix/input-validation --title "Validate sales CSV input" --body "Validate input with useful errors and regression tests."
```

Fork PR creation often defaults upstream; keep the explicit `--repo` and confirm
the base repository on the PR page before reviewing or merging.
Follow steps 6-8 for review, checks, merge and local verification.

If GitHub is entirely unavailable, keep the reviewed/tested validation commit
locally and record the remote steps as blocked. You may rehearse GH9 on top of
it, but neither lab's remote PR requirement is complete. Observe the presenter's
prepared PR later. Skip Spaces if unavailable.

## Cleanup After a Rehearsal

This lab creates workflows, an issue and a merged application change. It is not
a disposable-file exercise. Removing committed changes requires a deliberate
reviewed revert, not deleting application files or resetting your fork. Preserve
other workshop work. Delete only a practice Space you created if you no longer
need it; do not delete the repository or remove workflows needed by later labs.

**Done when:** the validation PR is reviewed and merged into your fork, its test
check passes, and the merged local `main` passes the reports and regression tests.
Spaces is optional; a locally reviewed/tested fallback without a remote PR is
partial completion.
Next: [GH8 guardrails](./08-guardrails.md).
