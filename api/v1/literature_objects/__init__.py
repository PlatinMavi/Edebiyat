from django.urls import path, include
from .comments.list import export as GET_comment_list
from .comments.post import export as POST_comment_post
from .comments.vote import export as POST_comment_vote
from .list import export as GET_books_list	

urlpatterns = [
		path("<int:object_id>/comments/post", view=POST_comment_post),
		path("<int:object_id>/comments/list", view=GET_comment_list),
		path("<int:object_id>/comments/<str:comment_id>/vote",view=POST_comment_vote), #allow -1 for book
		path("list", view=GET_books_list)
	]