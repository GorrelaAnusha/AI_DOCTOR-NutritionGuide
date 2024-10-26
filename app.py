# Import necessary libraries
from dotenv import load_dotenv
import os
import google.generativeai as genai
from PIL import Image
import streamlit as st


# Load API Key
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Google Gemini Pro model and get a diet response
def get_response_diet(prompt, input_text):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([prompt, input_text])
    return response.text

# Function to load Google Gemini Vision model and get a nutrition response
def get_response_nutrition(image_data, prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([image_data, prompt])
    return response.text

# Preprocess image data
def prep_image(uploaded_file):
    if uploaded_file is not None:
        # Read the file as bytes
        bytes_data = uploaded_file.getvalue()
        # Prepare the image data for the Gemini Vision model
        image_data = {
            "mime_type": uploaded_file.type,
            "data": bytes_data
        }
        return image_data
    else:
        raise FileNotFoundError("No File is uploaded!")

# Configure Streamlit App
st.set_page_config(page_title="Health Management(AI_DOCTOR): Nutrition Calculator & Diet Planner")
st.image('healthy.jpg', width=100)
st.header("AI_DOCTOR: Nutrition Calculator & Diet Planner")

######################################################################################
section_choice1 = st.radio("Choose Section:", ("Nutrition Calculator", "Diet Planner"))

# If choice is nutrition calculator
if section_choice1 == "Nutrition Calculator":
    upload_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if upload_file is not None:
        # Show the uploaded image
        image = Image.open(upload_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

    # Prompt template for nutrition calculator
    input_prompt_nutrition = """
    You are an expert Nutritionist. Analyze the food items in the image and determine the total nutritional value.
    Provide a breakdown of each food item along with its respective content.

    Format: Food item, Serving size, Total Cal., Protein (g), Fat (g),
    Carbohydrate (g), Fiber (g), Vitamin B-12, Vitamin B-6, Iron, Zinc, Magnesium.

    Use a table format to show the information.
    """
    # Button to calculate nutrition value
    submit = st.button("Calculate Nutrition Value!")
    if submit and upload_file:
        try:
            image_data = prep_image(upload_file)
            response = get_response_nutrition(image_data, input_prompt_nutrition)
            st.subheader("Nutrition AI:")
            st.write(response)
        except Exception as e:
            st.error(f"Error processing image: {e}")

# If choice is diet planner
if section_choice1 == "Diet Planner":
    # Prompt template for diet planner
    input_prompt_diet = """
    You are an expert Nutritionist. 
    - If the input contains a list of food items (e.g., fruits or vegetables), suggest a diet plan with recommendations for breakfast, lunch, and dinner using the given items.
    - If the input contains a calorie amount, suggest a daily diet plan with breakfast, lunch, and dinner within the specified calorie range.

    Return the response in markdown format.
    """
    # Text area for diet input
    input_diet = st.text_area("Input a list of items you have at home or the daily calorie intake goal:")
    submit1 = st.button("Plan my Diet!")
    if submit1 and input_diet:
        response = get_response_diet(input_prompt_diet, input_diet)
        st.subheader("Diet AI:")
        st.write(response)
