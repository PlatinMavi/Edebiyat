let TEMPLATE_COMMENT
const comments_list = document.getElementById("comments")
function main() {
	// document.addEventListener("scroll",(e)=>{
	// 	console.log(window.scrollY)
	// })
	const request = new XMLHttpRequest()
	request.open("GET", "/api/v1/literature_objects/" + "1" + "/comments/list?max-results=50&cursor=" + 0)
	request.send()
	request.onload = (e) => {
		if (request.status == 200 && request.responseText) {
			const data = JSON.parse(request.responseText)
			data.forEach((comment) => {
				new Comment(comment)
			})
		}
	}
}

class Comment {
	constructor(comment_data) {
		const new_comment = document.createElement("div")
		new_comment.className = "comment"
		new_comment.innerHTML = TEMPLATE_COMMENT
		const field_creator = new_comment.getElementsByClassName("comment-creator")[0]
		const field_message_content = new_comment.getElementsByClassName("comment-content")[0]
		const field_message_created_at = new_comment.getElementsByClassName("comment-created-at")[0]
		const field_message_upvotes = new_comment.getElementsByClassName("comment-upvotes")[0]
		const field_message_downvotes = new_comment.getElementsByClassName("comment-downvotes")[0]
		new_comment.id = comment_data.id
		field_message_content.innerText = comment_data.content
		field_message_upvotes.innerText = comment_data.votes.up
		field_message_downvotes.innerText = comment_data.votes.down
		field_creator.innerText = comment_data.hide_name ? "anonim (" + comment_data.author.uid + ")" : comment_data.author.name + " (" + comment_data.author.uid + ")"
		if (comment_data.hide_name) {
			field_creator.style.fontStyle = "italic"
		}
		field_message_downvotes.addEventListener("click",()=>{
			console.log("downvote")
		})
		const created_at = new Date(comment_data.created_at)
		field_message_created_at.innerText = created_at.toLocaleString()
		comments_list.appendChild(new_comment)
	}
}
const hello = new Promise((resolve, reject) => {
	const request = new XMLHttpRequest()
	request.open("GET", "/static/html/templates/comment.html")
	request.send()
	request.onload = (e) => {
		if (request.status == 200 && request.responseText) {
			TEMPLATE_COMMENT = request.responseText
			resolve()
		}
	}
})
hello.then((e) => {
	main()
})
