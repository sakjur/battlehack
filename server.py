from flask import Flask, request
from urllib.parse import parse_qs
import apini
import elks
import re

app = Flask(__name__)
baseurl = 'https://apini.theusr.org/pay/%s'

@app.route('/')
def index():
    return apini.random_url()

@app.route('/incomingsms', methods=['POST'])
def incomingsms():
    rawmessage = request.form['message'].strip()
    rawmessage = rawmessage.split()
    rawmessage = list(map(lambda x: x.strip(), rawmessage))
    sender = request.form['from']
    if re.match("\+[0-9]*", rawmessage[0]):
        recipient = rawmessage[0]
        amount = rawmessage[2]
    else:
        recipient = sender
        amount = rawmessage[1]
    url = apini.insert_transaction(int(amount), sender, recipient)
    if recipient == sender:
        return baseurl % url
    else:
        elks.send_url(url, amount, recipient)
    return ''

@app.route('/pay', methods=['POST'])
def post_handler(payid):
    return ''

@app.route('/pay/<payid>')
def pay(payid):
    return ''

if __name__ == '__main__':
    print('Starting server...')
    app.run(debug=True)

