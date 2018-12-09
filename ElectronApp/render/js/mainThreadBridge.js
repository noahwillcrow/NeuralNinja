// Communication between front-end and back-end

var mainThreadBridge = (function() {
	const { ipcRenderer } = require('electron');

	let threadEventHandlers = {};
	let defaultThreadEventHandler;

	ipcRenderer.on('async-reply', (event, eventName, ...args) => {
		if (eventName in threadEventHandlers) {
			threadEventHandlers[eventName](...args);
		}
		else if (defaultThreadEventHandler !== undefined) {
			defaultThreadEventHandler(eventName, ...args);
		}
	});

	return {
		toggleStacktrace: function () {
			ipcRenderer.send('async', 'toggleStacktrace');
		},

		sendMessage: function (eventName, ...args) {
			ipcRenderer.send('async', eventName, ...args);
		},

		registerThreadEventListener: function (eventName, callback) {
			threadEventHandlers[eventName] = callback;
		},

		registerDefaultThreadEventListener: function (callback) {
			defaultThreadEventHandler = callback;
		}
	};
})();