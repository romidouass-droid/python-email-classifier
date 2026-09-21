from reply_generator import generate_reply


print("TEST 1: Simple reply")

email = """
Subject: Meeting tomorrow?

Hi,

Are you free for a meeting tomorrow at 10 AM to discuss the project?

Best,
John
"""

notes = "yes tomorrow works, send location"

try:
    result = generate_reply(email, notes)
    print("Generated reply:\n", result)
except Exception as error:
    print("Error:", error)


print("\nTEST 2: Empty notes")

try:
    result = generate_reply(email, "")
    print("Generated reply:\n", result)
except Exception as error:
    print("Error:", error)