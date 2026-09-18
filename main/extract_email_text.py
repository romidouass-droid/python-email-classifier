"""
Email Text Extraction Module (Task 2)

Cleans raw .eml email files and extracts usable plain text for AI
classification: strips HTML, attachments, and garbage characters,
then combines subject + body into one clean string.

Requirements:
    pip install beautifulsoup4

Usage:
    from extract_email_text import extract_email_text
    text = extract_email_text("sample.eml")

    # or run directly on one or more .eml files:
    python extract_email_text.py email1.eml email2.eml
"""

import re
import sys
import glob
from email import policy
from email.parser import BytesParser

from bs4 import BeautifulSoup


def extract_email_text(file_path):
    """
    Read a .eml file and return a single cleaned text string containing
    the subject, sender, and plain-text body (HTML converted to text,
    attachments skipped).
    """
    with open(file_path, "rb") as f:
        msg = BytesParser(policy=policy.default).parse(f)

    subject = msg.get("Subject", "") or ""
    sender = msg.get("From", "") or ""

    body_text = _extract_body(msg)

    combined = f"Subject: {subject}\nFrom: {sender}\n\n{body_text}"
    return _clean_text(combined)


def _extract_body(msg):
    """Walk the email, pulling text/plain and text/html parts and
    skipping any attachments."""
    body_parts = []

    if msg.is_multipart():
        for part in msg.walk():
            disposition = str(part.get("Content-Disposition", ""))
            if "attachment" in disposition.lower():
                continue  # skip attachment content entirely

            content_type = part.get_content_type()

            if content_type == "text/plain":
                body_parts.append(_safe_get_content(part))
            elif content_type == "text/html":
                body_parts.append(_html_to_text(_safe_get_content(part)))
    else:
        content_type = msg.get_content_type()
        content = _safe_get_content(msg)
        if content_type == "text/html":
            body_parts.append(_html_to_text(content))
        else:
            body_parts.append(content)

    return "\n".join(p for p in body_parts if p)


def _safe_get_content(part):
    try:
        return part.get_content()
    except Exception:
        return ""


def _html_to_text(html):
    """Convert an HTML email body into plain text using BeautifulSoup."""
    if not html:
        return ""
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style"]):
        tag.decompose()
    text = soup.get_text(separator="\n")
    text = re.sub(r"<[^>]+>", "", text)  # remove any leftover HTML tags
    return text


def _clean_text(text):
    """Remove extra blank lines, stray symbols, and garbage characters."""
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n\s*\n+", "\n\n", text)
    # keep printable ASCII + newlines only (drops weird encoded junk)
    text = re.sub(r"[^\x20-\x7E\n]+", "", text)
    return text.strip()


if __name__ == "__main__":
    files = sys.argv[1:] if len(sys.argv) > 1 else glob.glob("*.eml")

    if not files:
        print("Usage: python extract_email_text.py file1.eml file2.eml ...")
        print("(or place .eml files in this folder and run with no arguments)")
        sys.exit(0)

    for fp in files:
        print(f"\n===== {fp} =====")
        try:
            print(extract_email_text(fp))
        except Exception as e:
            print(f"Error processing {fp}: {e}")