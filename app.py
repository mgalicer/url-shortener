from flask import Flask, request

app = Flask(__name__)

base62_chars = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','0','1','2','3','4','5','6','7','8','9']

id_counter = 1

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

# takes in the longer link, creates a new shorter link, saves shorter link to db and returns to user
@app.route('/', methods=['POST'])
def shorten():
    response = request.get_json()
    long_link = response['long_link']
    short_link = to_base62(id_counter)
    return short_link

# takes a short link and redirects to the original longer link
@app.route('/<short_link>', methods=['GET'])
def lengthen(short_link):
    pass

if __name__ == '__main__':
    app.run()
