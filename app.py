from flask import Flask, request

app = Flask(__name__)

# takes the longer link and converts it to a base62 string
def to_base62(link_id):
    pass

# takes the shorter link and converts it to base10 (to access id)
def to_base10(link):
    pass

# make sure everything is working ok
@app.route('/', methods=['GET']):
def hello():
    return 'Hello, world!'

# takes in the longer link, creates a new shorter link, saves shorter link to db and returns to user
@app.route('/', methods=['POST']):
def shorten():
    pass

# takes a short link and redirects to the original longer link
@app.route('/<short_link', methods=['GET']):
def lengthen(short_link):
    pass