from db import personal_data_collection, notes_collection

def getValues(_id):
    #just starting vals
    return {
        "_id": _id, 
        "general": {
            "name": "",
            "age": 30,
            "weight": 60,
            "height": 165,
            "activity_level": "Moderately Active",
            "gender": "Male"
        },
        "goals": ["Muscle Gain"],
        "nutrition": {
            "calories": 2000,
            "protein": 140,
            "fat": 20,
            "carbs": 100,
            },
    }

def createProfile(_id):
    profile_values = getValues(_id)
    result = personal_data_collection.insert_one(profile_values)
    return result.inserted_id, result

def getProfile(_id):
    profile = personal_data_collection.find_one({"_id": {"$eq": _id}})
    return profile

def getNotes(_id):
    return notes_collection.find({"_id": {"$eq": _id}})