from flask import Flask, render_template, request
import requests
import smtplib
import os
import datetime


url_data_link = "https://api.npoint.io/a1294ef9dde4ff418a45"
data = requests.get(url_data_link)
data_json = data.json()
my_email = os.environ.get('MY_EMAIL')
my_password = os.environ.get('MY_PASSWORD')
rec_address = os.environ.get('REC_ADDRESS')
present_year =  datetime.datetime.now().year
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html', blogs=data_json, year=present_year)


@app.route('/about')
def about():
    return render_template('about.html', year=present_year)


@app.route('/read_more/<int:id>')
def read_more(id):
    for blog in data_json:
        if blog['id'] == id:
            return render_template('readmore.html', blog=blog)
    return render_template('readmore.html', blog=None, year=present_year)


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/message', methods=['POST'])
def receive_data():
    connection = smtplib.SMTP("smtp.gmail.com", port=587)
    connection.starttls()
    connection.login(user=my_email, password=my_password)

    if request.method == 'POST':
        email = request.form['email']
        message = request.form['message']
        connection.sendmail(from_addr=my_email, to_addrs=rec_address,
                            msg=f"Subject: Blog Website Inquiry \n\n email:{email}\nmessage:{message}")
        connection.close()
        return render_template('contact.html', year=present_year)
    return None


if __name__ == '__main__':
    app.run()
