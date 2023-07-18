# AI Products Backend

Tools Used:
a. LangChain - to connect different components in a LLM Chain
b. Pinecone - Vector Database
c. Flask - Web Framework for Python

## Requirements

- Python Version >= 3.10

## Installation

### Python

The 1st thing you need is Python whose version is >= 3.10.

Easiest way is to install directly on your terminal using System Package Managers:

- Linux - `apt`, `apt-get`, `yum`
- Mac - `homebrew`

But ideal & recommended way is via [pyenv](https://github.com/pyenv/pyenv).

It helps you manage multiple versions of python on your system effectively. Install it as explained in pyenv docs.

Once pyenv is installed, install & select python version

```bash
pyenv install 3.10.12
pyenv local 3.10.12
```

### Python Virtual Environment

Use `python venv` to manage [Python Virtual Environments](https://realpython.com/python-virtual-environments-a-primer/)

- Create a new environment

```bash
python -m venv venv
```

- Activate Python environment

```bash
source venv/bin/activate
```

### Python Packages

```bash
python -m pip install -r requirments.txt
```

## Running the App

- 1st Configure your `.env` file. Copy `.env.sample` to `.env` file & fill your env values there

- Run Command

```bash
python index_server.py
```
