// Front-end functionality for the weight matrix page 

var controller = (function() {
	let url = document.URL;
	let indexOfEqualsSign = url.indexOf("=");
	let layerIndex = parseInt(url.substring(indexOfEqualsSign + 1));

	let arrayValues;

	let matrixCanvas = document.getElementById("matrix-canvas");
	let canvasContext = matrixCanvas.getContext("2d");
	
	// Clears the canvas
	function clear(ctx) {
		ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
	}

	// Renders the grid for the weight matrix
	function renderGrid(ctx) {
		if (arrayValues === undefined) return;

		let minWidth = ctx.canvas.width / arrayValues.length;
		let minHeight = ctx.canvas.height / arrayValues[0].length;
		let cellSize = Math.ceil(Math.min(minWidth, minHeight));

		for (let x = 0; x <= arrayValues.length - 1; x++) {
			for (let y = 0; y <= arrayValues[0].length - 1; y++) {
				ctx.fillStyle = getWeightColor(arrayValues[x][y]);
				ctx.fillRect(x * cellSize, y * cellSize, cellSize, cellSize);
			}
		}
	}

	// Main render method for the weight 
	// Also called on resizing of the window
	function render(){
		matrixCanvas.width = window.innerWidth - (window.innerWidth / 20);
		matrixCanvas.height = window.innerHeight - 120;

		// Clears then renders the grid
		clear(canvasContext);
		renderGrid(canvasContext);
	}

	//Received the data for the weight matrix and starts the render
	function setWeightMatrix(responseObject) {
		arrayValues = responseObject.weightMatrix;
		render();
	}

	mainThreadBridge.registerThreadEventListener("getWeightMatrix", setWeightMatrix);
	window.addEventListener("resize", render);

	mainThreadBridge.sendMessage("getWeightMatrix", layerIndex);

	return {

	};
})();