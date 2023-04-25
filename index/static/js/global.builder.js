function Translated(key) {
	return window["translation-data"][key] || Translated("unknown_translation")
}
function global() {
	console.log("Loading global.js")
	document.querySelectorAll("[translated]").forEach((element) => {
		console.log("Translating", element)
		const key = element.getAttribute("translated")
		if (key) {
			console.log("Translated", key)
			element.innerText = Translated(key)
		}
	})
}
window["language"] = window["language"] || "tr"
console.log("Language:", window["language"])
const language_request = new XMLHttpRequest()
language_request.open("GET", "/api/v1/translations/" + window.language)
language_request.send()
language_request.onload = (e) => {
	if (language_request.status === 200) {
		const data = JSON.parse(language_request.responseText)
		if (data.success) {
			window["translation-data"] = data["data"]
			global()
		} else {
			window.location.reload()
		}
	}
}
