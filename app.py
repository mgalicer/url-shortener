from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os, json

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "links.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

base62_chars = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','0','1','2','3','4','5','6','7','8','9']

id_counter = 1

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    short_link = db.Column(db.String(8), unique=True, nullable=False)
    long_link = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)

# takes the longer link and converts it to a base62 string
def to_base62(link_id):
    base62_int = []

    while link_id > 0:
        remainder = link_id % 62
        base62_int.append(remainder)
        link_id = link_id // 62
    base62_int.reverse()

    base62_string = ''
    for i in base62_int:
        base62_string += base62_chars[i]
    
    return base62_string

# takes the shorter link and converts it to base10 (to access id)
def to_base10(link):
    pass

# make sure everything is working ok
@app.route('/', methods=['GET'])
def hello():
    return 'Hello, world!'

# route to shorten long links
@app.route('/', methods=['POST'])
def shorten():
    response = request.get_json()
    long_link = response['long_link']

    # the same url should always generate the same shortlink
    link = Link.query.filter_by(long_link=long_link).first()
    if link:
        short_link = link.short_link
    else:    
        global id_counter
        # convert user provided link to a shorter one, add to db
        short_link = to_base62(id_counter)
        db.session.add(Link(id=id_counter, short_link=short_link, long_link=long_link))
        db.session.commit()
        id_counter = id_counter + 1

    return json.dumps({'short_link': short_link})

# takes a short link and redirects to the original longer link
@app.route('/<short_link>', methods=['GET'])
def lengthen(short_link):
    pass

if __name__ == '__main__':
    app.run()
