# Python Environment

All Python commands must run inside the conda environment `torch_py310`.

Rules:
- Never use system Python.
- Always execute Python using:
  conda run -n torch_py310 python

Python version: 3.10
Primary ML framework: PyTorch

# Others

Always respond in Chinese-simplified

# Skills

Before answering a task, check whether any local skill under ~/.agents is relevant.

Local skills are stored as:

~/.agents/<skill-name>/SKILL.md

When a user request matches a skill's "When to use" section, read and follow that SKILL.md before answering.