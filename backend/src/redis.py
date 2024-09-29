import redis,sys,os
from src.utils.exception import customException
from src.utils.logger import logging
from src.data.supabase import Supabase

class Redis:
    def __init__(self):
        '''
        Initialize the Redis class.
        '''
        self.host = os.getenv("CLIENT_HOST_DEPLOY")
        self.port = int(os.getenv("CLIENT_PORT"))
        self.db = int(os.getenv("CLIENT_DB"))
        self.client = redis.Redis(host=self.host, port=self.port, db=self.db, decode_responses=True)
        self.supabase = Supabase()
        self.cache_key=os.getenv("CACHE_KEY")
        self.offset_key=os.getenv("OFFSET_KEY")
    
    def fetch_and_cache_products(self,limit: int, offset: int):
        '''
        Fetch products from Supabase and cache them in Redis.
        '''
        products = self.supabase.fetch_products(limit,offset)

        if products:
            # Cache the products in Redis as a list
            self.client.delete(self.cache_key)  # Clear previous cache
            self.client.rpush(self.cache_key, *[str(product) for product in products])  # Add new products to the Redis list

            # Update the offset in Redis
            self.client.set(self.offset_key, offset + limit,ex=300)
        
        return products
    