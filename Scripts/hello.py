from flask import Flask,render_template, request, redirect,url_for,session
from flask_mail import Mail, Message
from flask_socketio import SocketIO
# from flask_mysqldb import MySQl
from flask_mysqldb import MySQL
app = Flask(__name__)
socketio = SocketIO(app)#initialize an socket object
# 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 API key
app.secret_key='abcd1234'
#config db
app.config['MYSQL_HOST']='127.0.0.1'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='123456'
app.config['MYSQL_DB']='python'
app.config['MYSQL_PORT']=3306
app.config['AUTH_PLUGIN']='mysql_native_password'
#config for email
# app.config['MAIL_SERVER']='smtp.gmail.com'
# app.config['MAIL_PORT'] = 465
# app.config['MAIL_USERNAME'] = 'iamken0303@gmail.com'
# app.config['MAIL_PASSWORD'] = '4.0Ismygpa'
# app.config['MAIL_USE_TLS'] = False
# app.config['MAIL_USE_SSL'] = True
#-----------------
mysql= MySQL(app)#define the name of the variable for database
mail= Mail(app)#initialize an object of class mail
# recall express, import express, then create(express) -> only 1 app
@app.route('/',methods=['GET','POST'])#then defining the route
def index():#subsequently a function to call with that route ?? 
    if request.method== 'POST':
        cur= mysql.connection.cursor()
        value1=request.form['userName']
        value2=request.form['password']
        value3=request.form['firstName']
        value4=request.form['lastName']
        value5=request.form['age']
        value6=request.form['email']
        cur.execute("INSERT INTO users(userName,password,firstName,lastName,age,email) values (%s,%s,%s,%s,%s,%s)",(value1, value2,value3,value4,value5,value6))
        mysql.connection.commit()
        cur.close()
        cur= mysql.connection.cursor()
        cur.execute("SELECT userId from users where userName=%s",[value1])
        userId=cur.fetchone()[0]#get the first row ?
        mysql.connection.commit()
        cur.close()
        return "added to database successfully, your userId is "+str(userId)
    return render_template("index.html")
    # return "This is the index"

@app.route('/home', methods=['GET'])
def homePage():
    return render_template('home.html')

@app.route('/login',methods=['POST'])#then defining the route
def login():#subsequently a function to call with that route ?? 
    value1=request.form['userName']
    value2=request.form['password']
    cur= mysql.connection.cursor()
    cur.execute("SELECT userId from users where userName=%s and password=%s",[value1,value2])
    response=cur.fetchone()
    mysql.connection.commit()
    cur.close()
    if response!=None:
        session['userName']=value1
        return redirect(url_for('homePage'))
    return "<h2>Wrong password</h2><br><a href='/'>Try again</a><br><a href='/forgotPassword'>Forgot password?</a>"

@app.route('/forgotPassword', methods=['GET','POST'])
def resetPassword():
    if request.method=='POST':
        if('userName' in session):
            userName=session['userName']
        else:
            return "please login"#get the parameter
        cur= mysql.connection.cursor()
        response=cur.execute("UPDATE users SET password=%s where userName=%s",[request.form['password'],userName])
        mysql.connection.commit()
        cur.close()
        if response!=None:
            # return "your email is: "+str(response)
            #  msg = Message('Welcome to KenChat', sender = 'iamken0303@gmail.com', recipients = ['kenn.tnguyen@gmail.com'])
            #  msg.body = "Hello Flask message sent from Flask-Mail"
            #  mail.send(msg)
             return "<h2>password reset</h2><br><a href='/'>Login now</a>"
        return "<h2>Incorrect userName</h2><br><a href='/'>Try again</a>"
    return render_template("forgotPassword.html")

@app.route('/checkUserName', methods=['get'])
def usedUserName():
    userName=request.args.get('userName')#get the para
    # app.logger.debug('Value of userName=%s',userName)
    cur= mysql.connection.cursor()
    cur.execute("SELECT userName from users where userName=%s",[userName])
    response=cur.fetchone()
    mysql.connection.commit()
    cur.close()
    if response is not None:
        return "The user name is in use, please choose another"
    return "Your user name is good"

