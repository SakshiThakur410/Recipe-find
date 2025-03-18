import streamlit as st
import requests

# Gemini endpoint provided by Google Generative Language API.
# Here we assume the full endpoint with method suffix ":generate" is required.
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generate"

def get_recipe_suggestions(prompt, ingredients, dietary_pref, max_time, api_key):
    """
    Calls the Gemini API to fetch recipe suggestions.
    
    Combines the user's prompt, ingredients, dietary preference, and maximum prep time
    into a full prompt, then sends a POST request to the Gemini API endpoint.
    
    The API key is passed as a query parameter (common for Google Cloud APIs).
    Adjust the payload and response parsing based on the official API docs.
    """
    # Build a comprehensive prompt from user inputs
    full_prompt = (
        f"{prompt}\n\n"
        f"Ingredients: {', '.join(ingredients)}\n"
        f"Dietary Preference: {dietary_pref}\n"
        f"Maximum Preparation Time: {max_time} minutes\n\n"
        "Please provide a quick, delicious Indian recipe along with step-by-step cooking instructions."
    )
    
    # Construct the payload. Adjust keys based on the API documentation.
    payload = {
        "prompt": {
            "text": full_prompt
        },
        "temperature": 0.7,          # Adjust temperature as needed
        "max_output_tokens": 256     # Adjust token limit as needed
    }
    
    # Pass the API key as a query parameter.
    params = {"key": api_key}
    
    try:
        response = requests.post(GEMINI_API_URL, json=payload, params=params)
        response.raise_for_status()
        data = response.json()
        # Here we assume the API returns a list of candidate outputs under "candidates"
        # Each candidate is assumed to have an "output" field with the recipe text.
        candidates = data.get("candidates", [])
        recipes = []
        for candidate in candidates:
            # Create a simple recipe structure; adjust as needed.
            recipes.append({
                "name": "Generated Recipe",
                "details": candidate.get("output", "No details provided.")
            })
        return recipes
    except requests.RequestException as e:
        st.error(f"Error contacting Gemini API: {e}")
        return []

def main():
    st.title("Quick Indian Food Recipe Suggester using Gemini")
    st.write("Provide a prompt and available ingredients to get quick, delicious Indian food recipes, powered by Google Gemini API.")
    
    # Input fields for user data
    prompt = st.text_input("Enter your prompt", placeholder="E.g., 'I want a spicy, quick dinner recipe'")
    ingredients_input = st.text_area("Enter available ingredients (comma separated)", 
                                     placeholder="E.g., tomato, onion, paneer, chickpeas")
    dietary_options = ["None", "Vegetarian", "Vegan", "Gluten-Free", "Low-Carb"]
    dietary_pref = st.selectbox("Select Dietary Preference", options=dietary_options)
    max_time = st.slider("Select maximum preparation time (minutes)", min_value=5, max_value=120, value=16)
    
    # Retrieve the Gemini API key from Streamlit secrets.
    gemini_api_key = st.secrets["api_keys"]["gemini"]
    
    if st.button("Suggest Recipes"):
        # Process the ingredients input into a list
        ingredients = [ingredient.strip() for ingredient in ingredients_input.split(",") if ingredient.strip()]
        
        st.write("### Your Input:")
        st.write("**Prompt:**", prompt)
        st.write("**Ingredients:**", ingredients)
        st.write("**Dietary Preference:**", dietary_pref)
        st.write("**Max Prep Time:**", f"{max_time} minutes")
        
        # Get recipe suggestions from the Gemini API
        recipes = get_recipe_suggestions(prompt, ingredients, dietary_pref, max_time, gemini_api_key)
        
        if recipes:
            st.write("### Suggested Recipes:")
            for recipe in recipes:
                st.subheader(recipe.get("name", "Generated Recipe"))
                st.write(recipe.get("details", "No details provided."))
        else:
            st.write("No recipes found matching your criteria.")

if __name__ == "__main__":
    main()
