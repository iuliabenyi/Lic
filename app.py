import flask
from flask import render_template, redirect, url_for, flash
from nltk_utils import stem
from usersTable import usersTable
from werkzeug.security import generate_password_hash, check_password_hash
from login import *
from chat import *

isLoggedIn = False
currUser = User()
bot_response = ""
bot_response2 = ""
tagName = []

@app.route('/', methods=['GET', 'POST'])
def homePage():
    if flask.request.method == 'GET':
        return render_template("home_page.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    global isLoggedIn
    global currUser
    if flask.request.method == 'GET':
        return render_template("login.html")
    # here if action = login and method = POST thee log in works but the chat page throws an error

    email = request.form.get('email')
    password = request.form.get('password')
    type = request.form.get('type')
    remember = True if request.form.get('remember') else False
    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('login'))  # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    isLoggedIn = True
    currUser = user

    if request.form['loginBtn'] == 'Log in as user':
        return redirect(url_for('chat'))
    elif request.form['loginBtn'] == 'Log in as therapist':
        return redirect(url_for('therapist'))
'''
@app.route('/therapist')
def therapist():
    index = open("templates/therapist_page.html").read().format(therName=currUser.name, table=table)
    return index'''

@app.route('/therapist')
def therapist():
    results = User.query.all()
    #print(results)
    if not results:
        return redirect(url_for('homePage'))
    else:
        table = usersTable(results)
        table.border = True
        #print(table.__html__())
        index = open("templates/therapist_page.html").read().format(therName=currUser.name, table=table.__html__())
        return index

@app.route('/protected')
def protected():
    if isLoggedIn:
        return 'Logged in as: ' + currUser.name
    else:
        return 'Not logged in'

@app.route('/logout')
def logout():
    global isLoggedIn
    #flask_login.logout_user()
    isLoggedIn = False
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup_post():
    if flask.request.method == 'GET':
        return render_template("signup.html")
    else:
        email = flask.request.form['email']
        name = flask.request.form['name']
        password = flask.request.form['password']

        user = User.query.filter_by(email=email).first()  # if this returns a user, then the email already exists in database
        if user:  # if a user is found, we want to redirect back to signup page so user can try again
            return redirect(url_for('signup_post'))

        new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))


@app.route('/finish')
def finish():
    """s = ""
    if flask.request.method == 'GET':
        '''if bot_response != "null":
            for t in tagName:
                s = s + " " + t
            return s
        else:'''
        return render_template("conclusion_page.html")
    else:
        return redirect(url_for('login'))"""
    index = open("templates/final_page.html").read().format(userName=currUser.name, tags=tagName)
    return index

@app.route('/tags')
def tags():
    s = ""
    for t in tagName :
        s += t + ","

    return s








@app.route('/chat')
def chat():
    return render_template("index.html")

@app.route("/userName")
def get_user_name():
    return currUser.name

@app.route("/get")
def get_bot_response():
    global bot_response
    global tagName
    userInput = request.args.get('msg')
    userText = tokenize(userInput)
    X = bag_of_words(userText, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                # print(f"{bot_name}: {random.choice(intent['responses'])}")
                bot_response = random.choice(intent['responses'])
                tagName.append(tag)

    else:
        # print(f"{bot_name}: I do not understand...")
        bot_response = "I do not understand"
    return bot_response


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()




if __name__ == "__main__":
    app.run()