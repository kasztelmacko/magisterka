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
    user_id = data[0]['person_id']
    return user_id

def insert_direct_survey(rect1, rect2, rect3, rect4, rect5, wtp, person_id):
    new_direct_survey = {
        "rect1": rect1,
        "rect2": rect2,
        "rect3": rect3,
        "rect4": rect4,
        "rect5": rect5,
        "wtp": wtp,
        "person_id": person_id
    }
    response = supabase.table("direct_survey").insert(new_direct_survey).execute()
    return response

def select_items(item_id_list=None):
    query = supabase.table("items").select("*")

    if item_id_list:
        query = query.in_("item_id", item_id_list)
    
    response = query.execute()

    items = response.data
    return items


