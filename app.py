from flask import Flask, render_template, request, jsonify, session, redirect, url_for, send_file
from flask_cors import CORS
import functions
import image_gen
from PIL import Image
from waitress import serve
import os
import llm


app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = "102394020"
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production


global current_user
@app.route('/')
def main_page():
    print(f"Current session main page: {session}")
    if 'username' in session:
        current_user = session['username']
        return redirect(url_for('render_home'))
    else:
        return redirect(url_for('render_home'))


@app.route('/home')

def render_home():

    return render_template('home.html')


@app.route('/sign_up')

def render_sign_up():
    if 'username' in session:
        return redirect(url_for('main_page'))
    return render_template("signup.html")

@app.route('/login')

def render_log_in():
    if 'username' in session:
        return redirect(url_for('render_home'))
    
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('main_page'))

@app.route('/validate_credentials',  methods = ['POST'])

def validate():


    user_data = request.get_json()

    if not user_data:

        return jsonify({"message" : "Invalid JSON"})  



    username = user_data['username']
    password = user_data['password']

    user_credentials = functions.specific_user_credentials(username)
    if user_credentials!=None:
        real_passwd = user_credentials[-1]
        if password == real_passwd:
            session['username'] = username
            print("This is the checkpoint!")
            print(f"Set session : {session}")
            return jsonify({"message" : "Your password is correct!", "flag" : '1'})
        else:
            return jsonify({"message" : "Your password is not correct!", "flag" : "0"})
        

    else:
        return jsonify({"message" : "user does not exist", "flag" : '2'})     
    


@app.route('/insert_data_into_DB', methods = ["POST",])

def insert_data():

    user_data = request.get_json()
    print(user_data['username'], user_data['password'])
    
    creds = functions.specific_user_credentials(user_data['username'])
    print(creds)
    if creds is None:
        functions.insert_data((user_data['username'], user_data['password']))
        functions.assign_mult_and_score_to_user(user_data['username'])
        

    else:
        return jsonify({"message" : "user already exists", "flag" : '0'})
    

    current_data = functions.select_data(("Username", "Password"))
    print(current_data)
    



    return jsonify({"message" : "inserted data", "flag" : '1'})

@app.route('/render_tool')

def render_tool():
    print(f"Render tool current session : {session}")
    return render_template("image.html")



@app.route('/handle_image', methods = ['POST'])

def ImageHandler():
    print(f"This is request.files : {request.files}")

    if 'image' not in request.files:
        return jsonify({'message': 'no image'})
    

    static_folder = "static"
    
    print(f"This is the current user : {request.form['username']}")
    
    
    generated_image_path = os.path.join(static_folder, "generated_image.jpg")
   
    image = request.files['image']
    
    image_gen.generateArt(image, generated_image_path)
    functions.insert_art_into_data( request.form['username'], generated_image_path)

    print("Checkpoint 1")
    
    print("Checkpoint 2")
    return {"message": "success", "image_url" : f"/{generated_image_path}"}



@app.route('/render_recipe_page')
def render_recipe_page():
    return render_template('recipe.html')

@app.route('/get_score')

def get_score():

    print(session)
    username = session['username']

    score = functions.fetch_score(username)
    
    return {"score" : int(score[0])}


    
    
@app.route('/application', methods = ['POST'])
def get_ing_gen_recipe():
    print('Checkpoint')
    ingredients = request.json
    recipe = llm.generate_recipe(ingredients)
    
    response = {
        "gen_recipe" : recipe
    }
    print(recipe)
    return jsonify(response)

    

    

    


if __name__ == "__main__":
    app.run(debug=True)
