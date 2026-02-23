from flask import*

import pymysql
import os 

app=Flask(__name__)
app.config["UPLOAD_FOLDER"] = "static/images"

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
@app.route("/api/add_products",methods=["POST"])
def addproducts():

    product_name = request.form['product_name']
    product_description = request.form['product_description']
    product_category = request.form['product_category']
    product_cost  = request.form['product_cost']
    product_image = request.files['product_image']

   
    print(product_name,product_category,product_cost,product_image,product_cost)

     #get image name
    image_name = product_image.filename
    print(image_name)

    #save the image to folder
    file_path = os.path.join(app.config["UPLOAD_FOLDER"], image_name)
    print(file_path)
    product_image.save(file_path)


    

    connection = pymysql.connect(host="localhost", user="root", password="", database="owen_sokogarden")
    cursor = connection.cursor()

    sql= "insert into product_details (product_name,product_description,product_category,product_cost,product_image) values (%s,%s,%s,%s,%s)"

    data = (product_name,product_description,product_category,product_cost,product_image)
    cursor.execute(sql,data)

    connection.commit()

    return jsonify({"message": "product added"})


@app.route("/api/get_products")
def getproducts():
    connection = pymysql.connect(host="localhost",user="root",password="",database="owen_sokogarden")
    cursor = connection.cursor(pymysql.cursors.DictCursor)

    #select query
    sql = "select * from product_details"
    cursor.execute(sql)




    if cursor.rowcount == 0:
        return jsonify({"message": "no products found"})
    else:
        #fetch products

        products = cursor.fetchall()
        return jsonify(products)





if __name__=="__main__":
    app.run(debug=True)
