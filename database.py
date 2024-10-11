from databases import Database

POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "temp"
POSTGRES_DB = "postgres"

# Corrected connection URL
database = Database(f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost/{POSTGRES_DB}')

async def connect_db():
    await database.connect()
    print("Database connected")

async def disconnect_db():
    await database.disconnect()
    print("Database disconnected")

# Function to insert a new customer into the customers table
async def insert_customer(first_name: str, last_name: str, email: str, password: str, phone_number: int):
    query = """
    INSERT INTO customers (first_name, last_name, email, password, phone_number)
    VALUES (:first_name, :last_name, :email, :password, :phone_number)
    RETURNING customer_id, first_name, last_name, email, password, phone_number, created_at  -- Fixed: added missing comma
    """
    values = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": password,
        "phone_number": phone_number
    }
    return await database.fetch_one(query=query, values=values)

# Function to get a customer by customer_id
async def get_customer(customer_id: int):
    query = "SELECT * FROM customers WHERE customer_id = :customer_id"
    return await database.fetch_one(query=query, values={"customer_id": customer_id})

# Function to update a customer in the customers table
async def update_customer(customer_id: int, first_name: str, last_name: str, email: str, password: str, phone_number: int):
    query = """
    UPDATE customers
    SET first_name = :first_name, last_name = :last_name, email = :email, password = :password, phone_number = :phone_number
    WHERE customer_id = :customer_id
    RETURNING customer_id, first_name, last_name, email, password, phone_number, created_at  -- Fixed: added missing comma
    """
    values = {
        "customer_id": customer_id,
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "password": password,
        "phone_number": phone_number
    }
    return await database.fetch_one(query=query, values=values)

# Function to delete a customer from the customers table
async def delete_customer(customer_id: int):
    query = "DELETE FROM customers WHERE customer_id = :customer_id RETURNING *"
    return await database.fetch_one(query=query, values={"customer_id": customer_id})
