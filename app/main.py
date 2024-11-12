from fastapi import FastAPI, HTTPException
from typing import List
from app.models.user import User, UserUpdate
from app.database.mongodb import get_collection
from app.data.initial_data import INITIAL_DATA

app = FastAPI(
    title="User Management API",
    description="API for managing user data with MongoDB",
    version="1.0.0"
)

# Get MongoDB collection
collection = get_collection()

# Insert initial data on startup
@app.on_event("startup")
async def insert_initial_data():
    try:
        # Clear existing data
        collection.delete_many({})
        
        # Insert the new data
        collection.insert_many(INITIAL_DATA)
        print("Initial data inserted successfully!")
    except Exception as e:
        print(f"Error inserting initial data: {e}")

# Root route
@app.get("/")
async def root():
    return {
        "message": "Welcome to User Management API",
        "endpoints": {
            "GET /users": "Get all users",
            "PUT /users/{phone_number}": "Update a user"
        }
    }

# GET endpoint to retrieve all users
@app.get("/users/", response_model=List[User])
async def get_all_users():
    try:
        users = list(collection.find({}, {"_id": 0}))
        return users
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# PUT endpoint to update user details (except phone number)
@app.put("/users/{phone_number}", response_model=User)
async def update_user(phone_number: str, user_update: UserUpdate):
    try:
        # Validate phone number format
        if len(phone_number) != 10 or not phone_number.isdigit():
            raise HTTPException(status_code=400, detail="Invalid phone number format")

        update_data = {k: v for k, v in user_update.dict().items() if v is not None}
        
        if not update_data:
            raise HTTPException(status_code=400, detail="No valid update data provided")
        
        result = collection.update_one(
            {"Phone_Number": phone_number},
            {"$set": update_data}
        )
        
        if result.matched_count == 0:
            raise HTTPException(status_code=404, detail="User not found")
        
        updated_user = collection.find_one({"Phone_Number": phone_number}, {"_id": 0})
        return updated_user
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)