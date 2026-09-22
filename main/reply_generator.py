def generate_reply(email_content):
    return "Thank you for your email. I have received your message and will review it shortly."
import os
import requests


API_URL = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "openai/gpt-oss-120b"


def call_groq(prompt):
    """
    Send a prompt to the Groq API and return the AI's text response.
    Shared by reply_generator.py and tone_presets.py so both use the
    same connection and error-handling logic.
    """

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable is not set.")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(
            API_URL,
            headers=headers,
            json=data,
            timeout=30
        )

        response.raise_for_status()

        result = response.json()

        return result["choices"][0]["message"]["content"].strip()

    except requests.exceptions.Timeout:
        raise RuntimeError(
            "The reply generation request timed out."
        )

    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            "Could not connect to the Groq API."
        )

    except requests.exceptions.HTTPError as error:
        raise RuntimeError(
            f"Groq API returned an HTTP error: {error} | "
            f"Response body: {response.text}"
        )

    except requests.exceptions.RequestException as error:
        raise RuntimeError(
            f"API request failed: {error}"
        )

    except (ValueError, KeyError, TypeError) as error:
        raise RuntimeError(
            f"Invalid API response: {error}"
        )


def generate_reply(email_text, short_notes):
    """
    Generate a full, polite email reply from a few short notes.

    Args:
        email_text (str): The original email's cleaned text.
        short_notes (str): A few words describing how the user wants to reply.

    Returns:
        str: The AI-generated full reply.
    """

    if not short_notes or not short_notes.strip():
        raise ValueError("Reply notes cannot be empty.")

    prompt = (
        f"Here is the original email:\n{email_text}\n\n"
        f"Write a full, polite email reply based on these short notes: "
        f"{short_notes}\n\n"
        f"Only return the reply text, nothing else."
    )

    return call_groq(prompt)
