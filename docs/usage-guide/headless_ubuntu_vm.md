# Using Instagrapi in a Headless Ubuntu VM

This guide explains how to install and run **instagrapi** inside a terminal-only Ubuntu virtual machine.
It includes scripts for session persistence, challenge resolution and proxy configuration.

## Prerequisites

- Python 3.9 or newer
- `git` and `pip`

```bash
sudo apt update
sudo apt install python3.9 python3.9-venv python3.9-pip git
```

Create and activate a virtual environment:

```bash
python3 -m venv instagrapi_env
source instagrapi_env/bin/activate
pip install --upgrade pip
```

Install instagrapi from PyPI:

```bash
pip install instagrapi
```

## Example Scripts

Several example scripts are available in `examples/headless_vm`:

 - `login_example.py` – simple login and account information test
- `session_manager.py` – saves and loads sessions to reduce login challenges
- `challenge_handler.py` – demonstrates automated email code retrieval
- `proxy_config.py` – helper class with proxy and rate limiting support
- `instagram_automation.py` – complete automation framework

Copy `.env.example` to `.env` and fill in your credentials, then run:

```bash
source .env && python3 examples/headless_vm/instagram_automation.py
```
