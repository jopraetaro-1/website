from databases import Database


POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "temp"
POSTGRES_DB = "postgres"
POSTGRES_HOST = "localhost"


DATABASE_URL = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}'


database = Database(DATABASE_URL)


async def connect_db():
   await database.connect()
   print("Database connected")


async def disconnect_db():
   await database.disconnect()
   print("Database disconnected")


# Function to insert a new user into the users table
async def insert_customer(first_name: str,last_name:str, email: str,password: str,phone_number: int):
   query = """
   INSERT INTO customers (first_name, last_name, email,password,phone_number)
   VALUES (:first_name, :last_name, :email,:password,:phone_number)
   RETURNING customer_id,first_name, last_name, email,password,phone_number, created_at
   """
   values = {"first_name": first_name, "last_name": last_name, "email": email,"password":password,"phone_number":phone_number}
   return await database.fetch_one(query=query, values=values)


# Function to select a user by user_id from the users table
async def get_customer(first_name: str):
   query = "SELECT * FROM customers WHERE first_name = :first_name"
   return await database.fetch_one(query=query, values={"first_name": first_name})


# Function to select a user by email from the users table
async def get_user_by_email(email: str,password:str):
   query = "SELECT * FROM customers WHERE email = :email and password = :password"
   return await database.fetch_one(query=query, values={"email": email,"password": password})


# Function to update a user in the users table
async def update_customer(customer_id: int, first_name: str,last_name:str, email: str,password: str,phone_number: int):
   query = """
   UPDATE customers
   SET first_name = :username,last_name = :last_name, password = :password, email = :email,phone_number = :phone_number
   WHERE customer_id = :customer_id
   RETURNING customer_id, first_name,last_name, password, email,phone_number, created_at
   """
   values = {"customer_id": customer_id, "first_name": first_name, "last_name": last_name, "email": email,"password":password,"phone_number":phone_number}
   return await database.fetch_one(query=query, values=values)


# Function to delete a user from the users table
async def delete_customer(customer_id: int):
   query = "DELETE FROM customers WHERE customer_id = :customer_id RETURNING *"
   return await database.fetch_one(query=query, values={"customer_id": customer_id})
