from flask import*

import pymysql

app=Flask(__name__)

@app.route("/api/signup", methods=["POST"])
def signup():

    username = request.form['username']
    email = request.form['email']
    phone = request.form['phone']
    password = request.form['password']

    print(username,email,phone,password)
     #create conection to db
    connection = pymysql.connect(host="localhost", user="root", password="", database="owen_sokogarden")

   #create cursor to handle sql queries
    cursor= connection.cursor()
    
    #create sql query

    sql = "insert into users(username, email, phone, password) values(%s, %s, %s, %s)"
    print(sql)

    #data to be saved

    data = (username, email, phone, password)
    print(data)

    #execute the sql query
    cursor.execute(sql,data)

    #save the data
    connection.commit()
    #return response         
    return jsonify({"message": "signup successful"})


    #login route
@app.route("/api/login", methods=["POST"])
def login():

    email = request.form['email']
    password = request.form['password']
       
    print(password,email)

     #connnect to db
    connection = pymysql.connect(host="localhost", user="root", password="",database="owen_sokogarden")

    #cursor 
    # cursor=connection.cursor()
    #key value pair
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    #create the sql query to execute
    sql= "select user_id, username, email, phone from users where email = %s and password = %s"

    #data to execute the query
    data = (email,password)

    #execute the query
    cursor.execute(sql,data)

    #check the rresulting rows
    if cursor.rowcount==0:
        return jsonify({"message": "inavalid credentials"})
    else:
        #get the user data
        user = cursor.fetchone()
        return jsonify({"message": "login successful", "user": user})

   
   



if __name__=="__main__":
    app.run(debug=True)
