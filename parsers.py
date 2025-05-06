# import re
from datetime import datetime

# If using Google's Gemini API
import google.generativeai as genai
import json  # For parsing Gemini's response
import os  # To get API key from environment variable

# Configure Gemini API Key
# It's recommended to use an environment variable for your API key
try:
    gemini_api_key = os.environ.get("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set.")
    genai.configure(api_key=gemini_api_key)
except ValueError as e:
    print(f"Error: {e}")
    # Handle the missing API key appropriately - perhaps by exiting or using a fallback
    # For now, we'll print the error and let it proceed, which will likely fail at the API call.

# Initialize the Gemini model
# Make sure to choose the model that best suits your needs, e.g., 'gemini-pro' or 'gemini-1.5-flash'
# Handling potential errors during model initialization
try:
    model = genai.GenerativeModel(
        "gemini-1.5-flash"
    )  # Or your chosen model, e.g., 'gemini-1.5-flash'
except Exception as e:
    print(f"Error initializing Gemini model: {e}")
    model = None  # Set model to None if initialization fails


def parse_workout_record(record: str) -> dict:
    if not model:
        print("Gemini model not initialized. Cannot parse workout record.")
        # Return a default or error structure
        return {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "running_time": None,
            "running_speed": None,
            "max_heart_rate": None,
            "exercises": [],
            "notes": "Error: Gemini model not available.",
        }

    # 1. Construct a prompt for the Gemini model.
    prompt_text = f"""
    Parse the following workout log:
    "{record}"
    Extract the information into a JSON object with fields:
    - date (string, YYYY-MM-DD, use today if not found: {datetime.now().strftime("%Y-%m-%d")})
    - running_time (integer, minutes, null if not applicable)
    - running_speed (float, km/h or mph, null if not applicable)
    - max_heart_rate (integer, bpm, null if not applicable)
    - exercises (list of objects: [{{'name': 'str', 'weight': 'float', 'reps': 'int', 'sets': 'int'}}], null if not applicable or empty list if no exercises)
    - notes (string, any remaining text or observations)
    Return only the JSON object. Ensure the output is a valid JSON.
    If a field is not mentioned, set its value to null (or an empty list for exercises).
    Example of an exercise entry: {{'name': 'Bench Press', 'weight': 70.5, 'reps': 10, 'sets': 3}}
    """

    # 2. Call the Gemini API and parse its response.
    parsed_by_gemini = {}
    try:
        # Ensure the model is available before attempting to generate content
        if model:
            response = model.generate_content(prompt_text)
            # Attempt to clean and parse the response text as JSON
            # Gemini might sometimes return the JSON wrapped in markdown (```json ... ```)
            cleaned_response_text = response.text.strip()
            if cleaned_response_text.startswith("```json"):
                cleaned_response_text = cleaned_response_text[7:]
            if cleaned_response_text.endswith("```"):
                cleaned_response_text = cleaned_response_text[:-3]

            parsed_by_gemini = json.loads(cleaned_response_text)
        else:
            raise Exception("Gemini model is not available.")

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from Gemini response: {e}")
        print(
            f"Gemini raw response: {response.text if 'response' in locals() else 'No response object'}"
        )
        # Fallback or re-raise
        parsed_by_gemini = {
            "notes": f"Failed to parse Gemini response. Raw: {response.text if 'response' in locals() else 'No response object'}"
        }
    except Exception as e:
        print(f"Error interacting with Gemini: {e}")
        # Fallback or re-raise
        parsed_by_gemini = {"notes": f"Error during Gemini interaction: {e}"}

    # 3. Map the data from Gemini to the function's expected return dictionary.
    result = {
        "date": parsed_by_gemini.get("date", datetime.now().strftime("%Y-%m-%d")),
        "running_time": parsed_by_gemini.get("running_time"),
        "running_speed": parsed_by_gemini.get("running_speed"),
        "max_heart_rate": parsed_by_gemini.get("max_heart_rate"),
        "exercises": parsed_by_gemini.get("exercises", []),
        "notes": parsed_by_gemini.get("notes", ""),
    }

    return result
