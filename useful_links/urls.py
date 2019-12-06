from django.urls import path
from .views import (
	UsefulListView,
	LinkPostCreateView,
	UserPostLinkListView,
	CategoryUsefulView,
	UsefulPostUpdateView,
	PostDeleteView
	)

urlpatterns = [
	path('useful_links/', UsefulListView.as_view(), name='useful'),
	path('useful_links/new/', LinkPostCreateView.as_view(), name='post_url'),
	path('useful_links/<str:uploaded_by>/', UserPostLinkListView.as_view(), name='user_links'),
	path('useful_links/cat/<str:category>/', CategoryUsefulView.as_view(), name='useful_category'),
	path('useful_links/<int:pk>/update/', UsefulPostUpdateView.as_view(), name='post_update'),
	path('useful_links/<int:pk>/delete/', PostDeleteView.as_view(), name='post_delete')
]
