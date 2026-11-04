# GH0 - Compare Copilot surfaces

**Time:** 5 minutes within the orientation. **Starting point:** the presenter
opens the [starter script](./starter/summarize.py); attendees can observe before setup.

Use an ordinary code editor tab, not a rendered Markdown preview. Before GH3 the
loader is called `load`; after the rename it is `load_rows`. If you already did
setup, use `ws-part1-github-copilot/labs/starter/summarize.py` in your own fork.
Do not open the presenter solution with the same filename.

1. Walk thru overall VSCode tool
    - models selection, settings, etc
1. Select `load` in the editor and use inline chat:

   **Prompt:** Explain this function in two sentences. Do not edit anything.

1. Ask the Chat view, with the script attached:

   **Prompt:** Explain how this program reads a CSV and prints a report. Do not edit anything.

1. If available, ask the CLI or github.com Chat the same question with the same file context.
1. Compare: did the answer use the selected function, the file, or the whole repository?

To attach context in VS Code Chat, use **Add Context** (the paperclip or `+`)
and select the file, or drag its Explorer entry into Chat. Confirm the file
appears as an attachment before sending. Inline chat can be opened from the
selection's context menu. UI names and shortcuts vary by version.

**Expected explanation:** the loader opens a UTF-8 CSV, accepts an optional byte
order mark, and returns a list of dictionaries using the header as keys. It does
not yet validate the business rules. If a surface cannot access the local file,
paste this synthetic function explicitly; do not assume github.com or a CLI in
another folder can see the editor selection.

**Done when:** you can name a surface for a focused code edit and a surface for
a multi-file task. No code changes are required.

**If blocked:** watch the presenter; CLI and github.com can wait until GH6/GH7.
Next: [GH1 access](./01-access.md).

## Practice: Copilot Chat Symbols

Use these symbols to make your request more specific. Type a symbol and select
an available suggestion; options vary by VS Code version, installed extensions,
and chat mode. Use **Ask mode** for these learning exercises. This practice is
optional and can be revisited after setup.

### `@` - Choose a Specialist

Use `@` when you want to direct your question to a particular chat participant.
It helps distinguish questions about your project, terminal commands, or VS Code
itself. It does not automatically attach every relevant file.

| Use Case | Example Prompt | What You Learn |
| --- | --- | --- |
| Understand the workshop | `@workspace Compare the goals and prerequisites of Part 1 and Part 2 in Fabric-CICD-Workshop.` | How the Copilot exercises connect to Fabric CI/CD. |
| Get terminal guidance | `@terminal What Bash commands activate a Python virtual environment and run pytest from the Part 1 labs/starter folder? Explain without running them.` | How to prepare and test the starter project. |
| Configure the editor | `@vscode How do I select the Python interpreter from this project's virtual environment?` | How to make the editor use the correct Python environment. |

### `/` - Choose an Action

Use `/` for a predefined command, such as explaining code, suggesting a fix, or
generating tests. Select or attach the relevant code first so the action has a
clear target. Slash commands can also include extension-provided commands and
custom prompts. Only use commands that appear in your suggestions.

Open the [starter script](./starter/summarize.py) and select the relevant function.
Use `load_rows` instead of `load` if you have already completed the GH3 rename.

| Use Case | Example Prompt | What You Learn |
| --- | --- | --- |
| Explain CSV loading | `/explain Explain the selected load function in two sentences. Why does it use utf-8-sig? Do not edit anything.` | How CSV loading handles a byte order mark. |
| Investigate empty input | `/fix The selected summarize function divides by zero when rows is empty. Suggest a minimal fix without applying it.` | How to diagnose an edge case in the original starter. |
| Explore test coverage | `/tests Suggest pytest tests for summarize covering repeated regions, decimal amounts, and empty input. Show code without editing files.` | How to cover normal behavior and failure cases. |

### `#` - Provide Context

Use `#` to explicitly reference information Copilot should consider, such as a
file, an editor selection, or the codebase. This is especially useful when several
files have similar names or when "this function" would otherwise be ambiguous.
Depending on your setup, `#` can also expose tools.

Select each context entry from the suggestions before sending. For file context,
choose the script under `labs/starter`, not the presenter solution.

| Use Case | Context and Example Prompt | What You Learn |
| --- | --- | --- |
| Understand one file | Choose `#file`, attach the starter script, then ask: `Explain how this script reads a CSV and prints a report. Do not edit anything.` | How to ground the answer in one specific file. |
| Check selected logic | Highlight `summarize`, add `#selection`, then ask: `Does the average calculation match the printed label "Average per region"? Explain with a small example.` | How to check whether the original starter's calculation matches its output label. |
| Find workshop guidance | Add `#codebase`, then ask: `Within Fabric-CICD-Workshop, find the Part 2 guidance for validating changes before deployment. Reference the relevant files.` | How to find guidance across multiple files. |

**Remember:** `@` chooses a helper, `/` chooses an action, and `#` supplies context
or references a tool.

**If unavailable:** ask the same question in ordinary language and attach the
relevant file using **Add Context**. These examples are for VS Code Chat; terminal
shells, Copilot CLI, and github.com Chat have different commands and capabilities.
