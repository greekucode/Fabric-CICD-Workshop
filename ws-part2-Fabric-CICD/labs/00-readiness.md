# 00 - Get ready and copy the starter

**Time:** 20 minutes after installations and sign-in.
**Goal:** start with working materials and disposable resource names.
**Starting point:** GitHub Copilot access and a Fabric account.

## 1. Confirm access before the session

Before creating anything, send this checklist to the presenter/admin and record
which requirements are confirmed:

- You can create a private GitHub repository and run GitHub Actions in it.
- Your Fabric capacity is assigned, active and supports the workshop features.
- Fabric tenant settings allow workspace/item creation, Git synchronization,
  and specifically GitHub synchronization.
- You can be workspace Admin on your own four workshop workspaces.
- You can create a deployment pipeline and assign its stage workspaces.
  Deployment requires pipeline Admin and Contributor or higher in both workspaces.
- The tenant supports Git/deployment of Lakehouse and Notebook items.

Do not enable service principals or create app registrations: the core labs use
your interactive identity. No Azure resource or new capacity is required.
Required reviewers and branch protection in private repositories depend on your
GitHub plan. If unavailable, manually check CI before merging; do not describe
that fallback as enforced protection.

**Expected:** access to an existing capacity and permission for the four
disposable workspaces, one pipeline and one private attendee repository.
If any requirement is unresolved, stop the cloud setup and ask the organizer.

## 2. Check tools

Install VS Code, Python 3.10+, Git and GitHub CLI using your organization's
approved process. Fabric CLI is useful for Copilot-driven operations but the
portal path works without it. Azure CLI is optional.

Open a **local terminal** in VS Code. Run each command separately:

```text
python --version
git --version
gh --version
gh auth status
```

On macOS/WSL, use `python3` until your virtual environment is active.
Sign in with `gh auth login` if needed. If using Fabric CLI, run `fab --version`,
then `fab auth login`. Enter credentials yourself in the approved login flow.

After signing in, run `gh auth status` again. Confirm the intended GitHub
account is shown; never paste its credentials or token into Copilot Chat.
These commands check tools and sign-in, not Fabric workspace permissions.

In WSL, keep the repository and Python environment inside WSL. For a Fabric
login diagnostic, bound it with `timeout 20s fab auth status`. If login hangs,
stop and check DNS for `login.microsoftonline.com`; a GSA synthetic `6.6.x.x`
address can be unreachable from WSL. Ask the presenter/IT for the approved DNS
fix rather than repeatedly retrying or changing network settings blindly.

## 3. Copy only the starter

1. Make a **new, empty folder outside these materials**, such as `fabric-cicd-workshop-lee01`.
2. Copy the contents of [starter](./starter/), including `.gitignore`, into it.
3. Open that new folder in VS Code.
4. Do not copy the enclosing starter directory or the presenter folder.
5. In a terminal, confirm you see `notebooks`, `checks`, `data`, `fabric`,
   `tests`, `prepare_release.py` and `release.json`.

Use the file manager with hidden files visible so `.gitignore` is included.
Do not copy a `.git` directory, Part 1's sales application, or a previous
attendee's configuration. If the destination is not empty, choose another
folder rather than approving a bulk overwrite.

**Checkpoint:** VS Code Explorer shows `prepare_release.py` directly at the
opened folder's root, not inside an extra `starter` subfolder. All following
local commands run from this attendee root, not the materials repository.

Create and activate a virtual environment:

### Windows PowerShell

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If activation is blocked, do not relax execution policy; use
`.\.venv\Scripts\python.exe` instead of `python` in all subsequent commands.

### macOS / WSL / Ubuntu

```bash
python3 -m venv .venv
source .venv/bin/activate
```

No pip install is necessary. Everything local uses Python's standard library.
Select the environment with **Python: Select Interpreter** if the extension is installed.

Verify the interpreter in the same terminal:

```text
python -c "import sys; print(sys.executable)"
```

**Expected:** a path inside the attendee folder's `.venv`. Keep this environment
active for the local checks in labs 00-06. Reopening a terminal may require
activating it again.

## 4. Run the prebuilt checks

```text
python -m unittest discover -s tests -v
python checks/validate_items.py
```

Expected: **12 tests pass**, followed by:

```text
PASS: starter baseline; no synced Fabric items yet (setup only)
```

This is intentionally **not** release readiness. After the first Fabric sync,
the stricter command `python checks/validate_items.py --require-items` must pass.
Do not remove that switch from CI to hide a missing sync.

If either command fails, stop and check the folder and interpreter first.
Do not rewrite tests or fabricate Fabric item folders to make this gate pass.

## 5. Choose unique names

Use your own suffix, for example `lee01`. The item names stay fixed:

| Resource | Example |
| --- | --- |
| Private GitHub repository | `<owner>/fabric-cicd-workshop-lee01` |
| Development | `wk-dev-lee01` |
| Developer branch workspace | `wk-dev-a-lee01` |
| Test | `wk-test-lee01` |
| Production (lab only) | `wk-prod-lee01` |
| Deployment pipeline | `wk-pipeline-lee01` |
| Lakehouse / notebook | `lh_workshop` / `nb_workshop` |
| Feature branch / Git directory | `feature/sales-tax` / `/fabric` |

1. Choose one suffix and use it consistently for every resource.
2. In VS Code Explorer, copy `workshop-config.example.json` to
  `workshop-config.local.json` in the same attendee root.
3. Open the copy and fill in your owner, repository and resource names using
  its existing fields. Do not invent IDs for resources not created yet.
4. Save it and check the names against the table above.

It is an ignored **human/Copilot reference**, not an executable
deployment configuration. Do not put credentials in either file.
If a resource name exists, choose another suffix; never delete someone else's resource.

## 6. Set Copilot's boundaries

Start a new **regular Agent chat in VS Code**, with the attendee folder open.
Alternatively, start standalone `copilot` from that folder. Send this as a
**chat message**, not a terminal command:

```text
We are doing only the current Fabric CI/CD lab. Use my
workshop-config.local.json for names, but never read credential files.
Inspect state first. Before creates, commits, pushes, syncs, overwrites,
deployments, permission changes or deletion, show the exact scope and wait
for my approval. Never print tokens. Do not create a capacity, service principal
or an automated release workflow. Do not complete future labs early.

For lab 00, check only the local folder layout, interpreter and starter tests.
Report which access prerequisites still need my confirmation. Do not create
resources, initialize Git, commit, push or connect a workspace yet.
```

**Expected response:** local readiness results and unresolved access questions,
not resource creation. The portal path works without a Fabric MCP server.
If Copilot lacks a tool, perform the corresponding portal step yourself after
review; do not treat an unexecuted suggestion as a completed operation.

## 7. Record the Readiness Checkpoint

Before moving on, confirm all four statements:

1. The attendee folder is separate from the workshop materials.
2. Its virtual environment is selected, all 12 tests pass, and the setup-only
  validation message is present.
3. Your private-repository and Fabric access requirements are confirmed.
4. Unique resource names are saved in the local config, without credentials.

There are no cloud resources to clean up yet. Keep the starter and environment
for lab 01; do not delete the workshop materials.

**Done when:** tools work, all starter tests pass, access is confirmed and your
unique names are recorded.

**If blocked:** you can run local tests, but do not claim the Fabric labs are
complete. Use the presenter's disposable environment for demonstrations only.

Next: [01 baseline](./01-baseline.md).
