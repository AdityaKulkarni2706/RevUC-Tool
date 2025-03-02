import requests
import google.generativeai as genai 


genai.configure(api_key="AIzaSyDz84wYj5_VvDnt8Mp_8lFY2-QiMs819TQ")
model = genai.GenerativeModel("gemini-1.5-flash")

def generate_recipe(ingredients):
    prompt = f"Generate me a recipe which has : [Name of the dish, Prep time, Ingredients, Instructions] with the following ingredients : {ingredients}. Do not use any hashes or anything at all for styling, this is IMPORTANT, try to use only the specified ingredients"


    response = model.generate_content(prompt)
    return response.text

