// Front-end functionality for creating modal with content

var createModal = function(modalContent, height, width)
{
	let modalWindow = document.createElement("div");
	modalWindow.classList.add("modal");
	modalWindow.style.marginLeft = "-" + (width / 2).toString() + "px";
	modalWindow.style.marginTop = "-" + (height / 2).toString() + "px";
	modalWindow.appendChild(modalContent);

	modalWindow.addEventListener("click", function(event) {
		event.stopPropagation();
	});

	let overlay = document.createElement("div");
	overlay.classList.add("overlay");
	overlay.appendChild(modalWindow);

	overlay.addEventListener("click", function() {
		overlay.parentElement.removeChild(overlay);
	});

	document.body.insertBefore(overlay, document.body.firstChild);

	return {
		destroy: function() {
			overlay.parentElement.removeChild(overlay);
		}
	}
};