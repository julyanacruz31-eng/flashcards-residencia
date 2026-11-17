import urllib.request
import json

with open('index.html', 'rb') as f:
    html_data = f.read()

req = urllib.request.Request(
    'https://ship.page/deploy',
    data=html_data,
    headers={
        'Content-Type': 'text/html',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
    },
    method='POST'
)

try:
    with urllib.request.urlopen(req, timeout=30) as resp:
        res_text = resp.read().decode('utf-8')
        print('Ship.page response:', res_text)
except Exception as e:
    print('Ship deploy error:', e)
