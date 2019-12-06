from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import TemplateView, ListView, CreateView, DeleteView, DetailView
from django.core.files.storage import FileSystemStorage
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User

from .forms import BookForm
from .models import Book

class Home(TemplateView):
	template_name = 'books/book_list.html'

def upload(request):
	context = {}
	if request.method == 'POST':
		uploaded_file = request.FILES['document']
		fs = FileSystemStorage()
		name = fs.save(uploaded_file.name, uploaded_file)
		context['url'] = fs.url(name)
	return render(request, 'books/upload.html', context)


def book_list(request):
	books = Book.objects.all()
	return render(request, 'books/book_list.html',
		{'books': books})


def upload_book(request):
	if request.method == 'POST':
		form = BookForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return redirect('book_list')
	else:
		form = BookForm()

	return render(request, 'books/upload_book.html', 
		{'form': form})


class BookListView(ListView):
	model = Book
	template_name = 'books/book_list.html'
	context_object_name = 'books'
	ordering = ['-date_uploaded']
	paginate_by = 6

	def get_queryset(self):
		query = self.request.GET.get('q')
		if query is not None:
			object_list = Book.objects.filter(Q(title__icontains=query) |
											  Q(category__icontains=query)).order_by('-date_uploaded')
		else:
			object_list = Book.objects.all().order_by('-date_uploaded')
		return object_list


class UserBookListView(ListView):
	"""List view that displays all posts on user_posts
	   Make changes at urls.py to direct path to UserPostListView
	"""
	model = Book
	template_name = 'books/user_books.html' #<app>/<mode>_<viewtype>.html
	context_object_name = 'books'
	paginate_by = 3

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('uploaded_by'))
		return Book.objects.filter(uploaded_by=user).order_by('-date_uploaded')

class AfricanBookListView(ListView):
	"""List view that displays all posts on user_posts
	   Make changes at urls.py to direct path to UserPostListView
	"""
	model = Book
	template_name = 'books/african_author.html' #<app>/<mode>_<viewtype>.html
	context_object_name = 'books'
	paginate_by = 3

	def get_queryset(self):
		user = Book
		if user is not None:
			object_list = user.objects.filter(african_author=self.kwargs.get('african_author')).order_by('-date_uploaded')
		else:
			object_list = Book.objects.all().order_by('-date_uploaded')
		print("Query: ", object_list)
		return object_list


class CategoryListView(ListView):
	model = Book
	template_name = 'books/category.html' #<app>/<mode>_<viewtype>.html
	context_object_name = 'books'
	paginate_by = 3

	def get_queryset(self):
		user = Book
		if user is not None:
			object_list = user.objects.filter(category=self.kwargs.get('category')).order_by('-date_uploaded')
		else:
			object_list = Book.objects.all().order_by('-date_uploaded')
		# print("Query: ", object_list)
		return object_list



class BookDetailView(DetailView):
	"""Detail view that displays details of individual books 
	   on home. create a urlpatterns route for ind. posts at urls.py
	   create template post_detail.html under blog
	"""
	model = Book


class UploadBookView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
	model = Book
	form_class = BookForm
	success_url = reverse_lazy('book_list')
	template_name = 'books/upload_book.html'
	success_message = 'Thank you for uploading a book! Sharing is Caring!'

	def form_valid(self, form):
		"""creating new post's author before submission"""
		form.instance.uploaded_by = self.request.user
		return super().form_valid(form)


class BookDeleteView(SuccessMessageMixin, DeleteView):
	"""deletes books
	"""
	model = Book
	success_url = reverse_lazy('book_list')
	success_message = "'%(title)s' Book Successfully Deleted!"
	def test_func(self):
		book = self.get_object()
		if self.request.user == book.uploaded_by:
			return True
		return False

	def delete(self, request, *args, **kwargs):
		obj = self.get_object()
		messages.success(self.request, self.success_message % obj.__dict__)
		return super(BookDeleteView, self).delete(request, *args, **kwargs)


