import os

from flask import Flask, Response, jsonify, abort


# Data directory
data_dir = 'data'
# Port for server
server_port = 8080


app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(error):
	r"""Main error handaling function.

	Args:
		error (Exception): Error

	Returns:
		Tuple[str, int]: Data requested.
	"""
	return 'File name does not exits!!', 404


@app.route('/<file_name>', methods=['GET'])
def server(file_name=None):
	r"""Main server function for getting logs.

	Args:
		file_name (str): Name of the file

	Returns:
		Response: Data requested.
	"""
	files = os.listdir(data_dir)
	if file_name is None: return jsonify({'files': files, 'size': len(files)})
	if not file_name in files: abort(404)
	file = open('%s/%s' % (data_dir, file_name))
	return Response(file.read(), mimetype='text/plain')


@app.route('/log/out', methods=['GET'])
def log_out_server():
	r"""Main server function for getting logs.

	Returns:
		Response: Data requested.
	"""
	return Response(str(out).encode('utf-8'), mimetype='text/plain')


@app.route('/log/err', methods=['GET'])
def log_err_server():
	r"""Main server function for getting logs.

	Returns:
		Response: Data requested.
	"""
	return Response(str(err).encode('utf-8'), mimetype='text/plain')


def start_server(*args, **kwargs):
	app.run(host='0.0.0.0', port=server_port, threaded=True)


# vim: tabstop=3 noexpandtab shiftwidth=3 softtabstop=3
