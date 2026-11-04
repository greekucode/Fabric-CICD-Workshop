# 03 - Ship the prebuilt tax change through a PR

**Time:** 30 minutes.
**Starting point:** [02 Git and branch](./02-git-and-branch.md) complete.
**Goal:** focus on the review/release loop, not writing transformation code.

## Before You Start

Use the attendee root and active virtual environment for terminal commands.
Open your **private attendee repository** in GitHub and the **developer branch
workspace** in Fabric. Do not use the Part 1 fork or the shared Dev workspace
for the branch smoke test.

## 1. Inspect before changing

From your attendee repository:

```text
git status
git branch --show-current
git pull --ff-only
python checks/validate_items.py --require-items
```

Expect a clean tree, branch **feature/sales-tax**, release **baseline**.
Stop if you are on `main` or there are unexplained changes.

Run `git status` and the branch check before pulling. If either is unexpected,
stop before the pull. Also verify the CLI's repository target:

```text
gh repo view --json nameWithOwner,isPrivate,url
```

If it points elsewhere, set `gh repo set-default <owner>/<repository>` using
your configured private repository and verify again before creating a PR.

## 2. Preview the supplied change

```text
python prepare_release.py
```

This prints a diff but writes **nothing**. It finds the Fabric-generated notebook
using its `.platform` metadata, preserving its item identity and binding.
It proposes exactly two files:

- The synced notebook under `fabric/`: `RELEASE = "baseline"` -> `"tax"`.
- `release.json`: `baseline` -> `tax`.

The 10% calculation and smoke tests are already built in. The release selector
lets you practice a real definition change without implementing data processing.
The import seed under `notebooks/` stays baseline; never reimport it over a
deployed item.

**Optional Agent message**, not a shell command:

```text
We are in lab 03. Inspect branch and status, run prepare_release.py without
--apply, and explain the two-file diff. Do not rewrite the notebook,
.platform IDs, bindings, workflow or tests. Wait for my approval.
After approval, apply only the supplied release change and run the local
strict validator and tests from the attendee root. Show results and stop.
Do not stage, commit, push, create/merge a PR, sync Fabric or run a notebook
until I separately approve those operations.
```

## 3. Apply locally and verify

After reviewing and approving:

```text
python prepare_release.py --apply
python checks/validate_items.py --require-items
python -m unittest discover -s tests -v
git diff --stat
git diff
```

Expected: **12 tests pass**, strict validator says `release=tax`.
The pure transformation checks exact channels/amounts, expected column shapes,
tax total **385.00**, and rejection of an unknown release.
No Spark, Fabric call, commit or push has happened.

If the helper reports a failure or more than the expected semantic changes,
stop and inspect the diff. Do not rerun `--apply` or reset files to conceal it.

For `.ipynb` exports, JSON reformatting can enlarge the diff. Inspect it to
confirm only the release value changed semantically and no metadata was lost.
The helper normally sees Fabric's Python export, which gives a tiny diff.

## 4. Commit, push and open the PR

Stage only the two reviewed files: `release.json` and the notebook path printed
by the helper. In VS Code Source Control, stage these explicitly; do not stage
unrelated files.

```text
git diff --cached
```

After approval:

```text
git commit -m "Enable tax-inclusive workshop sales"
git push
gh pr create --base main --head feature/sales-tax --title "Enable sales tax release" --body "Activate the prebuilt 10 percent tax transformation. Expected: 3 rows, amount 350.00, amount_with_tax 385.00."
gh pr diff
gh pr checks
```

Run these commands one at a time. On the created PR page, confirm the base is
your **private attendee repository / main** and the head is **feature/sales-tax**.
Record the PR URL and number for release evidence and lab 06 recovery.
`gh pr checks` may report pending checks; inspect the existing run and wait
for its terminal result rather than creating another PR.

Wait for **validate** to pass. Inspect the actual GitHub Actions run if it fails.
CI does not execute Spark, verify target binding, deploy items or scan for all
possible secrets. A green check is one gate, not proof the release works in Fabric.

If protection requires another reviewer, get that review. The author cannot
supply their own required approval; use a presenter/partner as needed.

## 5. Smoke-test the branch workspace before merge

1. Open the **developer branch workspace**, not shared Dev.
2. Source control should show incoming changes. Review and **Update from Git**.
3. Wait until sync finishes. If conflicts appear, stop; do not blindly prefer
   remote or overwrite unsaved work.
4. Confirm the notebook now says `RELEASE = "tax"`.
5. Inspect the default lakehouse and workspace before running.
6. After approval, **Run all** once.
7. Expect this developer workspace and:

   ```text
   PASS: release=tax; rows=3; amount=350.00; amount_with_tax=385.00
   ```

| channel | amount | amount_with_tax |
| --- | --- | --- |
| Online | 100.00 | 110.00 |
| Partner | 50.00 | 55.00 |
| Store | 200.00 | 220.00 |

Recheck PR diff/checks if any later binding fix added another commit. Do not
merge while the branch workspace has unexplained uncommitted changes.

**Checkpoint:** save the tax PASS line and developer workspace identity with
the PR evidence. Test must still be baseline; a local test result alone cannot
replace this target-side Spark run.

## 6. Merge the reviewed release

1. Review the PR diff, passing checks and branch-workspace smoke result.
2. Ask for explicit approval to merge.
3. Use a **squash merge** for a straightforward recovery commit:

   ```text
   gh pr merge --squash
   git switch main
   git pull --ff-only
   python checks/validate_items.py --require-items
   python -m unittest discover -s tests -v
   ```

If squash merge is disabled by repository policy, use the allowed method and ask
the presenter to adjust the recovery commands; never override policy.
Keep the feature branch until cleanup because its workspace is still connected.

Run merge, branch switch, pull and tests separately. Confirm your working tree
is clean before switching branches. Save the resulting `main` commit SHA with:

```text
git rev-parse HEAD
```

In GitHub **Actions**, also wait for **validate** on that merged `main` commit
to pass. A green check on the feature commit is not the merged-commit result.

## 7. Update shared Dev from main

1. In **Dev** Source control, review incoming changes.
2. Update from Git. Wait for synchronization to complete.
3. Verify `RELEASE = "tax"` and the Dev-local lakehouse.
4. Approve and run the notebook in Dev.
5. Expect the tax PASS line with **Dev's** workspace printed.
6. Leave Test untouched: it should still contain the **baseline** notebook.

## 8. Record the Release Checkpoint

1. Record the merged PR, `main` commit SHA and passing merged-commit CI run.
2. Record the branch workspace's successful tax run.
3. Record Dev's successful tax run after **Update from Git**.
4. Verify Test remains baseline and Production remains empty.

Keep the feature branch and workspaces. Cleanup and optional recovery belong
to lab 06, not this PR step.

**Done when:** reviewed PR merged, CI green, Dev passes tax checks, Test remains
baseline. A merge alone does not update Fabric; **Update from Git** is required.

**If blocked:** the helper intentionally refuses a second apply, missing items,
wrong math or mismatched release markers. Inspect the branch/diff rather than
resetting or rerunning blindly. Preserve your work before recovery.

Next: [04 deploy Test](./04-deploy-test.md).
