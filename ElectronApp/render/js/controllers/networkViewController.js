// Front-end functionality for the network visualization

var controller = (function () {
	const { dialog } = require('electron').remote;
	const { range } = require("../../shared/utils.js");

	// The starting x value for the first node in the network visualization
	const xMin = 75;
	// The starting y value for the first node in the network visualization
	const yMin = 10;

	// The distance horizontally between each node to align node with layer
	const xMargin = 200;
	// The distance vertically between each node in layer
	const yMargin = 40;

	// Number of nodes before nodes become static and no longer visually render
	const largeLayerThreshold = 8;
	const hoveredWeightsBackgroundColor = "#dcdcdc";

	// Other canvas values for formatting
	const bodyLeftMargin = 8;
	const canvasHeight = 300;

	let layers, weightMatrices;
	// Initialized weight index
	let currentHoveredWeightsIndex = -1;

	let loadingOverlay = document.getElementById("loading-overlay");
	let networkWindow = document.getElementById("network-window");
	let networkControls = document.getElementById("network-controls");
	let networkCanvas = document.getElementById("neural-network-canvas");
	let canvasContext = networkCanvas.getContext("2d");
	let saveButton = document.getElementById("save-button");

	let layerControlsTemplate = document.getElementById("layer-controls-template");
	let layerCreateTemplate = document.getElementById("layer-create-template");

	// Resize layer to new size
	function changeLayerSize(layerIndex, newSize) {
		mainThreadBridge.sendMessage("resizeLayer", layerIndex, newSize);
	}

	// Save network functionality 
	function saveAs() {
		let path = dialog.showSaveDialog(options = { filters: networkFileTypeFilters });
		mainThreadBridge.sendMessage("save", path);
	}

	// Function to create new layers with activation type and specified number of nodes
	function createNewLayerModal(insertLayerIndex) {
		let layerCreateModalContent = layerCreateTemplate.content.cloneNode(true);

		let activationType = layerCreateModalContent.querySelector(".new-layer-activation-type-select");
		let layerType = layerCreateModalContent.querySelector(".new-layer-type-select");
		let createButton = layerCreateModalContent.querySelector(".create-layer-button");

		let currentLayerTypeSpecificOptions = layerCreateModalContent.querySelector(".layer-type-specific-options." + layerType.value);
		layerType.addEventListener("change", function() {
			currentLayerTypeSpecificOptions.classList.add("hide");
			currentLayerTypeSpecificOptions = currentLayerTypeSpecificOptions.parentElement.querySelector(".layer-type-specific-options." + layerType.value);
			currentLayerTypeSpecificOptions.classList.remove("hide");
		});

		let fullyConnectedLayerSizeInput = layerCreateModalContent.querySelector(".new-fully-connected-layer-size-input");
		let conv1DKernelSizeInput = layerCreateModalContent.querySelector(".new-conv1d-kernel-size-input");

		let modal = createModal(layerCreateModalContent, 100, 300);

		createButton.addEventListener("click", function() {
			if (layerType.value === "fullyConnected") {
				mainThreadBridge.sendMessage("addFullyConnectedLayer", insertLayerIndex, activationType.value, parseInt(fullyConnectedLayerSizeInput.value));
			}
			else if (layerType.value === "conv1d") {
				mainThreadBridge.sendMessage("addConv1DLayer", insertLayerIndex, activationType.value, parseInt(conv1DKernelSizeInput.value));
			}
			modal.destroy();
		});
	}

	// Clears canvas to rerender 
	function clear(ctx) {
		networkControls.innerHTML = "";
		ctx.canvas.width = layers.length * xMargin + 2*xMin;
		ctx.canvas.height = canvasHeight;
		ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
	}

	// Render nodes in layer 
	function renderNodes(ctx, layerIndex) {
		let xPos = xMin + xMargin*layerIndex;
		let yPos = yMin;

		let isLargeLayer = layers[layerIndex].numNodes > largeLayerThreshold;
		let numNodes = Math.min(layers[layerIndex].numNodes, largeLayerThreshold);

		for (let i = 0; i < numNodes; i++) {
			ctx.beginPath();
			if (!isLargeLayer || i === 0 || i === numNodes - 1) {
				ctx.arc(xPos, yPos, 5, 0, 2 * Math.PI, false);
			}
			else {
				ctx.arc(xPos, yPos, 3, 0, 2 * Math.PI, false);
			}
			ctx.fillStyle = 'Green';
			ctx.fill();
			ctx.closePath();

			yPos += yMargin;
		}
	}

	// Generates the node indices if nodes are within threshold
	function generateNodeIndices(layerIndex) {
		let layer = layers[layerIndex];
		let nodeIndices = range(0, Math.min(layer.numNodes, largeLayerThreshold), 1);

		if (layer.numNodes > largeLayerThreshold) {
			let middleIndex = Math.floor(nodeIndices.length / 2.0);
			nodeIndices[middleIndex] = Math.floor(layer.numNodes / 2.0);

			for (let i = 1; i <= nodeIndices.length - middleIndex; i++) {
				nodeIndices[nodeIndices.length - i] = layer.numNodes - i;
			}
		}

		return nodeIndices;
	}

	// Render edges for each layer 
	function renderIncomingEdges(ctx, layerIndex) {
		let incomingNodeIndices = generateNodeIndices(layerIndex - 1);
		let outgoingNodeIndices = generateNodeIndices(layerIndex);

		let xStart = xMin + (layerIndex - 1) * xMargin;
		let xEnd = xMin + layerIndex * xMargin;

		if (currentHoveredWeightsIndex === layerIndex) {
			ctx.fillStyle = hoveredWeightsBackgroundColor;
			ctx.fillRect(xStart, 0, xMargin, ctx.canvas.height);
		}

		for (let i = 0; i < incomingNodeIndices.length; i++) {
			let yStart = yMin + i * yMargin;
			let incomingNodeIndex = incomingNodeIndices[i];

			for (let j = 0; j < outgoingNodeIndices.length; j++) {
				let yEnd = yMin + j * yMargin;
				let outgoingNodeIndex = outgoingNodeIndices[j];

				let weightValue = weightMatrices[layerIndex - 1][outgoingNodeIndex][incomingNodeIndex];

				ctx.beginPath();
				ctx.moveTo(xStart, yStart);
				ctx.lineTo(xEnd, yEnd);
				ctx.strokeStyle = getWeightColor(weightValue);
				ctx.stroke();
				ctx.closePath();
			}
		}
	}

	// Add buttons to control neural network including incrementing nodes, decrementing nodes, 
	// adding layers and deleting layers
	function renderControls(layerIndex) {
		let layerControls = layerControlsTemplate.content.cloneNode(true);

		let layerSizeInput = layerControls.querySelector(".layer-size-input");
		let layerSizeIncrementButton = layerControls.querySelector(".increment-button");
		let layerSizeDecrementButton = layerControls.querySelector(".decrement-button");
		let removeLayerButton = layerControls.querySelector(".remove-layer-button");
		let addLayerButton = layerControls.querySelector(".add-layer-button");

		let currentLayerSize = layers[layerIndex].numNodes;
		layerSizeInput.value = currentLayerSize;

		layerSizeInput.addEventListener("change", function() {
			let newSize = parseInt(layerSizeInput.value);
			if (newSize <= 0) {
				layerSizeInput.value = currentLayerSize;
				return;
			}

			changeLayerSize(layerIndex, newSize);
		});

		layerSizeIncrementButton.addEventListener("click", function () {
			changeLayerSize(layerIndex, currentLayerSize + 1);
		});

		layerSizeDecrementButton.addEventListener("click", function () {
			changeLayerSize(layerIndex, currentLayerSize - 1);
		});

		removeLayerButton.addEventListener("click", function() {
			mainThreadBridge.sendMessage("removeLayer", layerIndex);
		});

		addLayerButton.addEventListener("click", function() {
			createNewLayerModal(layerIndex + 1);
		});

		if (currentLayerSize === 1) {
			layerSizeDecrementButton.parentElement.removeChild(layerSizeDecrementButton);
		}

		if (layerIndex === 0) {
			removeLayerButton.parentElement.removeChild(removeLayerButton);
			addLayerButton.classList.add("no-remove");
		}

		if (layerIndex === layers.length - 1) {
			addLayerButton.parentElement.removeChild(addLayerButton);
			removeLayerButton.parentElement.removeChild(removeLayerButton);
		}

		networkControls.appendChild(layerControls);
	}

	// Update canvas width 
	function updateWidth() {
		let networkAreaWidth = 2 * xMin + (layers.length - 1) * xMargin;
		networkControls.width = networkAreaWidth;
		networkCanvas.width = networkAreaWidth;
	}

	//Renders the network (abridged version) on screen
	function render() {
		updateWidth();

		for (let i = 0; i < layers.length; i++) {
			if (i > 0) {
				renderIncomingEdges(canvasContext, i);
			}
			renderNodes(canvasContext, i);
			renderControls(i);
		}
	}

	// Rendering nodes and edges based on weights
	function renderAroundWeights(ctx, outgoingLayerIndex) {
		let startX = xMin + (outgoingLayerIndex - 1) * xMargin;
		ctx.clearRect(startX, 0, xMargin, ctx.canvas.height);

		renderIncomingEdges(ctx, outgoingLayerIndex);
		renderNodes(ctx, outgoingLayerIndex);
		renderNodes(ctx, outgoingLayerIndex - 1);
	}

	//Creates move movement hover effects
	function onCanvasMouseMove(event) {
		let oldHoveredWeightsIndex = currentHoveredWeightsIndex;

		let mouseX = event.clientX + networkWindow.scrollLeft - bodyLeftMargin;
		if (mouseX >= xMin && mouseX <= xMin + (layers.length - 1) * xMargin) {
			let networkX = mouseX - xMin;
			currentHoveredWeightsIndex = Math.floor(networkX / xMargin) + 1;
		}

		if (oldHoveredWeightsIndex !== -1) {
			renderAroundWeights(canvasContext, oldHoveredWeightsIndex);
		}

		if (currentHoveredWeightsIndex !== -1) {
			renderAroundWeights(canvasContext, currentHoveredWeightsIndex);
		}
	}

	// Handler for when the cursor leaves the canvas
	function onCanvasMouseOut() {
		currentHoveredWeightsIndex = -1;
		clear(canvasContext);
		render();
	}

	// Opens weight matrix of layer when clicked
	function onCanvasMouseClick() {
		if (currentHoveredWeightsIndex == -1) return;

		location.href = "weightmatrixview.html?layer=" + currentHoveredWeightsIndex;
	}
	
	//Loads the network data onto the display
	function onNetworkDataRetrieved(networkData) {
		loadingOverlay.classList.add("hide");
		layers = networkData.network.layers;
		//alert(networkData.weightMatrices);
		weightMatrices = networkData.weightMatrices;
		
		clear(canvasContext);
		render();
	}

	networkCanvas.addEventListener("mousemove", onCanvasMouseMove);
	networkCanvas.addEventListener("mouseout", onCanvasMouseOut);
	networkCanvas.addEventListener("click", onCanvasMouseClick);
	saveButton.addEventListener("click", saveAs);

	mainThreadBridge.toggleStacktrace();
	mainThreadBridge.registerThreadEventListener("retrieve", onNetworkDataRetrieved);
	mainThreadBridge.registerDefaultThreadEventListener(() => mainThreadBridge.sendMessage("retrieve"));
	mainThreadBridge.sendMessage("retrieve");

	return {

	};
})();