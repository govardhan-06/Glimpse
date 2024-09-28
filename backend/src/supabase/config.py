import os,sys
from supabase import create_client, Client
from dataclasses import dataclass
from dotenv import load_dotenv
from backend.src.utils.exception import customException
from backend.src.utils.logger import logging

@dataclass
class Supabase_config:
    load_dotenv()
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")

class Supabase:
    def __init__(self):
        self.config=Supabase_config()
        self.supabase: Client = create_client(self.config.SUPABASE_URL, self.config.SUPABASE_KEY)
    
    def insert_data(self,user:dict):
        '''
        Insert data into supabase database
        '''
        try:
            response = (self.supabase.table("fashion_items")
                        .insert(user)
                        .execute()
                        )
            logging.info(f"Inserted data into supabase.")
            return response
        except Exception as e:
            logging.error(f"Error inserting data into supabase: {e}")
            raise customException(e,sys)


        
    
    
