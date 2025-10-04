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

# 📁 Repo structure (example)
vector/
├─ vector.py
├─ requirements.txt
├─ config.json
├─ links.md
├─ README.md
└─ ...other modules/scripts...


---

# 🚀 Quick Start

# Requirements
- Python 3.8+
- `pip`

# Windows
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

# ⚙️ Configuration
- Edit config.json to set API keys, toggles for modules, or output locations.

  Example config.json:

  {
    "pinata_api_key": "",
    "pinata_secret": "",
    "save_results": true,
    "output_dir": "outputs"
  }


  Also check links.md for configurable social endpoints and provider lists.

# ❓ Usage Examples
- General help
  python vector.py --help

# Username scan (OSINT)
- python vector.py username <target_username>
   e.g.
  python vector.py username john_doe

# Email scan
- python vector.py email <target_email>
   e.g.
  python vector.py email example@domain.com

# IP Info
- python vector.py ip <ip_address>
   e.g.
  python vector.py ip 8.8.8.8

# Notes
- Some modules may require external API keys or credentials — set them in config.json.
  Respect rate limits and terms of service for any third-party APIs.

# 🖼️ Preview
# CLI social media OSINT scan (Style: E0)
- <img width="864" height="889" alt="image" src="https://github.com/user-attachments/assets/d488b665-4bbf-408e-905a-ab9ea98e89c7" />
  <img width="716" height="722" alt="image" src="https://github.com/user-attachments/assets/1b786412-9831-4b57-84e4-2ce9d95e0471" />


# CLI Email Leak Leak Search (Style: E0)
-  <img width="856" height="483" alt="image" src="https://github.com/user-attachments/assets/03b9123e-9d34-4171-93ae-643518efd0e5" />

# CLI Vector geo info sniper (Style: E0)
- <img width="694" height="414" alt="image" src="https://github.com/user-attachments/assets/d88af67d-f7e1-4de0-97a9-afd2bdb58502" />

# Graph GUI examples
- <img width="625" height="856" alt="image" src="https://github.com/user-attachments/assets/aac1d86c-1f39-4e2c-8338-08318e76b051" />
  <img width="1233" height="805" alt="image" src="https://github.com/user-attachments/assets/9f0b71cc-b02d-4e3f-ad48-fbd49061f180" />

# 🧾 Help & Tips
- Always test on accounts you own or have explicit permission to analyze.
  Rate limits may apply for certain service queries — respect provider rules.
  For best results, configure any available API keys in config.json.  

# 🤝 Contributing
- Contributions, issues and feature requests are welcome. Please:
  1. Fork the repository
  2. Create a feature branch
     git checkout -b feature/your-feature
  3. Commit your changes
     git commit -m "Add feature"
  4. Push to your branch
     git push origin feature/your-feature
  5. Open a Pull Request

 # 📜 License & Disclaimer
 - Disclaimer: This tool is for educational and authorized testing only. The author and contributors are not responsible for misuse. Make sure you have explicit permission before scanning     or collecting information about any person or system.
   Author & Credits: originally by Thesaderror and H4wK1n6 (as stated in original project).

# 📫 Contact / Links
 - Project links and references: links.md
   Edit config.json for custom settings
















