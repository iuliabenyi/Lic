from datetime import datetime

import flask
from flask import render_template, redirect, url_for, flash
from messagesTable import messagesTable
from models import UserPage, Users, Messages, UsersAll, Message
from sqlalchemy import update
from usersTable import usersTable
from werkzeug.security import generate_password_hash, check_password_hash
from chat import *

isLoggedIn = False
currUser = UsersAll()
currUserPage = UserPage()
bot_response = ""
tagName = []
inputUserName = ""
currMainTag = ""
message = ""

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

    email = request.form.get('email')
    password = request.form.get('password')
    user = UsersAll.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('login'))

    isLoggedIn = True
    currUser = user
    if currUser.type == "user":
        stmt = (
            update(UsersAll).
                where(UsersAll.name == currUser.name).
                values(lastLogin=datetime.now().__str__())
        )
        return redirect(url_for('chat'))
    elif currUser.type == "therapist":
        return redirect(url_for('therapist'))

@app.route('/therapist', methods=['GET', 'POST'])
def therapist():
    global inputUserName
    results = UsersAll.query.filter_by(type='user').all()
    table = usersTable(results)
    table.border = True
    if flask.request.method == 'GET':
        return render_template("therapist_page.html", therName=currUser.name, table=table)
    if flask.request.method == 'POST':
        inputUserName = request.form.get('userName')
        if request.form['button'] == "See the user's details":
            return redirect(url_for('usersDetails'))


@app.route('/usersDetails', methods=['GET', 'POST'])
def usersDetails():
    resultsMes = []
    resultsUser = []
    resultsMesLast = []
    resultsUserLast = []
    resultsSendMes = []
    resultsSendUser = []
    resultsSendMesLast = []
    resultsSendUserLast = []
    results = Message.query.filter_by(nameReceiver=currUser.name).all()
    resultsSend = Message.query.filter_by(nameSender=currUser.name, nameReceiver=inputUserName)
    for r in results:
        resultsMes.append(r.message)
        resultsUser.append(r.nameSender)
    if len(resultsMes) > 3:
        for i in range(1, 3):
            resultsMesLast.append(resultsMes[len(resultsMes) - i])
            resultsUserLast.append(resultsUser[len(resultsUser) - i])
    else:
        resultsMesLast = resultsMes
        resultsUserLast = resultsUser

    for r in resultsSend:
        resultsSendMes.append(r.message)
        resultsSendUser.append(r.nameSender)
    if len(resultsSendMes) > 3:
        for i in range(1, 3):
            resultsSendMesLast.append(resultsSendMes[len(resultsSendMes) - i])
            resultsSendUserLast.append(resultsSendUser[len(resultsSendUser) - i])
    else:
        resultsSendMesLast = resultsSendMes
        resultsSendUserLast = resultsSendUser
    if flask.request.method == 'GET':
        user = UsersAll.query.filter_by(name=inputUserName).first()
        userTagsTable = UserPage.query.filter_by(userName=inputUserName).all()
        userTags = []
        for u in userTagsTable:
            userTags.append(u.userTags)
        tagsDict = {i: userTags.count(i) for i in userTags}
        sortedTagsDict = sorted(tagsDict.items(), key=lambda x: x[1], reverse=True)
        return render_template("usersDetails.html", userName=user.name, mainTag=sortedTagsDict[0][0], lastLogin=user.lastLogin, resultsMes=resultsMesLast, resultsUser=resultsUserLast, resultsSendMes=resultsSendMesLast, resultsSendUser=resultsSendUserLast)
    if flask.request.method == 'POST':
        if request.form['button'] == "Send":
            message = request.form.get('message')
            new_message = Message(nameReceiver=inputUserName, nameSender=currUser.name, message=message)
            db.session.add(new_message)
            db.session.commit()
            return redirect(url_for('usersDetails'))
        if request.form['button'] == 'See their page':
            return redirect(url_for('temporary'))

@app.route('/message', methods=['GET', 'POST'])
def message():
    global messagee
    if flask.request.method == 'GET':
        return render_template("message_page.html", therName=currUser.name, userName=inputUserName)
    if flask.request.method == 'POST':
        message = request.form.get('message')
        new_message = Message(nameReceiver=inputUserName, nameSender=currUser.name, message=message)
        db.session.add(new_message)
        db.session.commit()
        return redirect(url_for('homePage'))

