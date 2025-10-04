# Vector 🕵️‍♂️
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Profile views](https://komarev.com/ghpvc/?username=thesaderror&color=brightgreen)

![Vector Logo](https://media.discordapp.net/attachments/1028720953515057162/1028914619219181609/vector.png)

**Vector** is a lightweight OSINT/doxing utility to collect publicly available information about targets (usernames, emails, IPs), discover related social media accounts, check for leaks, and visualize relationships with a graph visualizer. This tool is intended for educational and authorized use only.

> ⚠️ **Use Responsibly** — Do not use this tool for illegal activity. Always have permission before probing accounts or systems you do not own.

---

## 🔍 Features
- Username scanning across many social platforms
- Email leak checks and related findings
- IP information lookups
- Graph visualizer to present relationships and results
- CLI output modes and optional GUI visualization
- Configurable via `config.json`

---

## 📁 Repo structure (example)
vector/
├─ vector.py
├─ requirements.txt
├─ config.json
├─ links.md
├─ README.md
└─ ...other modules/scripts...


---

## 🚀 Quick Start

### Requirements
- Python 3.8+
- `pip`

### Windows
- Option A — Using Git:
  git clone https://github.com/thesaderror/vector.git
  cd vector
  python -m venv venv
  venv\Scripts\activate
  pip install -r requirements.txt
  python vector.py v

- Option B — Download ZIP:
  Click Code → Download ZIP on GitHub.
  Extract the archive and open the folder in a terminal.
  Create/activate a virtual environment and install requirements as above.

⚙️ Configuration
- Edit config.json to set API keys, toggles for modules, or output locations.

Example config.json:

{
  "pinata_api_key": "",
  "pinata_secret": "",
  "save_results": true,
  "output_dir": "outputs"
}


Also check links.md for configurable social endpoints and provider lists.








