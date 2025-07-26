from db import db
import httpx, os
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# --- SMART INTENT HANDLING ---

async def get_products_by_brand(brand):
    cursor = db["products"].find({"brand": {"$regex": brand, "$options": "i"}})
    return await cursor.to_list(5)

async def get_orders_by_user(user_id):
    cursor = db["orders"].find({"user_id": user_id}).sort("created_at", -1)
    return await cursor.to_list(3)

async def get_product_by_name(name):
    return await db["products"].find_one({"name": {"$regex": name, "$options": "i"}})

async def get_distribution_center_for_product(product_id):
    product = await db["products"].find_one({"id": product_id})
    if not product:
        return None
    return await db["distribution_centers"].find_one({"id": product.get("distribution_center_id")})

# --- INTENT CLASSIFIER (basic rule-based for now) ---

def detect_intent(message: str):
    msg = message.lower()
    if "nike" in msg or "shoes" in msg:
        return "product_brand"
    elif "air max" in msg or "price of" in msg:
        return "product_name"
    elif "where is my order" in msg:
        return "track_order"
    elif "distribution center" in msg:
        return "dist_center"
    else:
        return "general"

# --- MAIN ENTRY POINT TO LLM ---

async def ask_llm_with_context(user_message: str, user_id: str = None):
    intent = detect_intent(user_message)

    context = ""
    if intent == "product_brand":
        products = await get_products_by_brand("Nike")
        if products:
            context = "\n".join([
                f"- {p['name']} (₹{p['retail_price']})"
                for p in products
            ])
        else:
            context = "No Nike products found."

    elif intent == "product_name":
        product = await get_product_by_name(user_message)
        if product:
            context = f"{product['name']} is priced at ₹{product['retail_price']} and belongs to {product['category']}."
        else:
            context = "Sorry, I couldn't find that product."

    elif intent == "track_order" and user_id:
        orders = await get_orders_by_user(user_id)
        if orders:
            context = "\n".join([
                f"Order {o['order_id']} is {o['status']}, shipped at {o.get('shipped_at', 'N/A')}, delivered at {o.get('delivered_at', 'N/A')}."
                for o in orders
            ])
        else:
            context = "No recent orders found for this user."

    elif intent == "dist_center":
        # Assume product_id is embedded in message for demo
        product = await get_product_by_name(user_message)
        if product:
            center = await get_distribution_center_for_product(product["id"])
            if center:
                context = f"{product['name']} is shipped from {center['name']} located at ({center['latitude']}, {center['longitude']})"
            else:
                context = "Could not find distribution center info."
        else:
            context = "Could not find product info."

    else:
        context = ""  # general chat

    prompt = f"""
You are an e-commerce assistant. The user said:
"{user_message}"

Here is some context to help:
{context}

Respond in a clear and friendly way.
"""

    # --- Call Groq ---
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}"}
    data = {
        "model": "mixtral-8x7b-32768",
        "messages": [{"role": "user", "content": prompt}]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=data
        )
        return response.json()["choices"][0]["message"]["content"]
