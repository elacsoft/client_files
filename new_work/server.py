from flask import Flask, request, jsonify
from final import genderFunc, intentFunc, toxicFunc, passionFunc




app = Flask(__name__)


@app.route('/reply', methods=['POST', 'GET'])
def reply():
    name = request.args.get('name')
    comment = request.args.get('comment')
    isarabic = request.args.get('isarabic')
    code = request.args.get('code')
    if code == "gender":
        g = genderFunc(name)
    return jsonify({'output': g)

    if code == "intent":
        i = intentFunc(comment, isarabic)
    return jsonify({'output': i)

    if code == "toxic":
        t = toxicFunc(comment)
    return jsonify({'output': t)


    if code == "passion":
        p = passionFunc()
    return jsonify({'output': p)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, threaded=True)
