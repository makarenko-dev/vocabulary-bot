import settings
from openai import OpenAI
import json


def translate_and_check(word: str):
    client = OpenAI(api_key=settings.OPEN_AI_KEY)

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=[
            {
                "role": "system",
                "content": [
                    {
                        "type": "input_text",
                        "text": 'Act as a translator. User will provide word or phraze in slovak language. Your task if fix errors, if they are present and give english translation for this word.\nRespond with json\n{\n"correct_word":"<corrected word here>"\n"translation":"<translation>"\n}',
                    }
                ],
            },
            {"role": "user", "content": [{"type": "input_text", "text": word}]},
        ],
        text={"format": {"type": "json_object"}},
    )
    data = json.loads(response.output_text)
    return data["correct_word"], data["translation"]
