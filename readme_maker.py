#!/usr/bin/env python3
"""gh-readme-maker: generate a professional GitHub profile README from a JSON config.

Usage:
    python readme_maker.py config.json > README.md

Paste the result into the README of your <username>/<username> profile repository.
Python 3 standard library only - no third-party dependencies.
"""

import json
import sys
import urllib.parse

USAGE = "Usage: python readme_maker.py <config.json>"

# Badge colours cycled through when a skill has no explicit badge_url.
_BADGE_COLORS = ["3776AB", "F05032", "2CA5E0", "E34F26", "3178C6", "61DAFB"]

# shields.io logo slugs for common skills. Skills not listed here still get a
# badge; the logo parameter is simply omitted for them.
_LOGO_SLUGS = {
    "python": "python",
    "javascript": "javascript",
    "typescript": "typescript",
    "go": "go",
    "rust": "rust",
    "java": "openjdk",
    "c++": "cplusplus",
    "c#": "csharp",
    "html5": "html5",
    "html": "html5",
    "css3": "css",
    "css": "css",
    "react": "react",
    "node.js": "nodedotjs",
    "node": "nodedotjs",
    "django": "django",
    "flask": "flask",
    "fastapi": "fastapi",
    "docker": "docker",
    "git": "git",
    "github": "github",
    "linux": "linux",
    "postgresql": "postgresql",
    "mysql": "mysql",
    "mongodb": "mongodb",
    "sqlite": "sqlite",
    "telegram": "telegram",
    "vs code": "visualstudiocode",
    "visual studio code": "visualstudiocode",
}


def shields_label(name):
    """Encode a skill name for the shields.io path-badge format.

    In this format '_' renders as a space, '--' as a literal dash and
    '__' as a literal underscore.
    """
    return name.replace("_", "__").replace("-", "--").replace(" ", "_")


def auto_badge(name, index=0):
    """Build a shields.io badge URL for a bare skill name."""
    label = shields_label(name)
    color = _BADGE_COLORS[index % len(_BADGE_COLORS)]
    url = "https://img.shields.io/badge/{}-{}?style=flat".format(label, color)
    logo = _LOGO_SLUGS.get(name.strip().lower())
    if logo:
        url += "&logo={}&logoColor=white".format(logo)
    return url


def cell(text):
    """Escape text so it is safe inside a Markdown table cell."""
    return str(text).replace("|", "\\|").replace("\r", "").replace("\n", "<br />")


def fail(message):
    print("gh-readme-maker: error: {}".format(message), file=sys.stderr)
    sys.exit(1)


def load_config(path):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            config = json.load(fh)
    except FileNotFoundError:
        fail("file not found: {}".format(path))
    except json.JSONDecodeError as exc:
        fail("invalid JSON in {}: {}".format(path, exc))
    if not isinstance(config, dict):
        fail("config must be a JSON object")
    name = config.get("name")
    if not name or not str(name).strip():
        fail("config must include a non-empty 'name'")
    return config


def build_markdown(config):
    name = str(config["name"]).strip()
    tagline = str(config.get("tagline") or "").strip()
    about = str(config.get("about") or "").strip()
    projects = config.get("projects") or []
    skills = config.get("skills") or []
    socials = config.get("socials") or []

    sections = []

    header = '<h1 align="center">Hi there, I\'m {} \U0001f44b</h1>'.format(name)
    if tagline:
        header += "\n\n<p align=\"center\">{}</p>".format(tagline)
    sections.append(header)

    if about:
        sections.append("## About\n\n{}".format(about))

    rows = []
    for proj in projects:
        if not isinstance(proj, dict):
            continue
        pname = str(proj.get("name") or "").strip()
        if not pname:
            continue
        url = str(proj.get("url") or "").strip()
        desc = str(proj.get("description") or "").strip()
        label = "[{}]({})".format(cell(pname), url) if url else cell(pname)
        rows.append("| {} | {} |".format(label, cell(desc)))
    if rows:
        table = ["## Projects", "", "| Name | Description |",
                 "| --- | --- |"] + rows
        sections.append("\n".join(table))

    badges = []
    for i, skill in enumerate(skills):
        if isinstance(skill, dict):
            sname = str(skill.get("name") or "").strip()
            if not sname:
                continue
            badge_url = str(skill.get("badge_url") or "").strip() or auto_badge(sname, i)
        else:
            sname = str(skill).strip()
            if not sname:
                continue
            badge_url = auto_badge(sname, i)
        badges.append("![{}]({})".format(sname, badge_url))
    if badges:
        sections.append("## Tech Stack\n\n" + " ".join(badges))

    links = []
    for soc in socials:
        if not isinstance(soc, dict):
            continue
        label = str(soc.get("label") or "").strip()
        url = str(soc.get("url") or "").strip()
        if label and url:
            links.append("[{}]({})".format(label, url))
    if links:
        sections.append("## Connect\n\n<p align=\"center\">{}</p>".format(
            " &middot; ".join(links)))

    return "\n\n---\n\n".join(sections) + "\n"


def main(argv):
    if len(argv) == 2 and argv[1] in ("-h", "--help"):
        print(USAGE)
        return 0
    if len(argv) != 2:
        print(USAGE, file=sys.stderr)
        return 1
    config = load_config(argv[1])
    sys.stdout.write(build_markdown(config))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
