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



# Step by step
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

6. After run, sync the repo back to huggingface Space
```bash
git remote set-url origin https://huggingface.co/spaces/CoralLeiCN/agent_course_final_assignment
```
# experiments
The score is max score after a few runs
| Features | Model | Score (out of 20) | Notes |
| --- | --- | --- | --- |
| Prompted LLM | gemini-flash 2.0 | 1 | Format could be wrong |
| + Structured Output | gemini-flash 2.0 | 3 |  |
| + System prompt from GAIA (slightly modified) | gemini-flash 2.0 | 3 |  |
| + AI Agent by smolagent & "Understand Video" Tool | gemini-flash 2.0 | 4 | Results varied due to Code-Agent output formatting issues. |
| + WebSearchTool | gemini-flash 2.0 | 7 | Greatly improved, but still has formatting issues. |
| + Change from flash 2.0 to flash 2.5 | gemini-flash 2.5 | 7 |  |
| + VisitWebpageTool | gemini-flash 2.5 | 10-12 | Cannot see image, mp3, excel file. |
| + DownloadFile & ReadExcelFileBytes | gemini-flash 2.5 | 13 |  |
| + TranscribeAudioBytes | gemini-flash 2.5 | 14 |  |
| + CodeExecutionTool | gemini-flash 2.5 | 14 |  |
| + WikipediaSearchTool (customised using wikipedia + markdownify) | gemini-flash 2.5 | 15 | Tested both WikipediaRetriever and WikipediaLoader from LangChain, but their performance was bad as they omit table data, which can contain key information. |
| + Increase thinking budget, edited system prompt & Set temperature to 0 for consistency | gemini-flash 2.5 | 15-17 | Stability is the key challenge.  Can achieve a score of 17 with the GAIA score function, but this assignment uses an exact match, so the formatter needs improvement. |
| + Chess Best Move Tool & Upgraded Image Understanding Model | gemini-flash 2.5 gemini-pro 2.5 | 18 | Chess tool is from a Hugging Face Space. The conversion of digital chessboard images to FEN strings is unstable by Gemini Pro.  |
| + Gemini pro with Grounding_tool (GoogleSearch) for baseball questions | gemini-flash 2.5 gemini-pro 2.5 | 19 | One question could not be solved by Flash with Duckduckgo |
| / | gemini-flash 2.5 gemini-pro 2.5 | 20 | Many Many runs to achieve 20. |

# Developer
## Install pre-commit
```bash
uv run pre-commit install
```

## export requirements.txt
```bash
uv export --format requirements-txt --no-dev --no-hashes --output-file requirements.txt
```