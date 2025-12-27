# Vibe-Code System

An intelligent agentic system that automatically plans, architects, and implements complete engineering projects from natural language prompts. Uses LangGraph agents with OpenAI or Groq APIs to generate full project structures with working code.

## Features

- **Natural Language to Code**: Describe your project in plain English, get working code
- **Multi-Agent System**: Coordinated agents for planning, architecture, and coding
- **Multiple LLM Providers**: Support for both OpenAI (GPT-4) and Groq APIs
- **Automatic Project Structure**: Creates organized project folders with timestamps
- **Intelligent Task Breakdown**: Breaks complex projects into manageable implementation steps
- **File Management**: Built-in tools for reading, writing, and organizing project files
- **Sandboxed Execution**: All projects generated in isolated folders for safety

# Coder Buddy

**Coder Buddy** is an AI-powered coding assistant built with [LangGraph](https://github.com/langchain-ai/langgraph).  
- It works like a multi-agent development team that can take a natural language request and transform it into a complete, working project file by file using real developer workflows.

## Architecture

- **Planner Agent** : Analyzes request and generates a detailed project plan.
- **Architect Agent** : Breaks down the plan into specific engineering tasks with explicit context for each file.
- **Coder Agent** : Implements each task, writes directly into files, and uses available tools like a real developer.

<div style="text-align: center;">
    <img src="resources/coder_buddy_diagram.png" alt="Coder Agent Architecture" width="90%"/>
</div>

## Getting Started
### Prerequisites
- Make sure you have uv installed, follow the instructions [here](https://docs.astral.sh/uv/getting-started/installation/) to install it.
- Ensure that you have created a groq account and have your API key ready. Create an API key [here](https://console.groq.com/keys).

## Project Structure

```
ai-project-planner/
├── agent/
│   ├── __init__.py
│   ├── graph.py          # Main agent graph and workflow
│   ├── prompts.py        # Agent prompts and instructions
│   ├── states.py         # Pydantic models for state management
│   └── tools.py          # File management tools
├── main.py               # Entry point - RUN THIS FILE
├── requirements.txt      # Python dependencies
├── .env                 # API keys 
├── uv.lock              # Dependency lock file 
└── README.md           
```

### Example Prompts
- Create a to-do list web app using html, css, and javascript.
- Create a simple calculator web app using html, css, and javascript.
- Create a simple blog API in FastAPI.
- Create an Expense Tracker web app in HTML, CSS, and JavaScript


## Architecture

```
User Prompt → Planner → Architect → Coder → Generated Project
```

## Installation

### Step 1: Install Dependencies with uv 

[uv](https://docs.astral.sh/uv/) is a fast Python package manager that creates isolated environments and manages dependencies efficiently.

```bash
# Sync dependencies - this creates a virtual environment and installs everything
uv sync
```

This will:
- Create a `.venv` virtual environment in your project
- Install all dependencies from `pyproject.toml` or `requirements.txt`
- Create a `uv.lock` file to lock dependency versions
- Set up your development environment

### Alternative: Install with pip

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/Scripts/activate

# Install dependencies
pip install -r requirements.txt
```

## Troubleshooting

### API Key Issues

**Problem**: `No API key found` error

**Solution**:
```bash
# Check your .env file exists and has correct format
cat .env

# Ensure no spaces around the = sign
OPENAI_API_KEY=sk-your-key-here  
OPENAI_API_KEY = sk-your-key-here  
```

### Import Errors

**Problem**: `ModuleNotFoundError: No module named 'langchain'`

**Solution**:
```bash
# With uv
uv sync

# With pip
source .venv/Scripts/activate  # Activate venv first
pip install -r requirements.txt
```