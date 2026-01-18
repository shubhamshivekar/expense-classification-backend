import io
import pandas as pd
from datetime import datetime
from bson import ObjectId

from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import StreamingResponse

from app.database import transactions_collection, uploads_collection
from app.services.categorizer import categorize
from app.auth import user_required

router = APIRouter()
@router.post("/upload")
async def upload_csv(file: UploadFile = File(...),current_user = Depends(user_required)):
    try:
        user_id = current_user["user_id"]
        # Read CSV
        df = pd.read_csv(file.file)

        # Validate columns
        required_columns = {"date", "description", "amount"}
        if not required_columns.issubset(df.columns):
            raise HTTPException(
                status_code=400,
                detail="CSV must contain date, description, and amount columns"
            )

        # Store upload metadata
        upload_doc = {
            "filename": file.filename,
            "uploaded_at": datetime.utcnow()
        }
        upload_result = await uploads_collection.insert_one(upload_doc)
        upload_id = upload_result.inserted_id

        # Process transactions
        for _, row in df.iterrows():
            transaction = {
                "upload_id": upload_id,
                "date": pd.to_datetime(row["date"]).date(),
                "description": row["description"],
                "amount": float(row["amount"]),
                "category": await  categorize(row["description"])
            }
            await transactions_collection.insert_one(transaction)

        return {
            "message": "CSV uploaded and transactions categorized successfully",
            "upload_id": str(upload_id)
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to process CSV: {str(e)}"
        )


@router.get("/export")
async def export_csv(current_user = Depends(user_required)):
    cursor = transactions_collection.find({})

    output = io.StringIO()
    output.write("date,description,amount,category\n")

    async for txn in cursor:
        output.write(
            f"{txn['date']},{txn['description']},{txn['amount']},{txn['category']}\n"
        )

    output.seek(0)

    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=categorized_expenses.csv"
        }
    )
