let TEMPLATE_COMMENT, latest_alert
const comments_list = document.getElementById("comments")
const URL = window.location.pathname.split('/');
let comment = {
	is_anonymous: false,
	is_spoilers: false,
	content: "",
	parent_id: null,
	author: "",
}

function main() {
	const upvotes = document.getElementsByClassName("upvote")
	const downvotes = document.getElementsByClassName("downvote")
	const comments_request = new XMLHttpRequest()
	comments_request.open("GET", "/api/v1/literature_objects/" + URL[2] + "/comments/list?max-results=50&cursor=" + 0)
	comments_request.send()
	comments_request.onload = (e) => {
		if (comments_request.status == 200 && comments_request.responseText) {
			const data = JSON.parse(comments_request.responseText)
			if (data.success) {
				data["data"].forEach((comment) => {
					new Comment(comment)
				})
			}
		}
	}
	const comments_post = document.getElementById("comments_post")
	const comment_author = document.getElementById("comments_post_author")
	const is_spoilers_element = document.getElementById("is_contains_spoilers")
	const is_anonymous_element = document.getElementById("is_anonymous")
	const comment_content_element = document.getElementById("comments_post_content")
	const comment_post_button = document.getElementById("comments_post_send")
	comment_post_button.addEventListener("click", (e) => {
		const request = new XMLHttpRequest()
		request.open("POST", "/api/v1/literature_objects/" + URL[2] + "/comments/post")
		comment["is_anonymous"] = is_anonymous_element.checked === "true"
		comment["is_spoilers"] = is_spoilers_element.checked === "true"
		comment["author"] = comment_author.value
		comment["content"] = comment_content_element.value
		request.setRequestHeader("Content-Type", "application/json;charset=UTF-8")
		request.setRequestHeader("is-hide-name", comment["is_anonymous"])
		request.setRequestHeader("is-spoilers", comment["is_spoilers"])
		request.setRequestHeader("author-name", comment["author"])
		request.setRequestHeader("content", comment["content"]) // ı ve ş bozuk
		request.send()
		request.onload = (e) => {
			if (!request.responseText) {
				return
			}
			const data = JSON.parse(request.responseText)
			if (data.success) {
				new Comment(data.data)
				return
			}
			// something went wrong
			latest_alert?.remove()
			const error_message = Translated(data.error)
			const error = data.error
			console.log(error, ":", error_message)
			const new_alert = document.createElement("alert")
			new_alert.setAttribute("variant", "danger")
			new_alert.setAttribute("caption", Translated("error") + ": " + error)
			new_alert.innerText = error_message
			const button = document.createElement("button")
			button.setAttribute("slot", "action-secondary")
			button.innerText = Translated("ok")
			new_alert.appendChild(button)
			latest_alert = new_alert
			button.addEventListener("click", (e) => {
				new_alert.remove()
			})
			comments_post.appendChild(new_alert)
		}
	})

}
// function comment_page_changed(object) {
// 	console.log(object.getAttribute("current-page"), object.getAttribute("items-per-page"))
// }
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
		const upvote_button = new_comment.getElementsByClassName("upvote")[0]
		const downvote_button = new_comment.getElementsByClassName("downvote")[0]

		const comment_id = new_comment.getElementsByClassName("unknown-comment")[0]
		comment_id.id = comment_data.id
		new_comment.id = comment_data.id
		// text generations
		field_message_content.innerText = comment_data.content
		field_message_upvotes.innerText = comment_data.votes.up
		field_message_downvotes.innerText = comment_data.votes.down
		field_creator.innerText = comment_data.hide_name ? "anonim (" + comment_data.author.uid + ")" : comment_data.author.name + " (" + comment_data.author.uid + ")"
		// font styles
		if (comment_data.hide_name) {
			field_creator.style.fontStyle = "italic"
			field_creator.style.color = "rgba(255, 255, 255, 0.7)"
			field_creator.innerText = Translated("anonymous_author")
		}
		if (!comment_data.approved_by) {
			field_message_content.style.fontStyle = "italic"
			field_message_content.style.color = "rgba(255, 255, 255, 0.3)"
			field_message_content.innerText = Translated("comment_not_approved")
		}
		// events
		function handle_vote(value) {
			const get_old_vote = new Promise((resolve, reject) => {
				const is_voted_http = new XMLHttpRequest()
				is_voted_http.open("GET", `/api/v1/literature_objects/${URL[2]}/comments/${new_comment.id}/is_voted`)
				is_voted_http.send()
				is_voted_http.onload = (e) => {
					if (is_voted_http.status == 200 && is_voted_http.responseText) {
						const response = JSON.parse(is_voted_http.responseText)
						console.log(response)
						if (response.success) {
							console.log(response.data.value, value)
							if (response.data.value === value) {
								value = 0
							}
							resolve()
						} else {
							reject("hata ", response)
						}
					} else {
						reject("hata")
					}
				}
			})
			get_old_vote.then(() => {
				console.log(`downvoting ${new_comment.id}`)
				const http_request = new XMLHttpRequest()
				http_request.open("POST", `/api/v1/literature_objects/${URL[2]}/comments/${new_comment.id}/vote`)
				console.log(`sending vote with value ${value}`)
				http_request.setRequestHeader("vote-value", value)
				http_request.send()
				http_request.onload = (e) => {
					if (http_request.status == 200 && http_request.responseText) {
						const data = JSON.parse(http_request.responseText)
						if (data.success) {
							console.log(`oy verildi ${value}, ${data}`)
							field_message_upvotes.innerText = data.votes.up
							field_message_downvotes.innerText = data.votes.down
						} else {
							console.log("hata ", data)
						}
					} else {
						console.log("hata")
					}
				}
			})
		}
		downvote_button.addEventListener("click", () => {
			handle_vote(-1)
		})
		upvote_button.addEventListener("click", () => {
			handle_vote(1)
		})
		const created_at = new Date(comment_data.created_at)
		field_message_created_at.innerText = created_at.toLocaleString()
		comments_list.appendChild(new_comment)
	}
}
const comment_template_promise = new Promise((resolve, reject) => {
	const request = new XMLHttpRequest()
	request.open("GET", "/static/html/templates/comment.html")
	request.send()
	request.onload = (e) => {
		if (request.status == 200 && request.responseText) {
			TEMPLATE_COMMENT = request.responseText
			resolve()
		} else {
			reject("FAILED TO LOAD COMMENT.HTML")
		}
	}
})
comment_template_promise.then((e) => {
	main()
})