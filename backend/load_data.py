import asyncio
import csv
from database import db

async def load_csv_to_collection(csv_file, collection_name):
    with open(csv_file, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        data = [dict(row) for row in reader]
        for doc in data:
            for key, value in doc.items():
                if value == "":
                    doc[key] = None
        await db[collection_name].delete_many({})  # Clear old data
        await db[collection_name].insert_many(data)
        print(f"Inserted {len(data)} records into '{collection_name}'.")

async def main():
    await load_csv_to_collection("F:/customerChatbot/dataset_files/distribution_centers.csv", "distribution_centers")
    await load_csv_to_collection("F:/customerChatbot/dataset_files/inventory_items.csv", "inventory_items")
    await load_csv_to_collection("F:/customerChatbot/dataset_files/order_items.csv", "order_items")
    await load_csv_to_collection("F:/customerChatbot/dataset_files/orders.csv", "orders")
    await load_csv_to_collection("F:/customerChatbot/dataset_files/products.csv", "products")
    await load_csv_to_collection("F:/customerChatbot/dataset_files/users.csv", "users")

if __name__ == "__main__":
    asyncio.run(main())
