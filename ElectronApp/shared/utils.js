module.exports = {
    // Inverts an object
    // i.e. if the provided object is {"a" = "hello", "b" = "world"} then this will return {"world" = "b", "hello" = "a"}
    // Handles collisions randomly
	invertObject: function(object) {
		let invertedObject = {};

		for (let key in object) {
			let value = object[key];
			invertedObject[value] = key;
		}

		return invertedObject;
	},
    
    // Just generates a list of numbers in the range of [start, end) by iterating with stepSize
	range: function(start, end, stepSize) {
		let n = (end - start) / stepSize;
		let array = Array(n);

		for (let i = 0; i < n; i++) {
			array[i] = start + i*stepSize;
		}

		return array;
	}
};