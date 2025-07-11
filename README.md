---
title: Template Final Assignment
emoji: 🕵🏻‍♂️
colorFrom: indigo
colorTo: indigo
sdk: gradio
sdk_version: 5.25.2
app_file: app.py
pinned: false
hf_oauth: true
# optional, default duration is 8 hours/480 minutes. Max duration is 30 days/43200 minutes.
hf_oauth_expiration_minutes: 480
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference



# step by step
1. Develop the app locally by clone the repo, for example:
```bash
git clone https://huggingface.co/spaces/CoralLeiCN/agent_course_final_assignment
cd agent_course_final_assignment
```
NOTE: if the space is private, you need to use `git clone https://{username}:{token}@huggingface.co ....` instead

2. sync the repo to github (optional)
```bash
git remote set-url origin https://github.com/CoralLeiCN/agent_course_final_assignment.git
```
Github guide on [Adding a local repository to GitHub using Git](https://docs.github.com/en/migrations/importing-source-code/using-the-command-line-to-import-source-code/adding-locally-hosted-code-to-github#adding-a-local-repository-to-github-using-git)

3. Create and activate Python environment by uv
```bash
uv venv
source .venv/bin/activate
```

4. (optional) As we are running the app outside of a Space environment, we need to logged in to Huggingface
```bash
huggingface-cli login

5. run the app locally
```bash
uv run app.py
# Or Automatically reloads the Gradio app
uv run gradio app.py
```

# experiments
| Features | Model | Score (out of 20) | Notes |
| --- | --- | --- | --- |
| Directly call LLM with questions | gemini-flash 2.0 | 1 | direct call |
| + Structured Output: Response Format | gemini-flash 2.0 | 3 |  |
| + system prompt from GAIA, slightly modified | gemini-flash 2.0 | 3 |  |
| + Agentic LLM with Smolagent & Add “Understand video” tool using gemini-flash. | gemini-flash 2.0 | 1-4 | Results varied due to `Codeagent` output formatting issues. |
| + WebSearch tool | gemini-flash 2.0 | 7 | Greatly improved, still has formatting issues |
| + Change model | gemini-flash 2.5 | 7 |  |
| + VisitWebpageTool | gemini-flash 2.5 | 10-12 | cannot see image, mp3, excel file. |
| + DownloadFile & ReadExcelFileBytes | gemini-flash 2.5 | 13 |  |
|  |  |  |  |


# Developer
## Install pre-commit
```bash
uv run pre-commit install
```