@app.route('/searchUserName', methods=['get'])
def searchUserName():
    userName=request.args.get('userName')#get the para
    #making regex
    searchValue='%'+userName+'%'
    # app.logger.debug('Value of userName=%s',userName)
    cur= mysql.connection.cursor()
    cur.execute("SELECT userName from users where userName LIKE %s",[searchValue])
    response=cur.fetchall()
    mysql.connection.commit()
    cur.close()
    if response is not None:
        result=""
        for a_row in response:
            result+="<div class='a_conversation' onclick='loadChat(this.textContent)'>"+str(a_row[0])+"</div>"
        return result
    return "Your user name is good"

@app.route('/loadingChat', methods=['get'])
def loadingChat():
    userName2=request.args.get('userName2')#get the para
    userName1=session['userName']#take the current user name from session
    #check in ListOfConvo if they ever chatteed together
    cur= mysql.connection.cursor()
    cur.execute("SELECT chatId from listOfConversation where (userName1=%s and userName2=%s) or (userName1=%s and userName2=%s)",[userName1,userName2,userName2,userName1])
    response=cur.fetchone()
    mysql.connection.commit()
    cur.close()
    if response is not None:#they have talked together
        chatId = response[0]#return the chatId
        session['chatId']=chatId#store in session
        #because there exists name in the conversationList, there must be info from the chat table
        #no need to create the table
        cur= mysql.connection.cursor()
        cur.execute("SELECT * from `%s` where messageId<=(select messageId from `%s` order by messageId desc limit 1)",[chatId,chatId])
        response=cur.fetchall()
        app.logger.info(type(response))#take the response
        mysql.connection.commit()
        cur.close()
        result=""
        if not response:
            return "You guys never have a chat before"
        else:
            for a_message in response:
                if a_message[1]==session['userName']:#if the message was sent by the user
                    result+="<div class='sender' id="+"'"+str(a_message[0])+"'>"
                    result+="<p>"+str(a_message[2])+"</p>"#print the content
                    result+="</div>"
                else:#if the message was sent by the other
                    result+="<div class='receiver' id="+"'"+str(a_message[0])+"'>"
                    result+="<p>"+str(a_message[2])+"</p>"#print the content
                    result+="</div>"
        return result #return a list of every lines in a chat
    else: #never talk together, then add to the list
        cur= mysql.connection.cursor()
        cur.execute("INSERT INTO listOfConversation(userName1,userName2) values (%s,%s)",[userName1,userName2])#add to the list of conver
        mysql.connection.commit()
        cur.execute("SELECT chatId from listOfConversation where (userName1=%s and userName2=%s)",[userName1,userName2])
        response=cur.fetchone()
        mysql.connection.commit()
        cur.close()
        if response is not None:#
            session['chatId']=response[0]#store in session
            chatId= response[0]
            #create the table for the chat
            cur= mysql.connection.cursor()
            response=cur.execute("CREATE TABLE `%s` (messageId int auto_increment primary key,sender varchar(30), content varchar(400), sent_at datetime,status varchar(30),foreign key(sender) references users(userName))",[chatId])#may have syntax error here
            app.logger.info(response)
            mysql.connection.commit()
            cur.close()
            return "You have never talked to each other"
        return "Error happen, cannot find the chatId after inserting for THE NEW CHAT"

#Chatting
new_message_status=[] #define the list of signals
@app.route('/sendMessage',methods=['GET'])
def sendAMessage():
    messageContent=request.args.get('content')#get the para
    messageContent=messageContent.replace("%20"," ")#replace the %20 by whitespace
    app.logger.debug(messageContent)
    if messageContent:
        #execute the below lines if there is a message sent
        time=request.args.get('time')#get the para
        time=time.replace("%20"," ")#replace the %20 by whitespace
        app.logger.debug(time)
        userName=session['userName']#take the current user name from session
        #check in ListOfConvo if they ever chatteed together
        cur= mysql.connection.cursor()
        response=cur.execute("INSERT INTO `%s`(sender,content,sent_at,status) values (%s,%s,%s,'sent')",[session['chatId'],userName,messageContent,time])
        mysql.connection.commit()
        cur.close()
        
        if response: #if insert successfully
            return "success" #return the content to add
    else: pass

# @app.route('/getChatStatus', methods='[GET]')
# def getChatStatus():
#     global new_message_status #reference the global variable
#     if new_message_status[session['chatId']]:#if there is a new message
#         return "True"
#     return "False"

#**************************defining socket endpoint******************
def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@socketio.on('my event')
def handle_my_custom_event(json, methods=['GET', 'POST']):
    print('received my event: ' + str(json))
    socketio.emit('my response', json, callback=messageReceived)
#starting the app
if __name__=='__main__':
    app.run(debug=True)