# SREGym Skills

Shared, agent-neutral workflows for work on [SREGym](https://github.com/SREGym/SREGym).

The Markdown files are the source instructions. No agent-specific installer, configuration, or command syntax is required.

## Available skills

| Skill | Purpose |
| --- | --- |
| [SREGym Fault Engineering](skills/sregym-fault-engineering/SKILL.md) | Create, review, audit, test, harden, and release SREGym faults. |

## Use with any agent

Point your preferred agent to this repository and name the skill and task. For example:

```text
Use the sregym-fault-engineering skill from
https://github.com/SREGym/sregym-skills.
Read its SKILL.md and the references relevant to my task.
Review this SREGym fault PR: <PR URL>.
Use my selected SREGym checkout. Keep the review read-only.
Report the evidence and any checks that you cannot complete.
```

The agent can read the files directly or adapt them to its supported instruction format.
The safety boundaries and evidence requirements remain the same after adaptation.

For agents that read this repository:

1. Read the selected `SKILL.md` before work on the task.
2. Read the references that apply to the requested mode.
3. Use equivalent tools available in your environment.
4. Identify the SREGym checkout selected by the user. Do not assume a home directory or machine name.
5. Respect the user's scope and permissions. These instructions do not authorize live mutations or publication.
6. If a required tool, permission, or target is unavailable, report the gap.
7. Change local agent configuration only when the user requests it.

Each skill keeps its helper scripts and references in the same directory.
The relative paths inside a skill refer to that directory unless the text states otherwise.
SREGym source paths refer to the selected SREGym checkout.

## Optional context helper

The fault-engineering skill includes a read-only helper that finds related code, tests, and notes.
It requires Python 3.9 or newer and [ripgrep](https://github.com/BurntSushi/ripgrep).
Git is optional and supplies the branch name when available.

From this repository, an example with a sibling SREGym checkout is:

```bash
python3 skills/sregym-fault-engineering/scripts/collect_fault_context.py \
  node_conntrack_exhaustion_hotel_reservation --repo ../SREGym
```

Use `--repo` for another checkout location.
If the working directory is inside a SREGym checkout, the helper finds its root without `--repo`.
The helper does not connect to a cluster or change repository files.

## Testing and records

The skills use `notes.mo/` inside the selected SREGym checkout for review and test records.
Create the required directories when the task permits file writes.
If the user selects another record location, use that location instead.
Do not copy private credentials or access configuration into this repository or into test notes.

To test the context helper from this repository:

```bash
python3 -m unittest discover -s tests -v
```
