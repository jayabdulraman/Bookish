from django.urls import path
from .views import (
	BookListView,
	UserBookListView,
	upload,
	BookDetailView,
	UploadBookView,
	BookDeleteView,
	CategoryListView,
	AfricanBookListView,
	SearchListView
	)

urlpatterns = [
	path('', BookListView.as_view(), name='book_list'),
	path('books/<str:uploaded_by>/', UserBookListView.as_view(), name='user_books'),
	path('category/<str:category>/', CategoryListView.as_view(), name='book_category'),
	path('african_author/<str:african_author>/', AfricanBookListView.as_view(), name='afri_author'),
	path('results/', SearchListView.as_view(), name='search'),
    path('upload/', upload, name='upload'),
    path('<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('book/upload/', UploadBookView.as_view(), name='upload_book'),
    path('book/<int:pk>/delete', BookDeleteView.as_view(), name='book_delete')

]