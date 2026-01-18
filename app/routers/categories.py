from fastapi import APIRouter, Depends, HTTPException
from app.auth import admin_required
from app.database import categories_collection
from app.schemas import CategorySchema

router = APIRouter()

@router.post("/categories")
async def add_category(category: CategorySchema,  current_user = Depends(admin_required)):
    if await categories_collection.find_one({"name": category.name}):
        raise HTTPException(400, "Category already exists")

    await categories_collection.insert_one(category.dict())
    return {"message": "Category added successfully"}

@router.put("/updateCategories")
async def update_category(category: CategorySchema, current_user = Depends(admin_required)):
    # Normalize keywords (lowercase + unique)
    keywords = list(set(k.lower() for k in category.keywords))

    result = await categories_collection.update_one(
        {"name": category.name},
        {
            "$addToSet": {
                "keywords": {"$each": keywords}
            },
            "$set": {
                "active": category.active
            }
        }
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Category not found"
        )

    return {
        "message": "Category updated successfully",
        "category": category.name,
        "added_keywords": keywords
    }
