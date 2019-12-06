from django import forms
from .models import Book

class BookForm(forms.ModelForm):
	class Meta:
		model = Book
		fields = ['title', 'author', 'pdf', 'cover', 'african_author', 'description', 'category']
		help_texts = {"african_author": "Please indicate 'Yes' if this book was written by an African Author or 'No' otherwise."}

