// HTTP Requests to backend

function deleteNote(noteId) {
	fetch("/delete-note", {
		method: "POST",
		body: JSON.stringify({ noteId: noteId }),
	}).then((_) => {
		console.log("deleting");
		window.location.href = "/";
	});
}

function deleteUser() {
	fetch("/delete-user", {
		method: "POST",
	}).then((_) => {
		console.log("Deleted user");
		window.location.href = "/login";
	});
}
