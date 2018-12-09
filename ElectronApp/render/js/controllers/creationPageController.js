// Front-end functionality for the creation page

var controller = (function () {
	let inputDropdown = document.getElementById("input-dropdown");
	let outputDropdown = document.getElementById("output-dropdown");
	let createButton = document.getElementById("create-button");

	// When network is created open the network view page
	function onNetworkCreated() {
		location.href = "networkview.html";
	}

	// Sends create network command to the back end
	function onCreateButtonClicked() {
		mainThreadBridge.sendMessage("create", inputDropdown.value, outputDropdown.value);
	}

	// Populate the drop down menus for input and output node count
	function populateDropdowns(minValue, maxValue, stepSize, dropdowns) {
		for (let optionValue = minValue; optionValue <= maxValue; optionValue += stepSize) {
			for (let i = 0; i < dropdowns.length; i++) {
				let option = document.createElement("option");
				option.textContent = optionValue.toString();
				option.value = optionValue;
				dropdowns[i].appendChild(option);
			}
		}

		for (let i = 0; i < dropdowns.length; i++) {
			dropdowns[i].value = minValue;
		}
	}
	
	mainThreadBridge.registerThreadEventListener("create", onNetworkCreated);
	createButton.addEventListener("click", onCreateButtonClicked);
	populateDropdowns(1, 50, 1, [inputDropdown, outputDropdown]);

	return {
		
	};
})();