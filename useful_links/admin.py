from django.contrib import admin
from .models import UsefulLinks

class LinksAdmin(admin.ModelAdmin):
	list_display = ('title', 'logo', 'category', 'url_link', 'date', 'uploaded_by')
	search_fields = ('title', 'category', 'url_link')
	readonly_fields = ('date')

	filter_horizontal = ()
	list_filter = ('category', 'date')
	# fieldsets = ()

admin.site.register(UsefulLinks, LinksAdmin)