@app.route('/myMessages', methods=['GET', 'POST'])
def myMessages():
    resultsMes = []
    resultsTh = []
    resultsMesLast = []
    resultsThLast = []
    resultsSendMes = []
    resultsSendTh = []
    resultsSendMesLast = []
    resultsSendThLast = []
    userInput=""
    sendTo = ""
    therSender = ""
    if flask.request.method == 'POST':
        userInput = request.form.get('mesText')
        sendTo = request.form.get('sendTo')
    if(userInput and sendTo):
        new_message = Message(nameReceiver=sendTo, nameSender=currUser.name, message=userInput)
        db.session.add(new_message)
        db.session.commit()
    results = Message.query.filter_by(nameReceiver=currUser.name).all()
    resultsSend = Message.query.filter_by(nameSender=currUser.name, nameReceiver=sendTo)
    for r in results:
        resultsMes.append(r.message)
        resultsTh.append(r.nameSender)

    if len(resultsMes) > 3:
        for i in range(1, 3):
            resultsMesLast.append(resultsMes[len(resultsMes) - i])
            resultsThLast.append(resultsTh[len(resultsTh) - i])
    else:
        resultsMesLast = resultsMes
        resultsThLast = resultsTh
    #print("==== " + resultsSend)
    for r in resultsSend:
        resultsSendMes.append(r.message)
        resultsSendTh.append(r.nameSender)
    if len(resultsSendMes) > 3:
        for i in range(1, 3):
            resultsSendMesLast.append(resultsSendMes[len(resultsSendMes) - i])
            resultsSendThLast.append(resultsSendTh[len(resultsSendTh) - i])
    else:
        resultsSendMesLast = resultsSendMes
        resultsSendThLast = resultsSendTh

    table = messagesTable(results)
    table.border = True
    return render_template("my_message.html", userName=currUser.name, table=table, resultsMes=resultsMesLast, resultsTh=resultsThLast, resultsSendMes=resultsSendMesLast, resultsSendTh=resultsSendThLast)

@app.route('/therMessages', methods=['GET', 'POST'])
def therMessages():
    resultsMes = []
    resultsUser = []
    results = Message.query.filter_by(nameReceiver=currUser.name).all()
    for r in results:
        resultsMes.append(r.message)
        resultsUser.append(r.nameSender)
    table = messagesTable(results)
    table.border = True
    return render_template("therMessages.html", userName=currUser.name, table=table, resultsMes=resultsMes, resultsUser=resultsUser)


@app.route('/temporary', methods=['GET', 'POST'])
def temporary():
    print(inputUserName)
    userTagsTable = UserPage.query.filter_by(userName=inputUserName).all()
    userTags = []
    for u in userTagsTable:
        userTags.append(u.userTags)
    return render_template("final_page.html", userName=inputUserName, tags=userTags, userType=currUser.type)


@app.route('/protected')
def protected():
    if isLoggedIn:
        return 'Logged in as: ' + currUser.name
    else:
        return 'Not logged in'

@app.route('/logout')
def logout():
    global isLoggedIn
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
        type = flask.request.form['type']

        user = UsersAll.query.filter_by(email=email).first()
        if user:
            return redirect(url_for('signup_post'))

        new_user = UsersAll(email=email, name=name, password=generate_password_hash(password, method='sha256'), type=type, mainTag="", lastLogin="")
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))


@app.route('/finish')
def finish():
    if flask.request.method == 'GET':
        for i in tagName:
            new_user_page = UserPage(userId=currUser.id, userName=currUser.name, userTags=i)
            db.session.add(new_user_page)
            db.session.commit()

        userTagsTable = UserPage.query.filter_by(userName=currUser.name).all()
        userTags = []
        for u in userTagsTable:
            userTags.append(u.userTags)
        print(userTags[len(userTags) - 1])
        user = UsersAll.query.filter_by(name=currUser.name).first()
        stmt = (
            update(UsersAll).
                where(UsersAll.name == user.name).
                values(mainTag=userTags[len(userTags) - 1])
        )
        print("====== " + currUser.mainTag + " =======")
        return render_template("final_page.html", userName=currUser.name, tags=userTags, userType=currUser.type)
    else:
        return redirect(url_for('login'))

@app.route('/tags')
def tags():
    s = ""
    for t in tagName :
        s += t + ","

    return s








@app.route('/chat')
def chat():
    user = UsersAll.query.filter_by(name=currUser.name).first()
    print(user.lastLogin + " ---------")
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
                bot_response = random.choice(intent['responses'])
                tagName.append(tag)

    else:
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