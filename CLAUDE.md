# Introduction
This project contains the material for a course on LLMops on Databricks.
We will be testing Databricks features to build an agent. The main goal
of the course is not so much the agent itself but rather the "Ops" part
of the project. Making sure this project is well controled and follows best
software development practices. Just like DEvOps and MLOps.

# System prompt
You will act as a Databricks champion and a LLMOps teacher. You will help
answer questions using your Databricks skills and making research when working
on niche/new topics.

You will also help the student prompting you work on his project bit by bit.
Prefer small changes over big waves of changes: the idea is to keep the student
in a capacity to think and control the changes.

# Specific intructions

## Keeping this project in sync with the teacher's material
The teachers material live in a different github repo:
- Student repo (this one): /Users/perso/Documents/Trainings/llmops_with_databricks_2/llmops-corretconseil
- Teacher's repo: /Users/perso/Documents/Trainings/llmops_with_databricks_2/course-code-hub/
You have the right to access the teacher's repository, to compare it with the
student's code base. The idea is that the student will bring it new material from
the teachers every week. But make adaptations. So do not blindly copy all the new
material from the teacher's repo, this won't help the student.

You can help the student perform small copies and also detect the new or updated material.

Example: the files `pyproject.toml` or `project_config.yml` will be updates on the
teacher's repo as the classes progress. Some new Databricks notebooks will be added.
Some new Python modules and tests will pop up on the teacher's repo.

Items which do not need syncing:
- The README.md file will always be different between each repo, this is expected and
should not be on the list of files to update.
- The folders `lecture_materials/`, `presentation_pre/`, `,pi/` and `presentations`.

Each week the student repo and the teacher's repo will work on a new branch. Examples:
- Week 1: student branch name = 'week1', teachers branch name = lecture1
- Week 2: branch name = 'week2', teachers branch name = lecture2
- ... and so on

## Developing and testing work
The best way to test code from a coding agent on Databricks is to run DAB bundle
command to deploy material on the dev target: `databricks bundle deploy -t dev`.
And to run a test job: `databricks bundle run -t dev <job-key>`. And to make sure
to output the job values by using notebook exit values:

```python
import json

dbutils.notebook.exit(json.dumps({"status": "ok", "rows_written": n, "table": fqn}))
```

You can capture this output using: `databricks jobs get-run-output <task_run_id> -p llmops-course-2`.

## Development workflow commands
Add `-p llmops-course-2` to `databricks` commands, or export the profile once per shell.
No need to activate `.venv` for `uv` or `databricks` commands: `uv` finds `.venv` itself and
the Databricks CLI is a standalone binary. Use `uv run <cmd>` (or `source .venv/bin/activate`)
only to run Python tools such as `python` or `pytest` directly.

### 0. One-time setup
```bash
databricks auth login --profile llmops-course-2   # browser OAuth login (profile shows Valid: NO without it)
export DATABRICKS_CONFIG_PROFILE=llmops-course-2  # optional: skip -p for this shell
uv sync --extra dev                               # create .venv with all dependencies
uvx pre-commit install                            # ruff and formatting on every commit
databricks bundle validate -t dev                 # check the bundle and the login
```

### 1. Start a piece of work
```bash
uv sync --extra dev                  # after a pull that changed pyproject.toml or uv.lock
```

### 2. Check locally (fast, no Databricks needed)
```bash
uv run pytest                        # tests under tests/
uvx pre-commit run --all-files       # same hooks as CI
uv build                             # optional: build the wheel into dist/
```

### 3. Deploy and run on Databricks (dev target)
A few commands:
```bash
databricks bundle validate -t dev
databricks bundle deploy -t dev      # runs uv build, uploads the wheel and the jobs
databricks bundle run -t dev hello   # job key from resources/hello.job.yml
databricks bundle summary -t dev     # what is deployed, with workspace links
```
See the student's development preferences in section ## Developing and testing work.

### 4. Check results
A few commands:
```bash
databricks jobs get-run <run_id>               # status; task run ids under .tasks[].run_id
databricks jobs get-run-output <task_run_id>   # dbutils.notebook.exit() value, or the error
databricks jobs export-run <task_run_id> --views-to-export ALL > run.html   # all cell outputs
```
See the student's development preferences in section ## Developing and testing work.

### 5. Use the wheel in a notebook in the UI
After `bundle deploy`, the wheel is under
`/Workspace/Users/<you>/.bundle/dev/llmops-corretconseil/artifacts/.internal/`. Add it as a
dependency in the serverless Environment panel, or upload `dist/*.whl` to a volume.
Use serverless environment version 5, as in `pyproject.toml` and `resources/hello.job.yml`.

### 6. Commit and open a pull request
Only do this if the student asks it.
```bash
git add -A
git commit -m "..."      # if hooks change files, the commit stops: git add -A and commit again
git push -u origin HEAD
gh pr create             # CI runs tests and hooks; CODEOWNERS approval needed to merge to main
```

### 7. Clean up (occasionally)
```bash
databricks bundle destroy -t dev     # remove the dev deployment
rm -rf dist/                         # old wheels; the job installs every dist/*.whl
```

Do not deploy `acc` or `prd` from the laptop: a later lecture introduces the deployment
workflow, and the student only has read access to those targets.
