from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
import sys,uvicorn
from backend.src.utils.exception import customException
from backend.src.utils.logger import logging
from starlette.responses import JSONResponse
from backend.src.redis import Redis

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def home():
    '''
    This function is used to redirect to the swaggerUI page.
    '''
    return RedirectResponse(url="/docs")

@app.get("/products")
def get_products():
    redis=Redis()

    # Check if cached products exist in Redis list
    cache_length = redis.client.llen(redis.cache_key)
    
    if cache_length > 0:
        # Pop the first product from the list and send to frontend
        product = redis.client.lpop(redis.cache_key)
        if product:
            return eval(product)  # Convert the string back to dictionary
    else:
        # If Redis list is empty, fetch new products from Supabase and repopulate cache
        offset = int(redis.client.get(redis.offset_key) or 0)
        products = redis.fetch_and_cache_products(limit=50, offset=offset)
        
        # Immediately serve the first product from the new batch
        if products:
            return products[0]  # Return the first product from the new batch

    return {"message": "No products available at the moment."}

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

