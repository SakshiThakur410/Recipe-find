import streamlit as st
import google.generativeai as genai
import os
from fpdf import FPDF

# ✅ Load API Key securely
API_KEY = os.getenv("Gen_API")  # Ensure this environment variable is set
if not API_KEY:
    st.error("API Key is missing! Set 'Gen_API' as an environment variable.")
    st.stop()

# ✅ Configure Google Gemini API
genai.configure(api_key=API_KEY)

# ✅ Function to call Gemini API and get recipe suggestions
def get_recipe_suggestions(prompt, ingredients, dietary_pref, max_time):
    model = genai.GenerativeModel("gemini-1.5-flash")  # Using a fast model
    full_prompt = (
        f"{prompt}\n\n"
        f"Ingredients: {', '.join(ingredients)}\n"
        f"Dietary Preference: {dietary_pref}\n"
        f"Max Preparation Time: {max_time} minutes\n\n"
        "Please provide a quick Indian recipe with step-by-step instructions."
    )

    try:
        response = model.generate_content(full_prompt)
        return response.text if response else "No recipe found."
    except Exception as e:
        st.error(f"Error contacting Gemini API: {e}")
        return None

# ✅ Function to create a PDF of the recipe
def generate_pdf(recipe_text):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    
    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(200, 10, "Generated Recipe", ln=True, align="C")
    
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, recipe_text)
    
    pdf_path = "recipe.pdf"
    pdf.output(pdf_path)
    return pdf_path

# ✅ Streamlit UI
def main():
    st.title("Quick Indian Recipe Generator 🍛")
    st.write("Enter a prompt and available ingredients to get a quick Indian recipe!")

    prompt = st.text_input("Enter your prompt", placeholder="E.g., 'I want a spicy, quick dinner recipe'")
    ingredients_input = st.text_area("Enter ingredients (comma separated)", placeholder="Tomato, onion, paneer, chickpeas")
    dietary_options = ["None", "Vegetarian", "Vegan", "Gluten-Free", "Low-Carb"]
    dietary_pref = st.selectbox("Select Dietary Preference", options=dietary_options)
    max_time = st.slider("Max Prep Time (minutes)", min_value=5, max_value=60, value=15)

    if st.button("Generate Recipe"):
        ingredients = [ingredient.strip() for ingredient in ingredients_input.split(",") if ingredient.strip()]
        
        st.write("### Your Input:")
        st.write(f"**Prompt:** {prompt}")
        st.write(f"**Ingredients:** {', '.join(ingredients)}")
        st.write(f"**Dietary Preference:** {dietary_pref}")
        st.write(f"**Max Prep Time:** {max_time} minutes")
        
        # ✅ Get Recipe from Gemini
        recipe = get_recipe_suggestions(prompt, ingredients, dietary_pref, max_time)
        
        if recipe:
            st.write("### Suggested Recipe:")
            st.write(recipe)
            
            # ✅ Generate PDF
            pdf_path = generate_pdf(recipe)
            with open(pdf_path, "rb") as file:
                st.download_button("Download Recipe as PDF", file, file_name="recipe.pdf", mime="application/pdf")
        else:
            st.write("No recipe found. Please try again.")

if __name__ == "__main__":
    main()
