"""
Reply Template Save & Reuse

Lets the user save a generated (or edited) reply as a reusable template,
and load it back instantly later for repetitive emails (confirmations,
follow-ups, thank-you notes) instead of generating a new AI reply
every time.

Templates are stored locally in templates.json, next to this file.
"""

import json
import os

TEMPLATES_FILE = os.path.join(os.path.dirname(__file__), "templates.json")


def load_templates():
    """
    Load all saved templates.

    Returns:
        dict: {template_name: template_text}
    """
    if not os.path.exists(TEMPLATES_FILE):
        return {}

    try:
        with open(TEMPLATES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def save_template(name, content):
    """
    Save a new template, or overwrite an existing one with the same name.

    Args:
        name (str): A short label for the template, e.g. "Meeting confirmation".
        content (str): The reply text to save.
    """
    if not name or not name.strip():
        raise ValueError("Template name cannot be empty.")

    if not content or not content.strip():
        raise ValueError("Template content cannot be empty.")

    templates = load_templates()
    templates[name.strip()] = content.strip()

    with open(TEMPLATES_FILE, "w", encoding="utf-8") as f:
        json.dump(templates, f, indent=2, ensure_ascii=False)


def delete_template(name):
    """Remove a saved template by name, if it exists."""
    templates = load_templates()

    if name in templates:
        del templates[name]
        with open(TEMPLATES_FILE, "w", encoding="utf-8") as f:
            json.dump(templates, f, indent=2, ensure_ascii=False)