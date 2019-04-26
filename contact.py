# FOR prod just change TO_ADDRESS
import requests
import json

reCaptcha_key = "xxx"

def verify_captcha(captcha):
    res = requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        data={"secret":reCaptcha_key, "response":captcha}
    )
    print(res.json())
    return res.json()['success']


def send_email(request):
    """
    Google cloud platform internally uses flask to run cloud functions.
    So here `request` is Flask.request
    """
    TO_ADDRESS = "any@any.com"
    ORIGINATOR = "mailjet_verified_email_addr@xyz.com"

    # Consuming input variables required from form
    FROM_EMAIL = request.form['email']
    FROM_NAME = request.form['name']
    PHONE = request.form['phone']
    SUB = request.form['subject']
    MSG = request.form['message']
    captcha = request.form['g-recaptcha-response']

    user = 'xxx'
    password = 'xxx'

    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'Content-Type': 'application/json'
        }

    verfy = verify_captcha(captcha)
    if not verfy:
        log = "CAPTCHA FAIL From: {}({})  MSG:{}".format(FROM_NAME, FROM_EMAIL, MSG)
        print(log)
        data = json.dumps({"code":"fail", "message":"unauthorized!"})
        return (data, 400, headers)


    log = "Captcha: {}  From: {}({})  MSG:{}".format(verfy,FROM_NAME, FROM_EMAIL, MSG)
    print(log)
    data = {
        'Messages': [
            {
                "From": {
                        "Email": ORIGINATOR,
                        "Name": "Contactform BOT"
                },
                "To": [
                        {
                                "Email": TO_ADDRESS,
                                "Name": "splendre"
                        }
                ],
                "ReplyTo": {"Email": FROM_EMAIL, "Name": FROM_NAME},
                "Subject": SUB,
                "TextPart": "",
                "HTMLPart": "<p>{}<hr><p>Name:{} <p>Ph:{} <p>Email:{}".format(
                    MSG, FROM_NAME, PHONE, FROM_EMAIL
                    )
            }
        ]
    }
    
    res = requests.post(
        'https://api.mailjet.com/v3.1/send',
        data=json.dumps(data),
        auth=requests.auth.HTTPBasicAuth(user, password)
        )
    data = json.dumps({"code":"ok", "message":"Message send successfully!"})
    return (data, 200, headers)
