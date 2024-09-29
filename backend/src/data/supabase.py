import os
from supabase import create_client, Client
import mimetypes
from dotenv import load_dotenv

load_dotenv()

class Supabase:
    def __init__(self):
        '''
        Initialize the Supabase client with your project's URL and key.
        '''
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        self.client= create_client(self.url, self.key)

    def upload_image(self,image_path,image_name):
        '''
        Uploads an image to the Supabase storage bucket.
        '''
        mime_type, _ = mimetypes.guess_type(image_path)
        
        # Read the image data as binary
        with open(image_path, "rb") as f:
            image_data = f.read()
        
        # Upload to Supabase bucket
        response = self.client.storage.from_('fashion_products_images').upload(f"fashion_products_images/{image_name}", image_data, {
            "content-type": mime_type
        })
        
        if response.status_code == 200:
            # Return the public URL of the uploaded image
            return f"{self.url}/storage/v1/object/public/your_bucket_name/fashion_images/{image_name}"
        else:
            print(f"Failed to upload {image_name}: {response.text}")
            return None

    def insert_fashion_item(self,data):
        '''
        Inserts a fashion item into the Supabase table.
        '''
        response = self.client.table("fashion_items").insert(data).execute()
        if response:
            print(f"Inserted {data['name']} successfully!")
        else:
            print(f"Failed to insert {data['name']}: {response.text}")
    
    def fetch_products(self,limit: int, offset: int):
        '''
        Fetches products from the Supabase table.
        '''
        response = self.client.table("fashion_items").select("*").range(offset, offset + limit - 1).execute()
        products = response.data
        return products