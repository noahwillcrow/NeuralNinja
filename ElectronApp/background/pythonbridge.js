module.exports = {
    // Creates a new python process that is held open until told otherwise
	createPythonBridge: function (callback, pythonPath) {
		let { PythonShell } = require('python-shell');
		let pyshell = new PythonShell(pythonPath);

		pyshell.on('message', function (message) {
			try {
				callback(message);
			}
			catch (ex) {
				console.log(message);
				console.error(ex);
			}
		});

		return {
			sendMessage: function(message) {
				pyshell.send(message);
			}
		};
	}
};