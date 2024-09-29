import random,os,random,uuid
from src.data.supabase import Supabase
from src.data.synthetic_data import brands,seller_platforms,sizes
from src.data.synthetic_data import kurti_descriptions,kurti_names,crop_top_names,crop_top_descriptions
from dotenv import load_dotenv

load_dotenv()

image_folder = os.getenv("IMAGE_PATH_FOLDER")

def generate_random_fashion_data(image_url):
    return {
        "name": random.choice(crop_top_names),  # Generate a random product name
        "description": random.choice(crop_top_descriptions),# Generate a random description
        "category": "Crop-tops",  # Pick a random category
        "price": round(random.uniform(100.0, 1000.0), 2),
        "size": random.choice(sizes),  # Pick a random size
        "brand": random.choice(brands),  # Pick a random brand
        "stock_qty": random.randint(1, 200),  # Generate a random stock quantity between 1 and 200
        "image": image_url,  # Use the uploaded image URL
        "seller_platform": random.choice(seller_platforms),  # Pick a random seller platform
    }

# Generate unique file name
def generate_unique_filename(image_name):
    unique_id = str(uuid.uuid4())
    file_extension = os.path.splitext(image_name)[1]
    return f"{os.path.splitext(image_name)[0]}_{unique_id}{file_extension}"

def generation():
    supabase=Supabase()
    count=0
    for image_file in os.listdir(image_folder):
        image_path = os.path.join(image_folder, image_file)
        image_name = generate_unique_filename(os.path.basename(image_path))

        if count==20:
            break

        if os.path.isfile(image_path):
            # Upload the image and get its public URL
            image_url = supabase.upload_image(image_path,image_name)
            
            if image_url:
                fashion_item_data = generate_random_fashion_data(image_url)
                
                # Insert the fashion item data into the Supabase table
                supabase.insert_fashion_item(fashion_item_data)
                count=count+1

    print("Data population completed.")

if __name__=="__main__":
    generation()