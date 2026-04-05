# Contributing to HRBot

Thank you for your interest in contributing to HRBot! 🎉

All contributions — bug reports, feature requests, documentation improvements, and code — are welcome.

---

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Features](#suggesting-features)
  - [Submitting a Pull Request](#submitting-a-pull-request)
- [Development Setup](#development-setup)
- [Commit Message Convention](#commit-message-convention)
- [Code Style](#code-style)

---

## Code of Conduct

By participating in this project you agree to be respectful, inclusive, and constructive. Harassment, discrimination, or personal attacks of any kind will not be tolerated.

---

## Getting Started

1. **Fork** the repository on GitHub.
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/<your-username>/HR-chatbot.git
   cd HR-chatbot
   ```
3. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

---

## How to Contribute

### Reporting Bugs

Before filing a bug report, search [existing issues](https://github.com/K-vino/HR-chatbot/issues) to avoid duplicates.

When reporting a bug, please include:
- A clear and descriptive title
- Steps to reproduce the problem
- Expected vs. actual behaviour
- Your Python version and OS
- Any relevant error messages or stack traces

### Suggesting Features

Open a [GitHub Issue](https://github.com/K-vino/HR-chatbot/issues) with the label `enhancement`. Include:
- The problem your feature solves
- A description of the proposed solution
- Any alternative approaches you considered

### Submitting a Pull Request

1. Create a new branch from `main`:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/bug-description
   ```
2. Make your changes, keeping commits small and focused.
3. Test your changes manually by running `streamlit run app.py`.
4. Push your branch and open a Pull Request against `main`.
5. Fill in the PR template, describing *what* changed and *why*.

A maintainer will review your PR and may request changes. Please be patient and responsive to feedback.

---

## Development Setup

```bash
# Install all dependencies
pip install -r requirements.txt

# Run the app locally
streamlit run app.py

# (Optional) Run with a specific model
# Edit config.py → DEFAULT_LLM before running
```

---

## Commit Message Convention

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
feat:     A new feature
fix:      A bug fix
docs:     Documentation changes only
style:    Formatting, missing semicolons, etc. (no logic change)
refactor: Code restructuring without feature changes
test:     Adding or updating tests
chore:    Maintenance tasks (dependency updates, CI config)
```

**Examples:**
```
feat: add DOCX document ingestion support
fix: handle empty PDF pages gracefully
docs: update installation steps for Windows
```

---

## Code Style

- Follow [PEP 8](https://peps.python.org/pep-0008/) for Python code.
- Use descriptive variable and function names.
- Add docstrings to all public functions (Google-style preferred).
- Keep functions short and single-purpose.
- Do not commit secrets, API keys, or personal data.

---

Thank you for helping make HRBot better! 🚀
