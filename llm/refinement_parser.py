import json
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key = os.getenv('DEEPSEEK_API_KEY'),
    base_url = 'https://api.deepseek.com'
)

SYSTEM_PROMPT = """
You are an expert shopping assistant.

Your task is to UPDATE an existing shopping search context.

You receive:

1. Previous search context
2. User refinement

Modify ONLY the fields requested by the user.

Keep every other field unchanged.

Allowed fields:

query
brand
category
min_price
max_price

Examples:

Context:
{
"query":"running shoes",
"brand":"Nike",
"max_price":5000
}

User:
cheaper ones

Output:
{
"query":"running shoes",
"brand":"Nike",
"max_price":3500
}

------------------------

Context:
{
"query":"running shoes",
"brand":"Nike"
}

User:
for women

Output:
{
"query":"women running shoes",
"brand":"Nike"
}

------------------------

Context:
{
"query":"shirts"
}

User:
formal instead

Output:
{
"query":"formal shirts"
}

------------------------

Context:
{
"query":"shirts"
}

User:
not Adidas

Output:
{
"query":"shirts",
"brand":null
}

Return ONLY valid JSON.
"""

def llm_refine_query(context: dict, refinement: str):
    user_prompt = f"""
    Previous Context:
    {json.dumps(context, indent=2)}
    User Refinement:
    {refinement}
    Return updated JSON only.
    """

    try:
        response = client.chat.completions.create(
            model='deepseek-chat',
            messages=[
                {
                    'role': 'system',
                    'content': user_prompt
                }
            ],
            temperature=0
        )

        content = response.choices[0].message.content.strip()

        if content.startswith('```'):
            content = content.replace('```json', '')
            content = content.replace('```', '')
            content = content.strip()

        return json.loads(content)

    except Exception as e:
        print('LLM Refinement Error:', e)
        return content