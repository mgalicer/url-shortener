# url-shortener

### Set up env
```
git clone https://github.com/mgalicer/url-shortener.git
cd url-shortener
source env/bin/activate
pip install -r requirements.txt
```

### Run the server locally
```
python app.py
```

## API Endpoints

Create a new short link from a long link
```
POST http://127.0.0.1:5000/
{
    'long_link': 'link to site',
    'custom_short_link': 'optional'
}
```

Get redirected from short link to long link
```
GET http://127.0.0.1:5000/<short_link>
```

Get the stats for a given short link
```
GET http://127.0.0.1:5000/stats/<short_link>
```