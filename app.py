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


# Mpesa Payment Route/Endpoint 
import requests
import datetime
import base64
from requests.auth import HTTPBasicAuth

@app.route('/api/mpesa_payment', methods=['POST'])
def mpesa_payment():
    if request.method == 'POST':
        amount = request.form['amount']
        phone = request.form['phone']
        # GENERATING THE ACCESS TOKEN
        # create an account on safaricom daraja
        consumer_key = "GTWADFxIpUfDoNikNGqq1C3023evM6UH"
        consumer_secret = "amFbAoUByPV2rM5A"

        api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"  # AUTH URL
        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))

        data = r.json()
        access_token = "Bearer" + ' ' + data['access_token']

        #  GETTING THE PASSWORD
        timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'
        business_short_code = "174379"
        data = business_short_code + passkey + timestamp
        encoded = base64.b64encode(data.encode())
        password = encoded.decode('utf-8')

        # BODY OR PAYLOAD
        payload = {
            "BusinessShortCode": "174379",
            "Password": "{}".format(password),
            "Timestamp": "{}".format(timestamp),
            "TransactionType": "CustomerPayBillOnline",
            "Amount": "1",  # use 1 when testing
            "PartyA": phone,  # change to your number
            "PartyB": "174379",
            "PhoneNumber": phone,
            "CallBackURL": "https://modcom.co.ke/api/confirmation.php",
            "AccountReference": "account",
            "TransactionDesc": "account"
        }

        # POPULAING THE HTTP HEADER
        headers = {
            "Authorization": access_token,
            "Content-Type": "application/json"
        }

        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"  # C2B URL

        response = requests.post(url, json=payload, headers=headers)
        print(response.text)
        return jsonify({"message": "Please Complete Payment in Your Phone and we will deliver in minutes"})
    



if __name__=="__main__":
    app.run(debug=True)
