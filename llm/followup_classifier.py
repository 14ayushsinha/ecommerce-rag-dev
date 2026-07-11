from openai import OpenAI
from dotenv import load_dotenv
import json
import os

load_dotenv()
client = OpenAI(
    api_key=os.getenv('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com"
)

SYSTEM_PROMPT = """
You determine whether the user's message is

FOLLOWUP

or

NEW_SEARCH.

Return ONLY JSON.

{
    "followup": true
}

Examples:

Previous:
running shoes under 5000

Current:
only adidas

followup=true

------------------

Previous:
running shoes

Current:
cheaper ones

followup=true

------------------

Previous:
running shoes

Current:
more premium

followup=true

------------------

Previous:
running shoes

Current:
women

followup=true

------------------

Previous:
running shoes

Current:
laptop under 60000

followup=false

------------------

Previous:
running shoes

Current:
gaming keyboard

followup=false
"""

def classify_followup(previous_query, current_query):
    response = client.chat.completions.create(
        model='deepseek-v4-flash',
        temperature=0,
        response_format={'type':'json_object'},
        messages=[
            {
                'role': 'system',
                'content': SYSTEM_PROMPT
            },
            {
                'role': 'user',
                'content': json.dumps({
                    'previous': previous_query,
                    'current': current_query
                })
            }
        ]
    )

    result = json.loads(response.choices[0].message.content)
    print(result)
    return result['followup']