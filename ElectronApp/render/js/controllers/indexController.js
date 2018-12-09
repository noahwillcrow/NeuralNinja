// Front-end functionality for the main homepage when the application initializes

var controller = (function() {
	const { dialog } = require('electron').remote;

	let openButton = document.getElementById("open-button");

	// When a network is created go to network view page
	function onNetworkCreated() {
		location.href = "networkview.html";
	}

	// When a network is loaded open the networkview
	function onNetworkLoaded() {
		location.href = "networkview.html";
	}

	// Open the dialogue to select a network file
	function onOpenButtonClicked() {
		let path = dialog.showOpenDialog(options = { 
			filters: networkFileTypeFilters,
			properties: [
				"openFile"
			]
		});
		mainThreadBridge.sendMessage("load", path);
	}

	mainThreadBridge.registerThreadEventListener("create", onNetworkCreated);
	mainThreadBridge.registerThreadEventListener("load", onNetworkLoaded);
	openButton.addEventListener("click", onOpenButtonClicked);

	return {

	};
})();