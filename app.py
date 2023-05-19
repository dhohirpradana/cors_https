from flask import Flask, request, Response
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    url = request.url.replace(request.host_url, '', 1)
    if not url:
        return Response('Missing URL parameter.', status=400)

    # Forward the request to the specified URL
    try:
        response = requests.request(
            method=request.method,
            url=url,
            headers={key: value for (key, value) in request.headers if key != 'Host'},
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False,
            verify=False  # Don't validate SSL certs
        )
    except requests.exceptions.RequestException as e:
        return Response(str(e), status=500)

    # Handle CORS by setting appropriate headers
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS'
    }

    # Return the response from the proxied request
    return Response(
        response=response.content,
        status=response.status_code,
        headers=headers
    )

if __name__ == '__main__':
    app.run()
