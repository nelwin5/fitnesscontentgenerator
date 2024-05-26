import streamlit as st
import google.generativeai as genai
import base64

#Favicon and title
st.set_page_config(page_title="FitGen", page_icon="images/logo.png")

# API key
api_key = "AIzaSyD3EwDSjOjYp0ag5PaWdxqfe_f1n3qvLn0"
genai.configure(api_key=api_key)

# Initialize the generative model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    safety_settings=safety_settings,
    generation_config=generation_config,
)

@st.cache_data()
def get_img_as_base64(file):
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Styling and background
background_img = get_img_as_base64("images/background.jpg")
logo_img = get_img_as_base64("images/logo.png")
favicon_img = get_img_as_base64("images/logo.png")

page_bg_img = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Archivo:wght@400;700&display=swap');

[data-testid="stAppViewContainer"] > .main {{
background-image: url("data:image/png;base64,{background_img}");
background-position: center; 
background-repeat: no-repeat;
background-attachment: fixed;
background-size: cover;
font-family: 'Archivo', sans-serif;
}}

[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}

h1, h2, h3, h4, h5, h6 {{
color: white;
font-family: 'Archivo', sans-serif;
}}

[data-testid="stMarkdownContainer"] {{
color: white;
font-family: 'Archivo', sans-serif;
}}

div[data-baseweb="select"] > div {{
background-color: #333333;
color: white;
border-radius: 5px;
padding: 10px;
font-family: 'Archivo', sans-serif;
}}
</style>
<link rel="icon" href="data:image/x-icon;base64,{favicon_img}">
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

# Define the multi-level prompting function
def multi_level_prompting():
    
    # Logo Image
    st.markdown(f'<img src="data:image/png;base64,{logo_img}" alt="logo" style="position: fixed; top: 20px; left: 20px; width: 150px; z-index: 9999;">', unsafe_allow_html=True)

    # Content and description
    st.title("FitGen: Your Personalized Fitness Content Creator")
    st.subheader("Final Project in CCS 229 - Intelligent Systems")
    st.subheader("Nelwin J. Serra  BSCS 3B")
    st.write("This project generates personalized fitness content, including workout plans, nutrition guides, tips, and motivational stories, based on user preferences, using a generative AI model.")
   
    # Level 1 Prompt
    st.header("Step 1: Choose a type of fitness content")
    content_type = st.selectbox(
        "Select a type:",
        ["Workout Plan", "Nutrition Guide", "Fitness Tips", "Motivational Story"],
    )

    # Level 2 Prompt
    if content_type:
        st.header(f"Step 2: Refine your {content_type}")
        if content_type == "Workout Plan":
            workout_type = st.selectbox(
                "Select a workout type:",
                ["Strength Training", "Cardio", "Flexibility", "HIIT"],
            )
        elif content_type == "Nutrition Guide":
            goal = st.selectbox(
                "Select a goal:",
                ["Weight Loss", "Muscle Gain", "Maintenance", "Vegan Diet"],
            )
        elif content_type == "Fitness Tips":
            focus_area = st.selectbox(
                "Select a focus area:",
                ["General Health", "Endurance", "Recovery", "Mental Wellness"],
            )
        elif content_type == "Motivational Story":
            theme = st.selectbox(
                "Select a theme:",
                ["Overcoming Challenges", "Achieving Goals", "Daily Motivation", "Success Story"],
            )

        # Final Prompt and Generation
        if st.button("Generate Fitness Content", key="generate_button"):
            chat_session = model.start_chat(history=[])
            if content_type == "Workout Plan":
                input_text = f"Create a {workout_type} workout plan."
            elif content_type == "Nutrition Guide":
                input_text = f"Write a nutrition guide for {goal}."
            elif content_type == "Fitness Tips":
                input_text = f"Give fitness tips focused on {focus_area}."
            elif content_type == "Motivational Story":
                input_text = f"Write a motivational story about {theme}."

            response = chat_session.send_message(input_text)
            st.subheader("Generated Fitness Content")
            st.write(response.text)

            # Option to generate another different result
            if st.button("Generate Another Result"):
                multi_level_prompting()  # Start the process again

# Run the multi-level prompting function
if __name__ == "__main__":
    multi_level_prompting()
