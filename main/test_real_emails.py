import os
import email
from email import policy

from api_classifier import classify_email


def extract_text_from_eml(filepath):
    """Read an .eml file and return its subject + plain text body."""
    with open(filepath, "rb") as f:
        msg = email.message_from_binary_file(f, policy=policy.default)

    subject = msg.get("subject", "")

    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == "text/plain":
                body = part.get_content()
                break
    else:
        body = msg.get_content()

    return f"Subject: {subject}\n\n{body}"


def main():
    # Folder containing your sample .eml files (adjust path if needed)
    test_files_dir = os.path.join("..", "test_files")

    if not os.path.isdir(test_files_dir):
        test_files_dir = "test_files"  # fallback if run from project root

    eml_files = sorted(
        f for f in os.listdir(test_files_dir) if f.lower().endswith(".eml")
    )

    if not eml_files:
        print(f"No .eml files found in {test_files_dir}")
        return

    for filename in eml_files:
        filepath = os.path.join(test_files_dir, filename)
        print("=" * 60)
        print("FILE:", filename)

        try:
            text = extract_text_from_eml(filepath)
            subject_line = text.split("\n", 1)[0]
            print(subject_line)
            result = classify_email(text)
            print("RESULT:", result)
        except Exception as error:
            print("Error:", error)

        print()


if __name__ == "__main__":
    main()