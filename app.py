from flask import Flask, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os, json

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "links.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
base_url = 'http://127.0.0.1:5000/'

db = SQLAlchemy(app)

base62_chars = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','0','1','2','3','4','5','6','7','8','9']

class Link(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    short_link = db.Column(db.String(8), unique=True, nullable=False)
    long_link = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)

class Visit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    link_id = db.Column(db.Integer, db.ForeignKey('link.id'),
            nullable=False)
    link = db.relationship('Link',
            backref=db.backref('visits', lazy=True))
    visit_time = db.Column(db.DateTime, nullable=False,
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

def add_to_db(short_link, long_link):
    db.session.add(Link(short_link=short_link, long_link=long_link))
    db.session.commit()

# create an object that shows the number of visits per day
def create_histogram(visits):
    histogram = {}
    for visit in visits:
        visit = visit.visit_time.strftime("%Y-%m-%d")
        if visit in histogram: 
            histogram[visit] += 1
        else:
            histogram[visit] = 1
    return histogram
   
# make sure everything is working ok
@app.route('/', methods=['GET'])
def hello():
    return 'Hello, world!'

# route to shorten long links
@app.route('/', methods=['POST'])
def shorten():
    response = request.get_json()
    if 'long_link' not in response:
        return 'Please provide a link to convert!', 400

    long_link = response['long_link']
    # if link already exists, we should return the already shortened url
    link = Link.query.filter_by(long_link=long_link).first()
    if link:
        return json.dumps({'short_link': f'{base_url}{link.short_link}'})

    if 'custom_short_link' in response:
        if len(response['custom_short_link']) > 7:
            return 'Please provide a short link 7 characters long or less', 400
        #if the user provided a short link, let's use that! 
        short_link = response['custom_short_link']
    else:
        # if they didn't, let's create one
        last_item_id = Link.query.order_by(Link.id.desc()).first().id
        short_link = to_base62(last_item_id + 1)

    add_to_db(short_link, long_link)

    return json.dumps({'short_link': f'{base_url}{short_link}'})

# takes a short link and redirects to the original longer link
@app.route('/<short_link>', methods=['GET'])
def lengthen(short_link):
    link = Link.query.filter_by(short_link=short_link).first()
    
    # create a new visit associated with the link
    db.session.add(Visit(link=link))
    db.session.commit()

    long_link = link.long_link
    if long_link:
        return redirect(long_link)
    else:
        return 'Couldn\'t find that url!', 400 

# returns the stats for a given link: when it was created, how many total visits, histogram of visits per day
@app.route('/stats/<short_link>', methods=['GET'])
def stats(short_link):
    link = Link.query.filter_by(short_link=short_link).first()
    created = link.created_at.strftime("%Y-%m-%d %H:%M:%S")
    visits = link.visits

    return json.dumps({
        'created at': created,
        'total visits': len(visits),
        'histogram': create_histogram(visits)
        })

if __name__ == '__main__':
    app.run()
