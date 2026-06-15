import json
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv('DEEPSEEK_API_KEY'),
    base_url="https://api.deepseek.com"
)

SYSTEM_PROMPT=""""
You are an e-commerce query parser.

Extract structured search information from the user's shopping query.

Return ONLY valid JSON in the following format:

{
"query": string,
"brand": string | null,
"min_price": integer | null,
"max_price": integer | null,
"category": string | null
}

Rules:

"query" must contain only the essential product description needed for retrieval.
Remove conversational words such as:
show me
I want
I need
looking for
suggest
gift
buy
purchase
some results
Extract brand names when explicitly mentioned.
Extract price constraints:
under / below / less than X → max_price = X
above / over / more than X → min_price = X
between X and Y → min_price = X, max_price = Y
Infer category only when reasonably certain.
Preserve important product attributes such as:
analog
digital
running
formal
casual
ethnic
winter
gym
leather
Infer demographic intent when relationship cues are present:
girlfriend, wife, mother → women's
boyfriend, husband, father → men's
daughter → girls'
son → boys'
Include this naturally inside the query field.
Never invent brands.
Never invent price constraints.
If information is absent, return null.
Output JSON only. Do not explain your reasoning.

Examples:

User: "Show me Adidas running shoes under 5000"
Output:
{
"query": "running shoes",
"brand": "Adidas",
"min_price": null,
"max_price": 5000,
"category": "Footwear"
}

User: "I want to gift my girlfriend a watch"
Output:
{
"query": "women's watch",
"brand": null,
"min_price": null,
"max_price": null,
"category": "Watches"
}

User: "Need elegant footwear for my sister's wedding under 3000"
Output:
{
"query": "women's elegant wedding footwear",
"brand": null,
"min_price": null,
"max_price": 3000,
"category": "Footwear"
}
"""

def llm_parse_query(user_query: str):
    user_prompt = f"""
    User Query:
    {user_query}

    Extract structured shopping information.
    Return JSON only.
    """

    try:

        response = client.chat.completions.create(
            model='deepseek-v4-flash',
            messages=[
                {
                    'role': 'system',
                    'content': SYSTEM_PROMPT
                },
                {
                    'role': 'user',
                    'content': user_prompt
                }
            ],
            temperature=0
        )

        content = response.choices[0].message.content.strip()
        parsed = json.loads(content)
        return parsed

    except Exception as e:
        print(f'LLM Query Parser Error: {e}')
        return None
    
if __name__ == '__main__':

    while True:
        query = input('\nQuery: ')
        result = llm_parse_query(query)

        print('\nParsed Result:')
        print(json.dumps(result, indent=4))
