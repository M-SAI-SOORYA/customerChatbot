from database import db
import httpx
import os
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

async def get_products_by_brand(brand: str):
    
    cursor = db["products"].find({"brand": {"$regex": brand, "$options": "i"}})
    products = await cursor.to_list(length=5)  # limit to 5 for readability
    return products

async def ask_llm_with_context(user_message: str):
    # Very basic keyword intent detection
    if "nike" in user_message.lower():
        brand = "Nike"
        products = await get_products_by_brand(brand)

        if not products:
            context = f"No products found for brand '{brand}'."
        else:
            context = "\n".join([
                f"- {p['name']} | ₹{p['retail_price']} | Category: {p['category']}"
                for p in products
            ])
        prompt = f"""
            You are a shopping assistant. The user asked: "{user_message}"
            Here is some product data you can use to help answer:
            {context}
            Now reply in a helpful, friendly tone.
            """

    else:
        # fallback: just pass the user's message
        prompt = user_message

    # --- Call Groq API ---
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mixtral-8x7b-32768",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=data
        )
        result = response.json()
        return result["choices"][0]["message"]["content"]
