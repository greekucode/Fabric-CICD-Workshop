# 05 - Approve and promote to lab Production

**Time:** 15 minutes plus Spark startup.
**Starting point:** [04 Test](./04-deploy-test.md) passed.
**Goal:** release the tested definition with an explicit human decision.

## Before You Start

Use the **Fabric portal** and your release evidence from labs 03-04.
Production in this workshop means only your disposable `wk-prod-<suffix>`
workspace. No real customer workspace or data belongs in this exercise.

## 1. Assemble the release evidence

Before deploying, collect:

- The merged PR URL and commit SHA on `main`.
- Passing **validate** run.
- Successful Development -> Test operation.
- Test notebook PASS line and the printed Test workspace.
- The exact destination and item list for this promotion.

If any evidence is missing, stop. Do not promote based only on "the chat said it worked."

Put the evidence in a local note or the PR discussion without secrets. Record
the approver and intended release SHA. If Test's definition or binding changed
after its successful run, inspect and reverify it before requesting approval.

## 2. Preview Test -> Production

1. Open your workshop deployment pipeline.
2. Confirm the source is **Test**, not Development.
3. Confirm Production is **your disposable lab Production workspace**.
4. Compare stages in the portal.
5. Because this is Production's first deployment, select **both `lh_workshop`
   and `nb_workshop`**. Do not select only the notebook into an empty target.
6. Explain that no customer data, capacity changes or permissions are involved.

**Optional Agent message**, not a terminal command:

```text
We are in lab 05 only. Present the PR/check/Test evidence and preview deploying
only lh_workshop and nb_workshop from Test to my lab Production stage.
Show the actual source/destination workspace names and IDs and selected items.
Do not execute until I say "approve production". Do not deploy from Dev.
After approval, track this operation to a terminal result with a bounded timeout.
Report failures or unresolved timeouts; do not submit a duplicate deployment.
Check the Production notebook binding before asking separate approval to run it.
Do not change permissions, capacity, Git connections or business logic.
```

**Checkpoint:** source is Test, destination is your lab Production, both items
are selected, and the evidence refers to the reviewed tax release. If Production
is unexpectedly populated, stop and inspect ownership/content before overwriting.

## 3. Approve and deploy

After review, type **approve production** in chat or give the presenter your
explicit approval if using the portal. Then:

Only give this approval after checking the preview. It approves this deployment,
not an unrestricted sequence of notebook runs or future promotions.

1. Execute Test -> Production, note `approved workshop release 1` if available.
2. Wait until the deployment operation succeeds.
3. Inspect operation details for both items.
4. In Production, open the **deployed** notebook, not a newly imported copy.
5. Confirm it says `RELEASE = "tax"`.

This approval is a workshop habit. It does **not** prevent another authorized
person from deploying through the portal/API. Enforced approvals, restricted
identities and GitHub environment protection are advanced follow-on work.

## 4. Verify Production independently

1. Inspect the default lakehouse. It must be Production's `lh_workshop`.
2. If a binding adjustment is needed, record it, save, and restart the session.
3. Confirm schemas are enabled and `dbo` exists.
4. Separately approve the run that overwrites Production's synthetic table.
5. Run all.
6. Verify the printed **Production** workspace and:

   ```text
   PASS: release=tax; rows=3; amount=350.00; amount_with_tax=385.00
   ```

7. Confirm the table contains Online 110.00, Store 220.00 and Partner 55.00
   in `amount_with_tax`.
8. Review deployment history and retain the release evidence without tokens.

If the notebook run fails, the release is not accepted even if deployment
succeeded. Inspect that run and its binding before an approved retry; do not
edit the expected totals or table rows to make the check pass.

## 5. Record the Production Checkpoint

1. Record the release SHA, approver, destination and approval decision.
2. Save the successful Test -> Production operation ID and both selected items.
3. Save Production's tax PASS line and printed workspace identity.
4. Confirm Dev and Test remain tax, and Test/Production remain disconnected
   from Git.

Keep resources until lab 06's explicit keep/remove decisions. This promotion
does not authorize cleanup or an automatic release workflow.

**Done when:** the approved Test -> Production operation succeeded and
Production's own persisted data passed all checks.

**If blocked:** keep the failed operation details and correct the cause before
an approved retry. Do not bypass Test by deploying directly from Dev, create a
second copy of the notebook, or alter the data to fake a passing result.

Next: [06 recovery and cleanup](./06-recovery-and-cleanup.md).
