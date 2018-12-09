  // Function to decide what color to make the weight matrix grid sections

var getWeightColor = (function() {

  // Color gradients based on weight
  let red = [255, 60, 60];
  let blue = [0, 170, 255];
  return function(weightValue) {
    weightValue = (weightValue + 1) / 2; // Move from [-1,1] to [0,1]

    let color = [0, 0, 0];
    for (var i = 0; i < color.length; i++)
    {
      color[i] = Math.round(red[i] + weightValue * (blue[i] - red[i]));
    }

    //Function to decide what color the weight matrix grid based on the value between -1 and 1
    return "#" + ((1 << 24) + (color[0] << 16) + (color[1] << 8) + color[2]).toString(16).slice(1);
  };
})();