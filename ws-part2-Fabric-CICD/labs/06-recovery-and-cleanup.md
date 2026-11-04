# 06 - Recover safely and clean up intentionally

**Time:** 20 minutes for discussion/cleanup; allow more for optional live recovery.
**Starting point:** [05 Production](./05-promote-production.md) complete.
**Goal:** understand forward recovery and leave no surprise resources.

## Before You Start

Choose **discussion only** or **optional live recovery into Test**. Record your
choice before executing commands. Discussion-only attendees skip step 2 and
continue with the resource inventory; do not claim a recovery was executed.
Use your attendee root and virtual environment for local commands.

## 1. Explain recovery before touching anything

There is no general one-click rollback for this path:

```text
revert PR --> reviewed main --> update Dev --> deploy Test --> run checks
                                                   |
                                                   +--> approve --> deploy Production --> run checks
```

Restoring a definition does not restore data. This workshop's notebook overwrites
one tiny synthetic table, so rerunning the reverted baseline rebuilds it.
Real workloads need their own data recovery plan.

Do **not** deploy backward into Dev or rewrite Git history as a shortcut.
Do **not** run the feature helper backwards; use a reviewed Git revert.

## 2. Optional: rehearse recovery into Test

You may discuss this section instead of executing it. Production stays at tax
unless a separate Production recovery is approved.

1. Preserve any uncommitted local work. Confirm the tax feature was squash-merged.
2. Find that PR's merge SHA, replacing `<feature-pr-number>`:

   ```text
   gh pr view <feature-pr-number> --json mergeCommit --jq .mergeCommit.oid
   git switch main
   git pull --ff-only
   git status
   git switch -c recovery/revert-tax
   ```

   Run commands one at a time. Verify `gh repo view --json nameWithOwner,url`
   targets your private attendee repository before looking up the PR. Confirm
   clean `main` before creating the recovery branch. If that branch already
   exists, inspect it or choose a fresh name; do not delete/reset it. Save the
   returned merge SHA and replace `<squash-merge-sha>` below with that actual value.

3. Inspect the identified commit. After approval, revert its actual SHA:

   ```text
   git show --stat <squash-merge-sha>
   git revert <squash-merge-sha>
   python checks/validate_items.py --require-items
   python -m unittest discover -s tests -v
   git show --stat HEAD
   ```

   `git revert` creates a **new commit** and may open your configured editor.
   For a noninteractive invocation use `git revert --no-edit <squash-merge-sha>`.
   Do not apply these commands to a merge commit from a different merge method
   without presenter guidance.

   **Expected:** the strict validator reports `release=baseline`, all 12 tests
   pass, and the new revert commit changes only the intended release files.
   The printed tax total in the validator still tests the prebuilt transformation;
   it does not mean the active release is tax.

4. Expect both the synced notebook and `release.json` back at **baseline**.
   If a conflict occurs, stop and resolve it deliberately; do not reset your tree.
5. Push and open a recovery PR:

   ```text
   git push -u origin recovery/revert-tax
   gh pr create --base main --head recovery/revert-tax --title "Recover baseline sales release" --body "Revert the tax release with a new commit. Redeploy and rerun Test before any Production recovery."
   gh pr checks
   ```

   Confirm the PR base is your private repository's `main`. Inspect its actual
   diff and checks, not just the revert commit message. Keep the PR number and
   recovery SHA as evidence. Stop on failed CI rather than weakening the checks.

6. Review, wait for **validate**, approve and squash-merge:

   ```text
   gh pr merge --squash
   git switch main
   git pull --ff-only
   python checks/validate_items.py --require-items
   ```

7. Update **Dev** from Git; confirm baseline and Dev-local binding.
8. Approve and deploy only the notebook Development -> Test.
9. In Test, verify binding, approve and run all.
10. Expect baseline PASS, **3 rows**, **350.00**, and **no tax column**.
    The notebook uses `overwriteSchema` to support this deliberate synthetic-table
    schema rollback. It is not a safe default for arbitrary production tables.
