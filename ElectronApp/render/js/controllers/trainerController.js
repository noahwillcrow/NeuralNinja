// Front-end functionality for the training page

var controller = (function() {
	const { dialog } = require('electron').remote;

	const maxLengthFullPath = 30;

	let loadingOverlay = document.getElementById("loading-overlay");
	let inputFileButton = document.getElementById("input-file-button");
	let inputFilePathDisplay = document.getElementById("input-file-path-display");
	let targetOutputFileButton = document.getElementById("target-output-file-button");
	let targetOutputFilePathDisplay = document.getElementById("target-output-file-path-display");
	let trainButton = document.getElementById("train-button");
	let batchSizeInput = document.getElementById("batch-size");
	let numEpochsInput = document.getElementById("num-epochs");
	let learningRateInput = document.getElementById("learning-rate");

	let inputFilePath;
	let targetOutputFilePath;

	// Updates the path display 
	function updatePathDisplay(path, pathDisplay) {
		if (path.length > maxLengthFullPath) {
			let earliestIndex = (path.length - 1) - (maxLengthFullPath - 3);
			let slashIndex = path.substring(earliestIndex).indexOf("/");
			if (slashIndex === -1) {
				slashIndex = earliestIndex;
			}
			else {
				slashIndex += earliestIndex;
			}
			path = "..." + path.substring(slashIndex);
		}

		pathDisplay.innerText = path;
	}

	// Opens input file
	function onInputFileButtonClicked() {
		let fileChoices = dialog.showOpenDialog(options = {
			filters: trainingFileTypeFilters,
			properties: [
				"openFile"
			]
		});
		if (fileChoices.length == 0) return;
		inputFilePath = fileChoices[0];
		updatePathDisplay(inputFilePath, inputFilePathDisplay);
	}

	// Opens output file
	function onTargetOutputFileButtonClicked() {
		let fileChoices = dialog.showOpenDialog(options = {
			filters: trainingFileTypeFilters,
			properties: [
				"openFile"
			]
		});
		if (fileChoices.length == 0) return;
		targetOutputFilePath = fileChoices[0];
		updatePathDisplay(targetOutputFilePath, targetOutputFilePathDisplay);
	}

	// Training button functionality, sends to back-end
	function onTrainButtonClicked() {
		if (inputFilePath === undefined || targetOutputFilePath === undefined) return;
		loadingOverlay.classList.remove("hide");

		let batchSize = parseInt(batchSizeInput.value);
		let numEpochs = parseInt(numEpochsInput.value);
		let learningRate = parseFloat(learningRateInput.value);

		mainThreadBridge.sendMessage("train", "\"" + inputFilePath + "\"", "\"" + targetOutputFilePath + "\"", batchSize, numEpochs, learningRate);
	}

	// Hide loading overlay and training controls 
	function onTrainingCompleted() {
		loadingOverlay.classList.add("hide");
	}

	inputFileButton.addEventListener("click", onInputFileButtonClicked);
	targetOutputFileButton.addEventListener("click", onTargetOutputFileButtonClicked);
	trainButton.addEventListener("click", onTrainButtonClicked);
	mainThreadBridge.registerThreadEventListener("train", onTrainingCompleted);

	return {

	};
})();