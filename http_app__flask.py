from flask import Flask, request, make_response

app = Flask(__name__)

MEM = dict()

@app.route('/set', methods=['PUT'])
def set():
    for k, v in request.args.items():
        MEM[k] = v
    return make_response('', 204)

@app.route('/get', methods=['GET'])
def get():
    for k, v in request.args.items():
        if k == 'key':
            if v in MEM:
                return make_response(MEM[v], 200)
            else:
                return make_response('', 404)
    return make_response('', 400)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', default=4000)
    args = parser.parse_args()

    app.run('localhost', port=4000, debug=True)
