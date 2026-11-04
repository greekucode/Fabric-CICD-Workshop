# GH8 - Practice a safe approval

**Time:** 10 minutes. **Starting point:** GH7, or any working local project.
**Goal:** practice pausing a change without touching credentials or real data.

## 1. Prepare the Disposable File

In your terminal, enter your cloned `Fabric-CICD-Workshop` repository, then run:

```text
git status --short
```

Save unrelated editor work and note the existing Git status as your baseline.
Do not discard earlier workshop changes. If Git says "not a git repository",
check your terminal location: the parent `Fabric` folder is not the workshop
repository. Run the Git checks inside your clone.

In VS Code Explorer, create
`ws-part1-github-copilot/labs/starter/output/approval-demo.txt` under your fork.
Enter this text and save the file yourself:

```text
KEEP THIS PRACTICE TEXT
```

This is disposable, ignored data. If the file already exists, inspect it first;
do not overwrite unrelated content.

## 2. Send the Ground Rules

Start a **new regular Agent chat**, not Ask mode or the tool-restricted reviewer.
A reviewer cannot demonstrate denying a write it never had permission to attempt.
Send each prompt below as a separate message and wait for its response.

The following prompt assumes you opened the workshop repository in VS Code.
If you opened a different folder, adjust only its file path before sending:

| VS Code Workspace Root | Path to Use in the Prompt |
| --- | --- |
| `Fabric-CICD-Workshop` | `ws-part1-github-copilot/labs/starter/output/approval-demo.txt` |
| Parent `Fabric` folder | `Fabric-CICD-Workshop/ws-part1-github-copilot/labs/starter/output/approval-demo.txt` |
| `ws-part1-github-copilot` | `labs/starter/output/approval-demo.txt` |

**Message 1 - ground rules:**

```text
For this exercise, use read-only checks first.

Before overwriting or deleting anything, show the exact path and proposed
change, then wait for my explicit approval.

Never inspect credentials. Work only on this disposable file:
ws-part1-github-copilot/labs/starter/output/approval-demo.txt

Do not change any other files.
```

**Expected:** the agent acknowledges the boundaries without changing any files.

## 3. Request a Proposal Only

**Message 2 - inspect and propose:**

```text
Inspect only the disposable file named above.

Propose replacing its content with:
Replacement report

Show the exact file path and proposed content, then stop and wait for
my approval. Do not write anything yet.
```

**Expected:** the agent reads only the practice file, shows its current content
and the proposed replacement, then stops. No write should occur.

## 4. Deny the Change

After the agent pauses, send **Message 3 - denial:**

```text
No. Keep the existing file unchanged. Do not overwrite or delete it.
Do not make any other changes.
```

**Expected:** the agent acknowledges your denial and does not write anything.
No tool approval dialog is required for this exercise: a conversational pause
and your explicit denial are sufficient. If a tool approval dialog appears
before you can reply, deny it as well. Do not enable automatic approval or
broader permissions to complete the exercise.

## 5. Verify the Result Yourself

Open the saved practice file directly in the editor. It must still contain:

```text
KEEP THIS PRACTICE TEXT
```

In your workshop repository's terminal, run:

```text
git status --short
git diff
```

Compare with your starting baseline. There should be no new tracked changes
from this exercise; pre-existing changes may still appear.

The starter ignores `output/`, so a clean `git diff` alone cannot prove this
exercise passed. Inspect the saved file content directly after denial; do not
rely on the assistant saying it kept the file. If the agent cannot read ignored
files, explicitly attach only this practice file or demonstrate the pause with
the presenter; do not enable broad access to ignored folders.

If the assistant writes before approval, record that as a failed exercise,
stop the action and manually restore only this disposable file's practice text.
Do not treat another instruction as a guarantee of enforcement.

**Discussion:** instructions guide behavior; tool permissions and approval
settings constrain it. Never test secret handling by asking for a real token.

## 6. Clean Up

After verification, delete only `approval-demo.txt` from the starter `output/`
folder using Explorer if desired. Do not delete the whole output folder or
revert other workshop work. No commit or pull request is required for this lab.

**Done when:** the agent paused before writing, respected your denial, and you
verified the saved practice text and compared Git status with your baseline.
Restoring the text after an unauthorized write does not turn a failed exercise
into a pass.

Next: [GH9 capstone](./09-capstone.md).
