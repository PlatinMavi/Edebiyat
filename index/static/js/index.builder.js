const MONTHS = ["ocak", "şubat", "mart", "Nisan", "mayıs", "haziran", "temmuz", "ağustos", "eylül", "ekim", "kasım", "aralık"]

function create_literature_object_field() {}
function sleep(number) {
	var now = new Date().getTime()
	while (new Date().getTime() < now + number) {
		/* do nothing */
	}
}

function main() {
	var date = new Date()
	const this_month_text = MONTHS[date.getMonth()][0].toUpperCase() + MONTHS[date.getMonth()].slice(1) + ", " + date.getFullYear()
	document.getElementById("this_month").innerText = this_month_text
}
main()
