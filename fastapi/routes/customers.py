from fastapi import APIRouter, FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from database import *  # Ensure your database functions are imported


router = APIRouter()


# Pydantic model for user creation
class CustomerCreate(BaseModel):
   first_name: str
   last_name: str
   email: str
   password: str
   phone_number: int


# Pydantic model for user update
class CustomerUpdate(BaseModel):
   first_name: Optional[str]
   last_name: Optional[str]
   email: Optional[str]
   password: Optional[str]
   phone_number: Optional[int]


# Pydantic model for user response
class Customer(BaseModel):
   customer_id: int
   first_name: str
   last_name: str
   email: str
   password: str
   phone_number: int
   created_at: datetime


# Pydantic model for login
class CustomerLogin(BaseModel):
   email: str
   password: str


# Endpoint to create a new user
@router.post("/customers/create", response_model=Customer)
async def create_customer(customer: CustomerCreate):
   # Check if the username already exists
   existing_customer = await get_customer(customer.first_name)
   if existing_customer:
       raise HTTPException(status_code=400, detail="Username already exists")
   
   result = await insert_customer(customer.first_name, customer.last_name,customer.password,customer.email)
   if result is None:
       raise HTTPException(status_code=400, detail="Error creating user")
   return result




# Endpoint to get a user by user_id
@router.get("/customers/{customer_id}", response_model=Customer)
async def read_user(customer_id: int):
   result = await get_customer(customer_id)
   if result is None:
       raise HTTPException(status_code=404, detail="User not found")
   return result


# Endpoint to update a user
@router.put("/customers/{customer_id}", response_model=Customer)
async def update_user_endpoint(customer_id: int, customer: CustomerUpdate):
   result = await update_customer(customer.first_name, customer.last_name,customer.password,customer.email)
   if result is None:
       raise HTTPException(status_code=404, detail="User not found")
   return result


# Endpoint to delete a user
@router.delete("/customers/{customer_id}")
async def delete_user_endpoint(customer_id: int):
   result = await delete_customer(customer_id)
   if result is None:
       raise HTTPException(status_code=404, detail="User not found")
   return {"detail": "Customer deleted"}


# Endpoint for user login
@router.post("/customers/login")
async def login_customer(customer: CustomerLogin):
   # Fetch user from the database
   db_user = await get_customer_by_email(customer.email,customer.password)
  
   if db_user is None:
       raise HTTPException(status_code=404, detail="User not found")


   # If login is successful, you can return user info (omit password hash)
   return {
       "customer_id": db_user.customer_id,
       "first_name": db_user.first_name,
       "last_name": db_user.last_name,
       "email": db_user.email,
       "created_at": db_user.created_at
   }
