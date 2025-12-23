import requests
from flask import Flask, request, Response

app = Flask(__name__)

@app.route('/')
def proxy():
    url = request.args.get('url')
    if not url:
        return "Welcome to the Web Gateway! Use ?url=https://example.com to fetch content.", 200

    try:
        # Fetch the content from the target URL
        # We use stream=True to handle large files and forward headers
        resp = requests.get(url, stream=True, verify=False)
        
        # Filter out hop-by-hop headers
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        headers = [(name, value) for (name, value) in resp.raw.headers.items()
                   if name.lower() not in excluded_headers]

        response = Response(resp.content, resp.status_code, headers)
        return response
    except Exception as e:
        return f"Error fetching URL: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
