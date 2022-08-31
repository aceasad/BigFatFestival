from flask import Flask, render_template, jsonify, request
from flask_restful import Resource, Api, reqparse
from werkzeug.wrappers import response
from werkzeug.utils import secure_filename
from dotenv import load_dotenv,find_dotenv
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask import Response, request, jsonify
from PIL import Image
from datetime import datetime
import boto3
import time
import os
from bson import json_util
import json
import io
import qrcode
load_dotenv(find_dotenv())

static_dir = str(os.path.abspath(os.path.join(__file__ , "..", os.getenv("STATIC_DIR"))))
app = Flask(__name__ , static_folder=static_dir , static_url_path="" , template_folder=static_dir)
app.config["MONGO_URI"] = "mongodb+srv://aceasad:helloworld12@cluster0.63ieciz.mongodb.net/bigfatfestival"
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
mongo = PyMongo(app)
api = Api(app)

@app.route("/")
def index():
    return render_template("index.html")

def generateCode(data,email):
    image_name = email.replace("@","%40")+'.png'
    #Creating a QRCode object of the size specified by the user
    qr = qrcode.QRCode(version = 2,
                   box_size = 10,
                   border = 5) 
    qr.add_data("http://13.235.83.97:4242/qrinfo?email="+email) #Adding the data to be encoded to the QRCode object
    qr.make(fit = True) #Making the entire QR Code space utilized
    img = qr.make_image() #Generating the QR Code
    img.save(f'{"./qrCodes/"+email.replace("@","%40")}.png') #Saving the QR Code

    #Showing the pop up message on saving the file
    print("QR Code is saved successfully!")
    s3 = boto3.resource('s3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
        aws_secret_access_key=os.getenv('AWS_SECRET_KEY')
    )
    bucket = 'big-fat-festival-ticket'
    region = 'ap-south-1'
    folder = 'qrTickets'
    time.sleep(1)
    s3.Bucket(bucket).upload_file("./qrCodes/"+image_name,folder+'/'+image_name)
    print("Upload Successful")
    url = f"https://{bucket}.s3.{region}.amazonaws.com/{folder}/{image_name}"
    key=folder+'/'+image_name
    
    if os.path.exists("./qrCodes/"+image_name):
        os.remove("./qrCodes/"+image_name)
    else:
        print("The file does not exist")
    return url,key
    #jsonify({'image':url,'key':folder+'/'+image_name+'.jpeg'})


@app.route('/qrinfo',methods=['GET'])
def qrinfo():
    data = request.get_json(force=True)
    info=mongo.db.UserTickets.find_one({'email':data['email']})
    passInfo="Pass has not been used yet."
    if (info["isPassUsed"]==True):
        passInfo="Pass Has been used already."
    return render_template("qrCode.html",name=info["name"],email=info["email"],pass_type=info["pass_type"],isPassUsed=info["isPassUsed"])

@app.route('/api/userticket',methods=['GET','POST','PUT','DELETE'])
def createUserTicket():
    '''
    This function creates a user in mongodB and a Stripe account
    '''
    if request.method == 'POST':
        data = request.get_json(force=True)
        count=mongo.db.UserTickets.find_one({'email':data['email']})
        if count==None or count==0:
            print(data)
            url,key=generateCode(data,data['email'])
            dataInsert= {
                "email":data['email'], 
                "name":data['name'], 
                "pass_type":data['pass_type'], 
                "qr_image":url,
                "qr_key":key,
                "isPassUsed":False
            }
            mongo.db.UserTickets.insert_one(dataInsert)
            return json.dumps({'message':data['email']+' pass has been made!',"key":key})
        else:
            return json.dumps({"message":"email already exists and ticket has been made, kindly update instead"})
    if request.method == 'GET':
        data = request.args["email"]
        res=mongo.db.UserTickets.find_one({"email":data})        
        return json.dumps(res,default=json_util.default)
    if request.method == 'PUT':
        data = request.get_json(force=True)
        myquery = { "email": data["email"] }
        newvalues = { "$set": { "isPassUsed": True } }
        mongo.db.UserTickets.update_one(myquery, newvalues)       
        return json.dumps({'message':data['email']+' pass used information has been updated.'})
    if request.method == 'DELETE':
        data = request.get_json(force=True)
        myquery = { "email": data['email'] }
        mongo.db.UserTickets.delete_one(myquery)
        return Response(json.dumps({'message':data['email']+' information has been deleted.'}), status=200, mimetype='application/json')
    





