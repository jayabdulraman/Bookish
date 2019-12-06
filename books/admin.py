from django.contrib import admin
from .models import Book

# Register your models here.
class BookAdmin(admin.ModelAdmin):
	list_display = ('title', 'author', 'cover', 'category', 'uploaded_by', 'date_uploaded')
	search_fields = ('title', 'author', 'description', 'category')
	readonly_fields = ('date_uploaded')

	filter_horizontal = ()
	list_filter = ('date_uploaded', 'category')
	fieldsets = ()

admin.site.register(Book, BookAdmin)
