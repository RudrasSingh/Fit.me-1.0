import streamlit as st

st.title("Personal Fitness Buddy")

@st.fragment()
def personalData_form():
    with st.form("personal_data"):
        st.header("Personal Data")
        
        name=st.text_input("Name")
        age=st.number_input("Age",min_value=0,max_value=120, step=1)
        height=st.number_input("Height (cm)",min_value=0)
        weight=st.number_input("Weight (kg)",min_value=0.0,max_value=300.0, step=0.1)
        gender = st.radio('Gender', ['Male','Female','Other'])
        activity_level = st.selectbox("Activity Level", ["Sedentary", "Lightly Active", "Moderately Active", "Very Active", "Super Active"])

        personal_data_submit = st.form_submit_button("Save")
        if personal_data_submit:
            if all([name, age, weight, height, gender, activity_level]):
                with st.spinner("Saving..."):
                    st.success("Personal data saved successfully!")
            else:
                st.warning("Please fill in all fields.")
            
def forms():
    personalData_form()

if __name__ == "__main__":
    forms()