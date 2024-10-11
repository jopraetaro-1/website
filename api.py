from typing import Union
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Define a Pydantic model for a product
class Product(BaseModel):
    name: str
    price: int
    size: str
    color: str
    stock: int

# In-memory database (rename to avoid conflict with the model)
products_db = {}

@app.get("/")
def read_root():
    return {"Hello": "World"}

# GET method to read a product by product_id
@app.get("/products/{product_id}")
def read_item(product_id: int, q: Union[str, None] = None):
    if product_id in products_db:
        return {"product_id": product_id, "product": products_db[product_id], "q": q}
    raise HTTPException(status_code=404, detail="Product not found")

# POST method to create a new product
@app.post("/products/{product_id}")
def create_product(product_id: int, product: Product):
    if product_id in products_db:
        raise HTTPException(status_code=400, detail="Product already exists")
    products_db[product_id] = product
    return {"product_id": product_id, "product": product}

# PUT method to update an existing product
@app.put("/products/{product_id}")
def update_item(product_id: int, product: Product):
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    products_db[product_id] = product
    return {"product_id": product_id, "product": product}

# DELETE method to delete a product
@app.delete("/products/{product_id}")
def delete_item(product_id: int):
    if product_id not in products_db:
        raise HTTPException(status_code=404, detail="Product not found")
    del products_db[product_id]
    return {"detail": "Product deleted"}
