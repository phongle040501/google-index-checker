# 🤖 Claude Agent Instructions - Google Index Checker

This repository contains an automated tool for checking the Google Search indexing status of URLs (`site:url`) and generating detailed report files in Markdown (`Index_Report.md`) and Excel (`.xlsx`).

---

## 🚀 Quick Onboarding for Fresh Clones / New Colleagues

If a colleague clones/opens this repository for the first time and asks Claude Code to run the tool, follow these steps automatically:

1. **Auto-Install Requirements:** Automatically run `pip install -r requirements.txt` if dependencies are missing.
2. **Check URLs:** Check if `urls.txt` has URLs. If the user provides URLs in their message, write them directly to `urls.txt`.
3. **Verify Config:** Ensure `config.json` is present. If missing, create `config.json` from `config.json.example` and ask the user for their Serper API key if required.
4. **Execute Check:** Run `python check_index.py`.
5. **Report & Analyze:** Read `Index_Report.md` and provide a clear summary of Indexed vs. Non-Indexed URLs along with SEO optimization advice.

---

## 🎯 Overview & Agent Capabilities

When the user asks Claude (Desktop App / Claude Code / AI Agent) to check Google indexing status, perform analysis, or troubleshoot URLs, follow these instructions:

### 1. Requirements & Setup
- **Python Version:** 3.8+
- **Dependencies:** `pandas`, `openpyxl`, `requests` / `urllib`
- **Config File:** `config.json` (contains `serper_api_key` or Google Custom Search credentials).
  - Use `config.json.example` as a template if `config.json` does not exist.

---

## 🚀 Commands for AI Agent Execution

| Task | Command |
| :--- | :--- |
| **Run Index Check on `urls.txt`** | `python check_index.py` |
| **Run Index Check on Specific File** | `python check_index.py -f <path_to_file.txt>` |
| **Run Index Check on Inline URLs** | `python check_index.py -u "https://example.com/page1, https://example.com/page2"` |
| **Install Dependencies** | `pip install -r requirements.txt` |

---

## 📋 Standard Workflow for Claude Agent

When the user requests an Index Check:

1. **Verify `urls.txt`:** Ensure `urls.txt` exists and contains the URLs to be checked (one per line). If the user provides URLs in chat, write them to `urls.txt` or use the `-u` argument.
2. **Verify `config.json`:** Check if `config.json` exists with a valid `serper_api_key`. If missing, notify the user or prompt them to fill in `config.json` dựa trên `config.json.example`.
3. **Execute Command:** Run `python check_index.py`.
4. **Analyze Results:**
   - Read the generated `Index_Report.md` file.
   - Summarize the total URLs checked, count of Indexed vs. Non-Indexed URLs.
   - List the Non-Indexed URLs and provide actionable SEO recommendations for why they might not be indexed (e.g., thin content, canonical tags, noindex tags, crawl errors).
5. **Present Output:** Direct the user to `Index_Report.md` and the timestamped `.xlsx` report generated in the workspace root.
