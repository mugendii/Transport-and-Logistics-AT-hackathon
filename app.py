from flask import Flask, request
import africastalking
import os
import random
from faker import Faker

fake = Faker()
app = Flask(__name__)
username = "sandbox"

api_key = os.environ.get("SECRET_KEY")  
africastalking.initialize(username, api_key)
sms = africastalking.SMS

response = ""

@app.route('/', methods=['POST', 'GET'])
def ussd_callback():
  global response
  session_id = request.values.get("sessionId", None)
  service_code = request.values.get("serviceCode", None)
  phone_number = request.values.get("phoneNumber", None)
  text = request.values.get("text", "default")
  sms_phone_number = []
  sms_phone_number.append(phone_number)

  if text == '':
    response  = "CON Welcome to our Transport and Logistics service \n"
    response += "1. Request for goods delivery \n"
    response += "2. Request for personal transport \n"
    response += "3. Check status \n"
    response += "0. Exit"

  elif text == '1':
    response = "CON What type of goods do you want to deliver?  \n"
    response += "1. Perishable goods  \n"
    response += "2. Bulky goods \n"
    response += "0. Exit"

  elif text == '1*1' or text == '1*2':
    response = "CON Choose nearest town  \n"
    response += "1. Nairobi \n"
    response += "2. Mombasa \n"
    response += "3. Nakuru \n"
    response += "4. Kisumu \n"
    response += "5. Eldoret \n"
    response += "6. Thika \n"
    response += "0. Exit"

  elif text.startswith('1*1*') or text.startswith('1*2*') and text != '1*1*0' and text != '1*2*0':
      name = fake.first_name()
      phone_number = "07" + "".join(random.choice("0123456789") for _ in range(8))
      response = f"END Driver {name} will assist you. Call {name} at {phone_number}."

  elif text == '2':
    response = "CON Choose type of vehicle \n"
    response += "1. Car \n"
    response += "2. Van \n"
    response += "3. Motorcycle \n"
    response += "0. Exit"

  elif text == '2*1' or text == '2*2' or text == '2*3' and text != '2*0':
      phone_number = "07" + "".join(random.choice("0123456789") for _ in range(8))
      response = f"END Call our transport service (phone no: {phone_number})"

  elif text == '3':
    response = "END We are checking the status of your request. You'll receive a message soon\n"
    response += "0. Exit"

  elif text == '0' or text == '1*1*0' or text == '1*2*0' or text == '2*0' or text == '3*0' or text == '1*0' or text == '2*1*0' or text == '2*2*0' or text == '2*3*0':
    response = "END Thank you for using our service."

  else:
    response = "END Invalid input. Try again or press 0 to exit."

  return response