import streamlit as st
import google.generativeai as genai
import os

# Set page config
st.set_page_config(
    page_title="Fitness Content Generator",
    page_icon=":weight_lifter:",
    layout="wide",
    initial_sidebar_state="expanded",
)

api_key = "AIzaSyD3EwDSjOjYp0ag5PaWdxqfe_f1n3qvLn0"  # Replace with your actual API key
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
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE",
    },
]

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    safety_settings=safety_settings,
    generation_config=generation_config,
)

# Define the multi-level prompting function
def multi_level_prompting():
    # Title
    st.title("Fitness Content Generator")

    # Main container with background image
    main_bg = """
        <style>
        body {
            background-image: url('gym.jpg');
            background-size: cover;
        }
        </style>
        """
    st.markdown(main_bg, unsafe_allow_html=True)

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


# Run the multi-level prompting function
if __name__ == "__main__":
    multi_level_prompting()
