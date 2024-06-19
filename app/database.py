import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SECRET_KEY = os.getenv("SUPABASE_SECRET_KEY")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SECRET_KEY)

def insert_person(age, gender, education, city_size, income, dining_freq):
    new_person = {
        "age": age,
        "gender": gender,
        "education": education,
        "city_size": city_size,
        "income": income,
        "dining_freq": dining_freq
    }

    response = supabase.table("people").insert(new_person).execute()
    
    data = response.data
    user_id = data[0]['id']
    return user_id

