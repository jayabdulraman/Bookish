from django.shortcuts import render, get_object_or_404
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (
			TemplateView,
			ListView,
			CreateView,
			UpdateView,
			DeleteView
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from .models import UsefulLinks
from django.contrib import messages
from django.db.models import Q


class Home(TemplateView):
	template_name = 'books/book_list.html'


class UsefulListView(ListView):
	model = UsefulLinks
	template_name = 'useful_links/useful_list.html'
	context_object_name = 'useful'
	paginate_by = 4

	def get_queryset(self):
		query = self.request.GET.get('q')
		if query is not None:
			object_list = UsefulLinks.objects.filter(Q(title__icontains=query) | 
													 Q(category__icontains=query)
													 ).order_by('-date')
		else:
			object_list = UsefulLinks.objects.all().order_by('-date')
		return object_list


class LinkPostCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
	"""Create view that creates new posts.
	   create a urlpatterns route for ind. posts at urls.py
	   create template post_form.html under blog
	"""
	model = UsefulLinks
	fields = ['logo', 'title', 'description', 'category', 'url_link']
	success_url = reverse_lazy('useful')
	template_name = 'useful_links/post_url.html'
	success_message = "Post Link Successfully Created! Thank you for sharing!"

	def form_valid(self, form):
		"""creating new post's author before submission"""
		form.instance.uploaded_by = self.request.user
		return super().form_valid(form)


class CategoryUsefulView(ListView):
	model = UsefulLinks
	template_name = 'useful_links/useful_category.html' #<app>/<mode>_<viewtype>.html
	context_object_name = 'useful'
	paginate_by = 3

	def get_queryset(self):
		user = UsefulLinks
		if user is not None:
			object_list = user.objects.filter(category=self.kwargs.get('category')).order_by('-date')
		else:
			object_list = Book.objects.all().order_by('-date')
		print("Query: ", object_list)
		return object_list


class UserPostLinkListView(ListView):
	"""List view that displays all posts on user_posts
	   Make changes at urls.py to direct path to UserPostListView
	"""
	model = UsefulLinks
	template_name = 'useful_links/user_post_links.html' #<app>/<mode>_<viewtype>.html
	context_object_name = 'useful'
	paginate_by = 4

	def get_queryset(self):
		user = get_object_or_404(User, username=self.kwargs.get('uploaded_by'))
		return UsefulLinks.objects.filter(uploaded_by=user).order_by('-date')


class UsefulPostUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
	"""Create view that creates new posts.
	   create a urlpatterns route for ind. posts at urls.py
	   create template post_form.html under blog
	"""
	model = UsefulLinks
	fields = ['logo', 'title', 'description', 'category', 'url_link']
	template_name = 'useful_links/post_update.html'
	success_url = reverse_lazy('useful')
	success_message = "Post link Successfully Updated!"

	def form_valid(self, form):
		"""creating new post's author before submission"""
		form.instance.uploaded_by = self.request.user
		return super().form_valid(form)

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.uploaded_by:
			return True
		return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	"""deletes posts
	"""
	model = UsefulLinks
	template_name = 'useful_links/usefulpost_confirm_delete.html'
	success_url = reverse_lazy('useful')
	success_message = "'%(title)s' Link Successfully Deleted!"

	def test_func(self):
		post = self.get_object()
		if self.request.user == post.uploaded_by:
			return True
		return False

	def delete(self, request, *args, **kwargs):
		obj = self.get_object()
		messages.success(self.request, self.success_message % obj.__dict__)
		return super(PostDeleteView, self).delete(request, *args, **kwargs)

