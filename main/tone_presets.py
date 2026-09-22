"""
AI Reply Custom Tone Presets

Lets the user pick a tone (Professional, Casual, Short, Apologetic,
Follow-Up) when generating an AI reply, instead of always getting the
same generic tone.

Reuses the same Groq connection as reply_generator.py (call_groq),
so both files talk to the AI the same way.
"""

from reply_generator import call_groq


TONE_INSTRUCTIONS = {
    "Professional": "Write in a professional, formal tone suitable for a workplace.",
    "Casual": "Write in a casual, friendly, relaxed tone, like messaging a friend.",
    "Short": "Write a very short, concise reply. No more than 2-3 sentences.",
    "Apologetic": "Write in a polite, apologetic tone, acknowledging any delay or inconvenience.",
    "Follow-Up": "Write as a polite follow-up reminder, gently asking for a response or update.",
}

TONE_LABELS = {
    "Professional": "💼 Professional",
    "Casual": "😊 Casual",
    "Short": "✂️ Short",
    "Apologetic": "🙏 Apologetic",
    "Follow-Up": "⏰ Follow-Up",
}


def generate_reply_with_tone(email_text, short_notes, tone="Professional"):
    """
    Generate a full email reply from a few short notes, in a chosen tone.

    Args:
        email_text (str): The original email's cleaned text.
        short_notes (str): A few words describing how the user wants to reply.
        tone (str): One of "Professional", "Casual", "Short", "Apologetic",
            "Follow-Up". Defaults to "Professional".

    Returns:
        str: The AI-generated full reply, written in the chosen tone.
    """

    if not short_notes or not short_notes.strip():
        raise ValueError("Reply notes cannot be empty.")

    tone_instruction = TONE_INSTRUCTIONS.get(tone, TONE_INSTRUCTIONS["Professional"])

    prompt = (
        f"Here is the original email:\n{email_text}\n\n"
        f"Write a full email reply based on these short notes: "
        f"{short_notes}\n\n"
        f"Tone instruction: {tone_instruction}\n\n"
        f"Only return the reply text, nothing else."
    )

    return call_groq(prompt)