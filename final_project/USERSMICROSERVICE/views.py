from flask import Flask, request, Response, jsonify
import requests
from configure import dbaas
import re

app = Flask(__name__)


@app.errorhandler(405)
def four_zero_five(e):
	count()
	return Response(status=405)


@app.route('/api/v1/users', methods=["PUT"])
def function_to_add_user():
	count()
	if request.method == "PUT":
		r_data = request.get_json(force=True)
		try:
			u_name = r_data["username"]
			pwd = r_data["password"]
		except KeyError:
			return Response(status=400)

		if re.match(re.compile(r'\b[0-9a-f]{40}\b'), pwd) is None:
			return Response(status=400)

		binded_data = {"insert": [u_name, pwd], "columns": ["_id", "password"], "table": "users"}
		resp = requests.post('http://' + dbaas + '/api/v1/db/write', json=binded_data)

		if resp.status_code == 400:
			return Response(status=400)

		return Response(status=201, response='{}', mimetype='application/json')
@app.route('/api/v1/users', methods=["GET"])
def function_to_delete_user():
	count()
	if request.method == "GET":
		binded_data = {"many": 1, "table": "users", "columns": ["_id"], "where": {}}
		response = requests.post('http://' + dbaas + '/api/v1/db/read', json=binded_data)
		res = []
		for i in response.json():
			res.append(i['_id'])
		if not res:
			return Response(status=204)
		return jsonify(res)


@app.route('/api/v1/users/<username>', methods=["DELETE"])
def remove_user(username):
	count()
	binded_data = {'column': '_id', 'delete': username, 'table': 'users'}
	response = requests.post('http://' + dbaas + '/api/v1/db/write', json=binded_data)
	if response.status_code == 400:
		return Response(status=400)
	return jsonify({})


@app.route('/api/v1/_count', methods=["GET"])
def function_to_requests_count_get():
	if request.method == "GET":
		f = open("requests_count.txt", "r")
		res = [int(f.read())]
		f.close()
		return jsonify(res)
@app.route('/api/v1/_count', methods=["DELETE"])
def function_to_requests_count_delete():
	if request.method == "DELETE":
		f = open("requests_count.txt", "w")
		f.write("0")
		f.close()
		return jsonify({})


def count():
	f = open("requests_count.txt", "r")
	count = int(f.read())
	f.close()
	f2 = open("requests_count.txt", "w")
	f2.write(str(count + 1))
	f2.close()


if __name__ == "__main__":
	app.run(debug=True, host="0.0.0.0", port=80)
