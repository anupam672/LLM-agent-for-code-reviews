# LLM-Based Autonomous Code Review Agent

An autonomous AI agent designed to streamline and automate the code review workflow. Built utilizing [crewAI](https://www.crewai.io/) and [LangChain](https://www.langchain.com/), this project integrates intelligent code analysis with automated review documentation.

## Features

- **Automated Directory Traversal:** Intelligently fetches and navigates repository tree structures using the GitHub API to identify all constituent files.
- **Content Streaming:** Automatically accesses file contents programmatically for subsequent analysis.
- **AI-Powered Code Review:** Utilizes advanced LLMs to independently review Python code, highlight issues, and propose corrections securely.
- **Automated Documentation Logging:** Syncs directly with Notion via its API to generate structured code review reports instantly, maintaining an audit trail for developers.

## Tech Stack

- **Frameworks:** crewAI, LangChain
- **APIs:** GitHub REST API, Notion API, OpenAI API
- **Environment:** Python, Jupyter Notebooks

## Architecture

1. **Repository Setup:** The agent extracts the working tree of the provided GitHub repository and builds paths for file interaction.
2. **File Processing:** It fetches source code utilizing authentication tokens.
3. **LLM Evaluation:** Passes file contents to the LLM agent to review variables, logic, and efficiency.
4. **Report Generation:** Connects to the Notion document to append formal reviews and suggestions directly into developer workspaces.

## Getting Started

### Prerequisites

- Python 3.9+ or Anaconda
- OpenAI API Key
- GitHub Personal Access Token (PAT)
- Notion API Key

### Installation & Execution

1. Clone this repository.
2. Create a `constants.py` file in the root directory and define the following variables:

```python
OPENAI_API_KEY = "your_openai_key"
GITHUB_SECRET_KEY = "your_github_pat"
NOTION_API_KEY = "your_notion_key"
```

3. Launch Jupyter Notebook (`jupyter notebook`) and execute the `.ipynb` files to instantiate the AI agent and begin reviewing code.
