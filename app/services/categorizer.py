from app.database import categories_collection

async def categorize(description: str) -> str:
    desc = description.lower()

    cursor = categories_collection.find({"active": True})

    async for category in cursor:
        for keyword in category.get("keywords", []):
            if keyword.lower() in desc:
                return category["name"]

    return "Others"
