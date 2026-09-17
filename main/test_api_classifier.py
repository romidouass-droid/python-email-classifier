from api_classifier import classify_email


# Test 1: Important email
important_email = """
Subject: Urgent Project Meeting

Dear Team,

This is an urgent reminder that we have an important
project meeting tomorrow at 10 AM.

Please prepare all the required documents.

Best regards,
Project Manager
"""


print("TEST 1: Important email")

try:
    result = classify_email(important_email)
    print("Email classification result:", result)

except Exception as error:
    print("Error:", error)


print("\nTEST 2: Empty email")

# Test 2: Empty email
empty_email = ""

try:
    result = classify_email(empty_email)
    print("Email classification result:", result)

except Exception as error:
    print("Error:", error)