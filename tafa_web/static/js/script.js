function alert_(title, text, type = "info") {
	swal({
	  title: title,
	  text: text,
	  icon: type,
	  button: true,
	});
}

function sleep(ms) {
	return new Promise(resolve => setTimeout(resolve, ms));
}
