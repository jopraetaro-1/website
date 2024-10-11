from databases import Database
import asyncio

POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "temp"
POSTGRES_DB = "postgres"

database = Database(f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@localhost/{POSTGRES_DB}')

async def connect_db():
    await database.connect()
    print("Database connected")

async def disconnect_db():
    await database.disconnect()
    print("Database disconnected")

# Function to select data from a table
async def select_data():
    query = "SELECT * FROM customers"
    rows = await database.fetch_all(query)
    for row in rows:
        print(dict(row))  # Prints each row in the result

# Function to insert data into the customers table
async def insert_customers(first_name, last_name, email, password, phone_number):
    query = """
    INSERT INTO customers (first_name, last_name, email, password, phone_number)
    VALUES (:first_name, :last_name, :email, :password, :phone_number)
    RETURNING customer_id, first_name, last_name, email, password, phone_number
    """
    # Convert phone_number to string
    phone_number = str(phone_number)

    values = {"first_name": first_name, "last_name": last_name, "email": email, "password": password, "phone_number": phone_number}
    try:
        result = await database.fetch_one(query=query, values=values)
        print(f"Inserted customer ID: {result['customer_id']}")
    except Exception as e:
        print(f"Error inserting customer: {e}")

# Function to update a customer
async def update_customers(customer_id, first_name=None, last_name=None, email=None, password=None, phone_number=None):
    query = "UPDATE customers SET "
    values = {"customer_id": customer_id}

    update_fields = []
    if first_name is not None:
        update_fields.append("first_name = :first_name")
        values["first_name"] = first_name
    if last_name is not None:
        update_fields.append("last_name = :last_name")
        values["last_name"] = last_name
    if email is not None:
        update_fields.append("email = :email")
        values["email"] = email
    if password is not None:
        update_fields.append("password = :password")
        values["password"] = password
    if phone_number is not None:
        update_fields.append("phone_number = :phone_number")
        values["phone_number"] = phone_number

    query += ", ".join(update_fields) + " WHERE customer_id = :customer_id RETURNING *"
    try:
        updated_row = await database.fetch_one(query=query, values=values)
        if updated_row:
            print(f"Updated customer: {dict(updated_row)}")
        else:
            print(f"No customer found with ID: {customer_id}")
    except Exception as e:
        print(f"Error updating customer: {e}")

# Function to delete a customer
async def delete_customers(customer_id):
    query = "DELETE FROM customers WHERE customer_id = :customer_id RETURNING *"
    values = {"customer_id": customer_id}
    try:
        deleted_row = await database.fetch_one(query=query, values=values)
        if deleted_row:
            print(f"Deleted customer: {dict(deleted_row)}")
        else:
            print(f"No customer found with ID: {customer_id}")
    except Exception as e:
        print(f"Error deleting customer: {e}")

# Main function to run async functions
async def main():
    try:
        await connect_db()
        
        # Example operations:
        # await insert_customers('John', 'Doe', 'john@example.com', 'password123', 1234567890)
        # await select_data()
        await update_customers(1, first_name="Jane")
        # await delete_customers(1)
    finally:
        await disconnect_db()

if __name__ == "__main__":
    asyncio.run(main())
