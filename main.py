import streamlit as st
from profiles import getProfile, createProfile, getNotes
from form_submit import *
from ai import get_macros,askAi


st.title("Fit.me - 1.0 : Your Personal Fitness Pal")

@st.fragment()
def personalData_form():
    with st.form("personal_data"):
        st.header("Personal Data")
        
        profile = st.session_state.profile

        name=st.text_input("Name", value=profile["general"]["name"])

        age=st.number_input("Age",value=profile["general"]["age"], min_value=0,max_value=120, step=1)

        height=st.number_input(
            "Height (cm)",
            value=float(profile["general"]["height"]),
            min_value=0.0,
            step=0.1, 
            max_value=250.0
            )

        weight=st.number_input(
            "Weight (kg)",
            value=float(profile["general"]["weight"]),
            min_value=0.0,
            max_value=300.0, 
            step=0.1
            )

        genders = ['Male','Female','Other']
        gender = st.radio('Gender',genders ,genders.index(profile["general"].get("gender","Male")))

        activities = ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Super Active"]
        activity_level = st.selectbox("Activity Level", activities,activities.index(profile["general"].get("activity_level","Moderately Active")))

        personal_data_submit = st.form_submit_button("Save")
        if personal_data_submit:
            if all([name, age, weight, height, gender, activity_level]):
                with st.spinner("Saving..."):
                    st.session_state.profile = update_personal_info(profile, "general", name = name, weight = weight, height = height, gender = gender, age = age, activity_level = activity_level)
                    st.success("Personal data saved successfully!")
            else:
                st.warning("Please fill in all fields.")
@st.fragment()
def goals_form():
    profile = st.session_state.profile
    with st.form("goals_forms"):
        st.header("Your Goals")
        goals = st.multiselect(
            "Select your goals:", 
            ["Muscle Gain", "Fat Loss", "Endurance", "Flexibility"], default=profile.get("goals", ["Muscle Gain"])
            )
        goals_submit = st.form_submit_button("Save")

        if goals_submit:
            if goals:
                with st.spinner("Saving..."):
                    st.session_state.profile = update_personal_info(profile, "goals", goals=goals)
                    st.success("Goals saved successfully!")
            else:
                st.warning("Please select at least one goal.")

@st.fragment()
def macros():
    profile = st.session_state.profile
    nutrition = st.container(border = True)
    nutrition.header("Macros")

    if nutrition.button("Generate with Fit-Pal"):
        result = get_macros(profile.get("general"),profile.get("goals"))
        profile["nutrition"] = result
        nutrition.success("Fit-Pal generated your macros successfully!")
        st.session_state.profile = profile
    with nutrition.form("Nutrition_Form", border=False):
        col1,col2,col3,col4 = st.columns(4)
        with col1:
            calories = st.number_input(
                "Calories (kcal)", 
                min_value=0,
                value=profile["nutrition"].get("calories", 2000),
                step=1
                )
        with col2:
            protein = st.number_input(
                "Protein (g)", 
                min_value=0,
                value=profile["nutrition"].get("protein", 100),
                step=1
                )
        with col3:
            fat = st.number_input(
                "Fat (g)", 
                min_value=0,
                value=profile["nutrition"].get("fat", 50),
                step=1
                )
        with col4:
            carbs = st.number_input(
                "Carbs (g)", 
                min_value=0,
                value=profile["nutrition"].get("carbs", 100),
                step=1
                )

        if st.form_submit_button("Save"):
            if all([calories, protein, fat, carbs]):
                with st.spinner("Saving..."):
                    st.session_state.profile = update_personal_info(
                        profile, 
                        "nutrition", 
                        calories=calories, 
                        protein=protein, 
                        fat=fat, 
                        carbs=carbs
                        )
                    st.success("Nutrition data saved successfully!")
            else:
                st.warning("Please fill in all fields.")

@st.fragment()
def notes():
    st.subheader("Notes")
    st.session_state.notes = list(notes_collection.find({}))
    for i, note in enumerate(st.session_state.notes):
        cols = st.columns([5, 1])
        with cols[0]:
            st.text(note.get("text"))
        with cols[1]:
            if st.button("Delete", key=i):
                with st.spinner("Deleting..."):
                    delete_note(note.get("_id"))
                    st.session_state.notes.pop(i)
                    st.rerun()
                    
    new_note = st.text_input("Add a new note : ")

    if st.button("Add Note"):
        if new_note:
            with st.spinner("Adding..."):
                note = add_notes(new_note, st.session_state.profile_id)
                st.session_state.notes.append(note)
                st.success("Note added successfully!")
                st.rerun()
        else:
            st.warning("Please enter a note.")

@st.fragment()
def askFitPal():
    st.subheader("Need help? Ask Fit-Pal!")
    question = st.text_input("Ask Fit-Pal for anything you need:")
    if st.button("Ask Fit-Pal"):
        if question:
            with st.spinner("Asking Fit-Pal..."):
                result = askAi(st.session_state.profile, question)
                st.success("Fit-Pal answered your question!")
                st.write(result)
        else:
            st.warning("Please enter a question.")

def forms():
    if "profile" not in st.session_state:
        profile_id = 1
        profile = getProfile(profile_id)
        if not profile:
            profile_id,profile = createProfile(profile_id)
        
        st.session_state.profile = profile
        st.session_state.profile_id = profile_id

    if "notes" not in st.session_state:
        st.session_state.notes = getNotes(st.session_state.profile_id)

    personalData_form()
    goals_form()
    macros()
    notes()
    askFitPal()
if __name__ == "__main__":
    forms()