# 04 - Selectively deploy the notebook to Test

**Time:** 20 minutes.
**Starting point:** [03 change and PR](./03-change-and-pr.md) complete.
**Goal:** promote the reviewed definition without redeploying unrelated items.

## Before You Start

This lab is primarily in the **Fabric portal**. Keep the merged PR and passing
`main` CI run open in GitHub. Do not create another branch or import a notebook.
Use the pipeline and workspace names from your attendee config.

## 1. Confirm the before state

1. Local `main` and Dev are at the reviewed tax release.
2. The GitHub validation run for the merged commit passed.
3. Open **Test's notebook** and confirm `RELEASE = "baseline"`.
4. Confirm Test already has its lakehouse from lab 01.
5. Record the current Test notebook item ID from its URL or item details.
   Use the same ID after deployment to show it was updated rather than duplicated.

Do not edit Test to create the tax feature. The release source is Dev.

**Checkpoint:** Dev is tax, Test is baseline, and Test's lakehouse already
exists. If this is not true, finish the previous lab instead of changing the
deployment selection to compensate.

## 2. Preview the release

In `wk-pipeline-<suffix>`:

1. Confirm Development is your Dev workspace and Test is your Test workspace.
2. Compare the stages in the portal.
3. Select **only `nb_workshop`** for Development -> Test.
4. Confirm `lh_workshop` is already present/paired in Test.
5. Review the destination, item selection and overwrite warning.

**Optional Agent message**, sent before the deployment:

```text
We are doing lab 04 only. Read my pipeline/stages/items and preview a selective
deployment of only nb_workshop from Development to Test. Show actual workspace
and item IDs. Confirm the lakehouse dependency exists and is paired in Test.
Use an explicit items list; do not deploy all items. Wait for approval.
Poll the resulting operation with a bounded timeout, reporting Failed/Canceled/
timeout explicitly. Do not start a second operation while the first is running.
Do not deploy to Production. Inspect Test binding after success, but do not
run the notebook until I approve its synthetic-table overwrite separately.
```

Item lists show identity/pairing, not a reliable definition-change status.
Use portal Compare or a normalized definition diff. A last-deployment timestamp
does not prove an item has or has not been edited.

## 3. Deploy and inspect the operation

1. Approve the reviewed notebook-only deployment.
2. Deploy with note `sales tax release to Test`, if available.
3. Wait for a terminal **Succeeded** result.
4. Open deployment history/details and verify the actual selected item and result.
5. Confirm the Test notebook keeps its existing item ID.
6. Confirm there is one `nb_workshop`, not a duplicate.

An API HTTP 202 means **accepted**, not deployed. A timeout means unresolved,
not success or permission to submit another deployment.

**Checkpoint:** record the operation ID, terminal result, destination and
selected notebook. Deployment success does not yet prove the Test data passed.

## 4. Run Test's persisted-data checks

1. Open the existing Test notebook.
2. Confirm `RELEASE = "tax"`.
3. Check its default lakehouse belongs to **Test**.
4. If binding is missing/wrong, stop, record it, attach Test's `lh_workshop`,
   save and restart the interactive session before running.
5. Approve overwriting only Test's `dbo.sales_wk`.
6. Run all and verify:

   ```text
   PASS: release=tax; rows=3; amount=350.00; amount_with_tax=385.00
   ```

7. Verify the printed workspace ID/name is Test's and the displayed rows match
   [lab 03's expected table](./03-change-and-pr.md#5-smoke-test-the-branch-workspace-before-merge).
8. Review the operation history: baseline deployment, then notebook-only update.

Definitions deploy; data stays as it was until the notebook runs. Before this
run, a baseline table in Test is expected even though its notebook is already tax.

## 5. Save the Test Release Evidence

1. Record the notebook item ID before and after deployment; they must match.
2. Save the successful notebook-only operation and its selected-item details.
3. Save the tax PASS line with Test's workspace identity.
4. Check the persisted table has three rows, amount total **350.00**, and
   `amount_with_tax` total **385.00**.
5. Confirm Production is still untouched and Test still has no Git connection.

Keep this evidence for the Production approval. Do not delete the pipeline or
Test workspace after this lab.

**Done when:** operation succeeded, only the notebook was selected, its item ID
is unchanged, and Test's persisted table passes tax checks.

**If blocked:** inspect the deployment error and dependencies. Do not reimport a
notebook, manually edit Test's business logic, or unassign a stage to force success.
Those actions hide the release problem rather than fix it.

Next: [05 Production](./05-promote-production.md).
