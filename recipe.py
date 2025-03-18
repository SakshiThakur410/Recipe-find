import streamlit as st
import requests
import json

# Replace this with your actual Gemini API endpoint URL.
GEMINI_API_URL = "https://api.gemini.com/v1/recipe_suggestions"

def get_recipe_suggestions(prompt, ingredients, dietary_pref, max_time):
    """
    Call the Gemini API to fetch recipe suggestions.
    This function sends a POST request to the API endpoint with the user inputs.
    """
    # Construct the payload for the API request.
    payload = {
        "prompt": prompt,
        "ingredients": ingredients,
        "dietary_preference": dietary_pref if dietary_pref != "None" else None,
        "max_time": max_time
    }
    
    try:
        response = requests.post(GEMINI_API_URL, json=payload)
        response.raise_for_status()  # Raise an error for bad status codes.
        data = response.json()
        # Assuming the API returns a JSON object with a "recipes" key.
        return data.get("recipes", [])
    except requests.RequestException as e:
        st.error(f"Error contacting Gemini API: {e}")
        return []

def main():
    st.title("Quick Indian Food Recipe Suggester")
    st.write("Provide a prompt and available ingredients to get quick, delicious Indian food recipes.")

    # Input for textual prompt
    prompt = st.text_input("Enter your prompt", placeholder="E.g., 'I want a spicy, quick dinner recipe'")

    # Input for ingredients
    ingredients_input = st.text_area("Enter available ingredients (comma separated)", 
                                     placeholder="E.g., tomato, onion, paneer, chickpeas")

    # Input for dietary preferences
    dietary_options = ["None", "Vegetarian", "Vegan", "Gluten-Free", "Low-Carb"]
    dietary_pref = st.selectbox("Select Dietary Preference", options=dietary_options)

    # Input for maximum preparation time
    max_time = st.slider("Select maximum preparation time (minutes)", min_value=5, max_value=120, value=30)

    if st.button("Suggest Recipes"):
        # Process ingredients input
        ingredients = [ingredient.strip() for ingredient in ingredients_input.split(",") if ingredient.strip()]
        
        st.write("### Your Input:")
        st.write("**Prompt:**", prompt)
        st.write("**Ingredients:**", ingredients)
        st.write("**Dietary Preference:**", dietary_pref)
        st.write("**Max Prep Time:**", f"{max_time} minutes")
        
        # Get recipe suggestions from Gemini API
        recipes = get_recipe_suggestions(prompt, ingredients, dietary_pref, max_time)
        
        if recipes:
            st.write("### Suggested Recipes:")
            for recipe in recipes:
                st.subheader(recipe.get("name", "Unnamed Recipe"))
                st.write("**Estimated Preparation Time:**", f"{recipe.get('prep_time', 'N/A')} minutes")
                st.write("**Cooking Steps:**")
                steps = recipe.get("steps", [])
                if steps:
                    for step in steps:
                        st.write("-", step)
                else:
                    st.write("No steps provided.")
        else:
            st.write("No recipes found matching your criteria.")

if __name__ == '__main__':
    main()
