# 01 - Create and deploy the working baseline

**Time:** 30 minutes plus Spark startup.
**Starting point:** [00 readiness](./00-readiness.md) passes.
**Goal:** establish baseline in Dev and Test before changing any code.

## Before You Start

Open the **attendee folder** in VS Code and keep its virtual environment active.
Open the **Fabric portal** in a browser with the intended tenant/account.
Use the names in your local config; replace `<suffix>` before entering names.
This lab creates resources but does not publish the attendee repository yet.

## 1. Create three disposable workspaces

In the Fabric portal:

1. Open **Workspaces > New workspace**.
2. Create your `wk-dev-<suffix>`, `wk-test-<suffix>` and `wk-prod-<suffix>`.
3. Assign each to your approved **existing active capacity**.
4. Confirm you have Admin on each and that Test/Production contain no user-created items.
5. Leave all three disconnected from Git for now.

Do not use My workspace, a shared production workspace, or an existing workspace
with unrelated content.

**Optional Agent message**, not a terminal command:

```text
We are doing lab 01 only. Read my workshop-config.local.json for names.
List my workspaces and available capacities first. Preview creating only my
Dev, Test and lab Production workspaces on the existing capacity in my config.
Reuse only resources verified to belong to this lab. Do not resume a paused
capacity or change permissions. Wait for approval, then create and verify.
Do not import items, connect Git or deploy until I approve those steps separately.
```

**Checkpoint:** all three names and their capacity assignments are correct;
Test and Production are empty. Record workspace IDs from details/URLs without
recording credentials. Stop if a similarly named workspace has unrelated items.

## 2. Import the notebook and attach its lakehouse

In **Dev**:

1. Create a **Lakehouse** named `lh_workshop`.
2. Ensure **Lakehouse schemas** are enabled. Verify the Tables area contains
   the `dbo` schema. If not, stop and create a fresh schema-enabled workshop
   lakehouse; do not try to convert a shared one during the lab.
3. Return to the workspace and choose **Import notebook > From this computer**
   (the menu may be under **New item**).
4. Select your local `notebooks/nb_workshop.ipynb`.
5. Confirm the imported item is named exactly `nb_workshop`; rename only the
   new workshop item if the import added a suffix.
6. Open it with **PySpark** selected.
7. In its lakehouse/Explorer pane, add **Dev's `lh_workshop`** and set it as
   the **default** lakehouse.
8. Save. If a Spark session already started before binding, stop that interactive
   session and start a fresh one.

Do not upload the CSV. The notebook embeds the identical three rows so network
access and file paths cannot derail the CI/CD exercise.

**Checkpoint:** Dev contains exactly the intended lakehouse and notebook
(plus any automatically generated system items). The notebook's default
lakehouse is Dev's copy. Importing the notebook does not execute it.

## 3. Run and verify Dev

1. Read the notebook's overwrite warning.
2. Confirm you are in **Dev**, not another workspace.
3. Inspect the default lakehouse: it must be `lh_workshop` **in Dev**.
4. Approve overwriting only the synthetic `dbo.sales_wk` table.
5. Select **Run all** once; wait for the existing run to finish.
6. Verify the printed workspace name/ID and lakehouse name/ID are Dev's.
7. Expect:

   ```text
   PASS: release=baseline; rows=3; amount=350.00
   ```

Expected table:

| channel | amount |
| --- | --- |
| Online | 100.00 |
| Partner | 50.00 |
| Store | 200.00 |

Open the lakehouse and refresh the Tables view to see `dbo.sales_wk`.
The notebook reads the **persisted** table to verify exact rows, columns and
total; a green cell alone is not the acceptance check.

If the run fails, inspect the existing run's error and workspace/binding before
retrying. Do not click **Run all** repeatedly. Save the PASS line and Dev
workspace identity as evidence; do not capture tokens in screenshots.

## 4. Set up the deployment pipeline

1. Open **Deployment pipelines** from Fabric navigation.
2. Create `wk-pipeline-<suffix>` with ordered stages **Development**, **Test**,
   **Production**.
3. Assign your Dev workspace to Development, Test workspace to Test, and
   lab Production workspace to Production.
4. Check the three workspace names before saving.
5. Confirm you are pipeline Admin. Pipeline permissions are separate from
   workspace permissions.

For Copilot, request a read-only inventory first, then a preview of the pipeline
and assignments. Resolve actual IDs from lists; never invent GUIDs.

**Checkpoint:** read the three stage-to-workspace assignments aloud or record
them before proceeding. No deployment has happened simply by assigning stages.

## 5. Deploy the baseline to Test

1. In the pipeline, inspect Development's items.
2. Select **both `lh_workshop` and `nb_workshop`** for Development -> Test.
   The automatically generated SQL analytics endpoint is not a separate selection.
3. Review the direction, destination and selected items.
4. Approve and deploy, using note `baseline to Test` if a note field is available.
5. Wait for completion and inspect the operation/history result.
6. In **Test**, open the deployed notebook. Do **not** import another copy.
7. Confirm its default lakehouse is **Test's** `lh_workshop`, not Dev's.
   If missing/wrong, stop before running, attach Test's copy, save and restart
   the interactive session. Record this binding adjustment for the presenter.
8. Check that Test's lakehouse has schemas enabled and `dbo` available.
9. After approving the target overwrite, **Run all** and expect the same baseline
   PASS line, with **Test's** workspace printed.

The notebook's cross-workspace guard blocks accidental writes back into Dev,
but binding must still be inspected before every target run.

**Optional Agent message** to send before executing step 5:

```text
Preview deploying only lh_workshop and nb_workshop from Development to Test
in my workshop pipeline. Show source/destination names, actual IDs and items.
Wait for my approval. Track the deployment to a terminal result with a bounded
timeout; report any failure instead of retrying. Confirm target notebook/lakehouse
binding before proposing a separately approved run. Do not deploy to Production
or assume table rows were copied.
```

## 6. Record the Baseline Checkpoint

1. Save Dev's baseline PASS line and workspace identity.
2. Save the successful Development -> Test operation ID/result.
3. Save Test's baseline PASS line and workspace identity.
4. Confirm Production is still empty and none of these workspaces is Git-connected.

Keep these resources for lab 02. Do not perform cleanup between labs.

**Done when:** Dev and Test both pass baseline checks; Production is still empty.
Record the baseline deployment in your notes or screenshots.

**If blocked:** check capacity, both permission systems and item support. A newly
assigned workspace can need time to initialize; inspect the failed operation
before an approved retry. Never unassign/reassign a stage as a quick fix: that
can destroy deployment history and rules.

Next: [02 Git and branch](./02-git-and-branch.md).
