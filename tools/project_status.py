#!/usr/bin/env python3
"""
Dutray Yorkies - GitHub Project Status Reporter

Creates a markdown status report from GitHub repository issues.

Requirements:
    pip install requests python-dotenv

Setup:
    1. Create a GitHub personal access token.
    2. Add it to a local .env file:
       GITHUB_TOKEN=your_token_here
       GITHUB_OWNER=hornmarc
       GITHUB_REPO=dutray-yorkies

Run:
    python tools/project_status.py
"""

import os
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv


ROOT = Path(__file__).resolve().parents[1]
REPORT_PATH = ROOT / "docs" / "PROJECT_STATUS.md"


def github_get(url, token):
    response = requests.get(
        url,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
        },
        timeout=20,
    )
    response.raise_for_status()
    return response.json()


def main():
    load_dotenv()

    token = os.getenv("GITHUB_TOKEN")
    owner = os.getenv("GITHUB_OWNER", "hornmarc")
    repo = os.getenv("GITHUB_REPO", "dutray-yorkies")

    if not token:
        raise SystemExit("Missing GITHUB_TOKEN in .env file.")

    repo_url = f"https://api.github.com/repos/{owner}/{repo}"

    repo_info = github_get(repo_url, token)
    issues = github_get(f"{repo_url}/issues?state=all&per_page=100", token)
    commits = github_get(f"{repo_url}/commits?per_page=10", token)

    open_issues = [i for i in issues if "pull_request" not in i and i["state"] == "open"]
    closed_issues = [i for i in issues if "pull_request" not in i and i["state"] == "closed"]

    REPORT_PATH.parent.mkdir(exist_ok=True)

    lines = []
    lines.append("# Dutray Yorkies Project Status")
    lines.append("")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %I:%M %p')}")
    lines.append("")
    lines.append("## Repository")
    lines.append("")
    lines.append(f"- Name: `{repo_info['full_name']}`")
    lines.append(f"- Default branch: `{repo_info['default_branch']}`")
    lines.append(f"- Visibility: `{repo_info['visibility']}`")
    lines.append(f"- Open issues: `{len(open_issues)}`")
    lines.append(f"- Closed issues: `{len(closed_issues)}`")
    lines.append("")

    lines.append("## Latest Commits")
    lines.append("")
    for commit in commits[:10]:
        sha = commit["sha"][:7]
        message = commit["commit"]["message"].splitlines()[0]
        author = commit["commit"]["author"]["name"]
        date = commit["commit"]["author"]["date"]
        lines.append(f"- `{sha}` {message} — {author}, {date}")
    lines.append("")

    lines.append("## Open Issues")
    lines.append("")
    if not open_issues:
        lines.append("No open issues.")
    else:
        for issue in open_issues:
            labels = ", ".join(label["name"] for label in issue["labels"]) or "no labels"
            lines.append(f"- #{issue['number']} **{issue['title']}** — {labels}")
    lines.append("")

    lines.append("## Closed Issues")
    lines.append("")
    if not closed_issues:
        lines.append("No closed issues.")
    else:
        for issue in closed_issues:
            lines.append(f"- #{issue['number']} **{issue['title']}**")
    lines.append("")

    lines.append("## Recommended Next Focus")
    lines.append("")
    if open_issues:
        lines.append(f"Start with: **#{open_issues[0]['number']} {open_issues[0]['title']}**")
    else:
        lines.append("No open issues. Create the next planning issue.")
    lines.append("")

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")

    print(f"Project status report created: {REPORT_PATH}")


if __name__ == "__main__":
    main()