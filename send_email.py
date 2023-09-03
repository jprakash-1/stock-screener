from stock_screener.screener import screener
import smtplib, ssl
import os


port = 465
smtp_server = "smtp.gmail.com"
USERNAME = os.environ.get('USER_EMAIL')
PASSWORD = os.environ.get('USER_PASSWORD')

all_positive_stock_info = screener()
# Convert the list of dictionaries to a JSON-formatted string with indentation
formatted_data = json.dumps(all_positive_stock_info, indent=4)

message = formatted_data

context = ssl.create_default_context()
with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
    server.login(USERNAME,PASSWORD)
    server.sendmail(USERNAME,USERNAME,message)