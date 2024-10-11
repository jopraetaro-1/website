from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from database import *

app = FastAPI()

# Pydantic model for user creation
class CustomerCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    password: str
    phone_number: int

# Pydantic model for user update
class CustomersUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    password: Optional[str]
    phone_number: Optional[int]  # Ensure consistency with the type in CustomerCreate

# Pydantic model for user response
class Customer(BaseModel):
    customer_id: int  # Fixed typo from 'cutomer_id'
    first_name: str
    last_name: str
    email: str
    password: str
    phone_number: int
    created_at: datetime

# Connect to the database on startup
@app.on_event("startup")
async def startup():
    await connect_db()

# Disconnect from the database on shutdown
@app.on_event("shutdown")
async def shutdown():
    await disconnect_db()

# Endpoint to create a new user
@app.post("/customers/", response_model=Customer)
async def create_customer(customer: CustomerCreate):
    result = await insert_customer(customer.first_name, customer.last_name, customer.email, customer.password, customer.phone_number)  # Use customer object
    if result is None:
        raise HTTPException(status_code=400, detail="Error creating user")
    return result

# Endpoint to get a user by user_id
@app.get("/customers/{customer_id}", response_model=Customer)
async def read_customer(customer_id: int):
    result = await get_customer(customer_id)
    if result is None:
        raise HTTPException(status_code=404, detail="customer not found")
    return result

# Endpoint to update a user
@app.put("/customers/{customer_id}", response_model=Customer)
async def update_customer_endpoint(customer_id: int, customer: CustomersUpdate):  # Match with CustomersUpdate model
    result = await update_customer(customer_id, customer.first_name, customer.last_name, customer.email, customer.password, customer.phone_number)  # Use customer object
    if result is None:
        raise HTTPException(status_code=404, detail="customer not found")
    return result

# Endpoint to delete a user
@app.delete("/customers/{customer_id}")
async def delete_user_endpoint(customer_id: int):
    result = await delete_customer(customer_id)
    if result is None:
        raise HTTPException(status_code=404, detail="customer not found")
    return {"detail": "customer deleted"}