11. Record that **Test is baseline and Production is still tax**.
    If Production recovery is desired, repeat the approval process and deploy
    the baseline notebook Test -> Production, then approve and run its checks.

Save the Dev/Test run evidence and successful deployment operation. Recovery
into Test alone does not mean Production was recovered. Do not automatically
repeat lab 05's first-deployment item selection: an existing Production target
normally needs only the changed notebook after its dependency pairing is checked.

## 3. Inventory resources before cleanup

Use your local config and list only resources created for this workshop:

| Resource | Keep or remove? |
| --- | --- |
| Four named workspaces and their synthetic items | Your choice |
| One deployment pipeline | Your choice |
| Feature/recovery branches after merge | Remove after disconnecting their workspaces |
| Private workshop repository | Keep for reference or remove explicitly |
| GitHub token / Fabric Git connection | Revoke/remove if workshop-only |
| Existing capacity | Leave alone unless you own it and explicitly approve a change |

**Optional Agent message**, sent in chat rather than the terminal:

```text
We are at lab 06 cleanup. Read-only: inventory only the resources in my workshop
config, including item contents and current Git branches/connections. Show actual
names/IDs and propose a keep/remove checklist. Flag resources with unexpected
contents, unclear ownership or shared credentials. Do not read credential values.
Do not delete anything, unassign stages, disconnect Git, revoke credentials or
pause a capacity until I separately approve the exact resources.
```

For each inventory row, write **keep** or **remove**, plus the verified name/ID.
Leaving a decision blank is not deletion approval. If any resource contains
unrelated items or is shared, stop and exclude it until its owner is consulted.

## 4. Approved cleanup order

Perform only actions you selected:

Use the **Fabric portal** for workspace/pipeline/Git-connection actions and
**GitHub** for repository, branch and token actions. Before each confirmation
dialog, recheck its exact name and scope against your inventory. Cancel if it
does not match. Review current UI warnings; deletion can be irreversible.

1. Save useful PR URLs, operation evidence and local work.
2. In Fabric settings, disconnect the developer workspace and Dev from Git.
   Review pending changes first; preserve any work you want.
3. Delete your workshop deployment pipeline after confirmation.
   Explain that its history/rules will be lost; deleting it is not deleting data
   or a substitute for deleting the workspaces.
4. Delete only your four verified workshop workspaces after inspecting contents.
5. Delete merged feature/recovery branches from your repository.
6. Revoke the workshop-only token in GitHub and remove its unused Fabric account/
   connection entry. Do not revoke a shared credential.
7. Optionally delete your workshop repository only after a separate confirmation.
8. Verify the selected resources no longer appear.

Do not run a broad delete/reset script. There is intentionally no automatic
cleanup helper.
Do not pause a shared/existing capacity. If you independently provisioned a
dedicated paid capacity, coordinate its stop/removal with its owner; deleting
workspaces does not stop capacity billing.

## 5. Verify What Remains

1. Refresh the Fabric workspace and deployment-pipeline lists. Verify only the
   resources approved for removal are absent.
2. Check retained workspaces still have the intended items and connections.
3. In GitHub, verify the chosen branch/repository removals and workshop-only
   token revocation. Never display token values as evidence.
4. Keep local work and the attendee folder unless you separately choose to
   remove them; remote cleanup does not authorize local deletion.
5. Record remaining resources, ownership and any follow-up action. Explicitly
   note whether recovery was discussed, executed only in Test, or also approved
   and verified in Production.

If a removal fails, record the error and current state. Do not compensate with
a broad delete script, change permissions or delete a similarly named resource.

**Done when:** you can explain recovery, any executed recovery passed its checks,
and every remaining workshop resource has an explicit keep/remove decision.

## Handoff

You practiced Git-native Fabric definitions, branch isolation, PR validation,
selective deployment, target-side smoke checks, explicit approval and recovery.
For advanced scenarios, return to the
[full guide](../workshop-part2-Fabric-CICD.md), especially UC8-UC13.
