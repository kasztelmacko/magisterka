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

def insert_direct_survey(person_id, low_1, poor_1, high_1, low_2, poor_2, high_2, low_7, poor_7, high_7, low_12, poor_12, high_12):
    new_direct_survey = {
        "person_id": person_id,
        "low_1": low_1,
        "poor_1": poor_1,
        "high_1": high_1,
        "low_2": low_2,
        "poor_2": poor_2,
        "high_2": high_2,
        "low_7": low_7,
        "poor_7": poor_7,
        "high_7": high_7,
        "low_12": low_12,
        "poor_12": poor_12,
        "high_12": high_12
    }
    response = supabase.table("direct_survey").insert(new_direct_survey).execute()
    return response

def insert_indirect_survey(rect1, rect2, rect3, rect4, rect5, wtp, person_id):
    new_indirect_survey = {
        "rect1": rect1,
        "rect2": rect2,
        "rect3": rect3,
        "rect4": rect4,
        "rect5": rect5,
        "wtp": wtp,
        "person_id": person_id
    }
    response = supabase.table("indirect_survey").insert(new_indirect_survey).execute()
    return response

def insert_discrete_order(person_id, observation, order_json, order_price, items_json, order_status):
    new_order = {
        "person_id": person_id,
        "observation": observation,
        "order_json": order_json,
        "order_price": order_price,
        "items_json": items_json,
        "order_status": order_status
    }
    response = supabase.table("discrete_orders").insert(new_order).execute()
    return response

def select_items(item_id_list=None):
    query = supabase.table("items").select("*")

    if item_id_list:
        query = query.in_("item_id", item_id_list)
    
    response = query.execute()
    items = response.data

    if item_id_list:
        order_dict = {item_id: index for index, item_id in enumerate(item_id_list)}
        items.sort(key=lambda item: order_dict.get(item['item_id'], float('inf')))
    
    return items


def select_types():
    response = supabase.table("types").select("*").execute()
    types = response.data
    return types


