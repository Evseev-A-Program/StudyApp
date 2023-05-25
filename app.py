from flask import *
import db
import secrets
from flask_socketio import SocketIO

app = Flask(__name__)
app.secret_key = "mysecretkey" # необходим для подписи сессии
socketio = SocketIO(app)

@app.route('/')
def index():
    return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        result = db.get_user(username, password)
        if result != "not found":
            token = secrets.token_urlsafe(32)
            session[token] = result # сохраняем token пользователя в сессии
            return redirect(url_for('home', token=token))
        else:
            return render_template('login.html', error='Неверный логин или пароль')
    return render_template('login.html')

@app.route('/home')
def home():
    token = request.args.get("token")
    if token in session:
        if session[token][6] == 1:
            chats = [[1, 1, 2, "Преподаватель: Дорошенко Валентина Михайловна"]]
            return render_template('home_student.html', token=token, name=session[token][2], surname=session[token][3],
                                   patronymic=session[token][4], group=session[token][5], chats=chats)
        else:
            return render_template('home_teacher.html', token=token, name=session[token][2], surname=session[token][3],
                                   patronymic=session[token][4], group=session[token][5])
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    token = request.args.get('token')
    session.pop(token, None) # удаляем имя пользователя из сессии
    return redirect(url_for('login'))

@app.route('/schedule')
def schedule():
    token = request.args.get('token')
    if token in session:
        if session[token][6] == 1:
            return render_template('schedule_student.html', token=token)
        else:
            return render_template('schedule_teacher.html', token=token)
    else:
        return redirect(url_for('login'))



@app.route('/chat', methods=['GET','POST'])
def chat():
    token = request.args.get('token')
    if token == None:
        token = request.form['token']
    chatId = request.args.get("chatId")
    if chatId == None:
        chatId = request.form['chatId']
    if token in session:
        messages = db.get_messages(chatId)
        messages_list =[]
        user_id = session[token][0]
        for message in messages:
            user = db.get_username_by_id(message[3])
            message = list(message)
            if int(user[0]) == int(user_id):
                message[3] = "Я"
            else:
                message[3] = user[2] + " " + user[1] + " " + user[3]
            messages_list.append(message)
        return render_template('chat.html', token=token, chatId=chatId, messages=messages_list)
    else:
        return redirect(url_for('login'))

@app.route('/send', methods=['POST'])
def send():
    token = request.form['token']
    chatId = request.form['chatId']
    message = request.form['message']
    if message != None:
        mes_check = message.replace(" ", "")
        if mes_check != "":
            db.add_messages(chatId, message, session[token][0])
            # return jsonify({'status': 'success'})
            return redirect(url_for("chat", token=token, chatId=chatId))

# @app.route('/get_message', methods=['GET'])
# def get_message():
#     # token = request.args.get('token')
#     # if token == None:
#     token = request.form['token']
#     # chatId = request.args.get("chatId")
#     # if chatId == None:
#     chatId = request.form['chatId']
#     if token in session:
#         messages = db.get_messages(chatId)
#         messages_list =[]
#         user_id = session[token][0]
#         for message in messages:
#             user = db.get_username_by_id(message[3])
#             message = list(message)
#             if int(user[0]) == int(user_id):
#                 message[3] = "Я"
#             else:
#                 message[3] = user[2] + " " + user[1] + " " + user[3]
#             messages_list.append(message)
#         return jsonify({'messages': messages})
#     else:
#         return redirect(url_for('login'))



app.run()


# server = Server(app.wsgi_app)
# server.watch("templates/*.*")
