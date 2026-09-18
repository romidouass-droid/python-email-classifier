import os
import requests


API_URL = "https://router.huggingface.co/hf-inference/models/facebook/bart-large-mnli"


def classify_email(clean_text):
    """
    Classify an email as Important or Normal.

    Args:
        clean_text (str): Clean email subject and body.

    Returns:
        str: "Important" or "Normal"
    """

    # Check for empty email text
    if not clean_text or not clean_text.strip():
        raise ValueError("Email text cannot be empty.")

    # Read the Hugging Face token from the environment
    api_token = os.getenv("HF_TOKEN")

    if not api_token:
        raise ValueError("HF_TOKEN environment variable is not set.")

    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }

    # Zero-shot classification request
    data = {
        "inputs": clean_text,
        "parameters": {
            "candidate_labels": [
                "important",
                "normal"
            ],
            "hypothesis_template": "This email is {}.",
            "multi_label": False
        }
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

        # Validate the API response
        if not isinstance(result, list) or not result:
            raise ValueError("Unexpected API response.")

        # Get labels and scores
        labels = []
        scores = []

        for item in result:
            labels.append(item["label"].lower())
            scores.append(float(item["score"]))

        # Find the scores for Important and Normal
        important_score = 0.0
        normal_score = 0.0

        for label, score in zip(labels, scores):
            if label == "important":
                important_score = score
            elif label == "normal":
                normal_score = score

        # Print scores so we can check the model's decision
        print("Important score:", important_score)
        print("Normal score:", normal_score)

        # Return the label with the higher score
        if important_score > normal_score:
            return "Important"

        return "Normal"

    except requests.exceptions.Timeout:
        raise RuntimeError(
            "The classification API request timed out."
        )

    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            "Could not connect to the classification API."
        )

    except requests.exceptions.HTTPError as error:
        raise RuntimeError(
            f"Classification API returned an HTTP error: {error}"
        )

    except requests.exceptions.RequestException as error:
        raise RuntimeError(
            f"API request failed: {error}"
        )

    except (ValueError, KeyError, TypeError) as error:
        raise RuntimeError(
            f"Invalid API response: {error}"
        )