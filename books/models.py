from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from .validator import FileValidator
import io
from django.core.files.storage import default_storage as storage
from PIL import Image

class Book(models.Model):
	validate_file = FileValidator(max_size=50124 * 500, content_types=('application/pdf',))
	title = models.CharField(max_length=100)
	author = models.CharField(max_length=100)
	pdf = models.FileField(upload_to='books/pdfs/', validators=[validate_file])
	cover = models.ImageField(default='default.jpg', upload_to='books/cover/', null=True, blank=True)
	description = models.TextField(help_text='Short description about book', max_length=500, blank=True)
	cat_choice = (
				('Technology', 'Technology'),
				('Computer Programming', 'Computer Programming'),
				('Sci-Fi', 'Sci-Fi'),
				('Health', 'Health'),
				('Accounting', 'Accounting'),
				('Entrepreneurship', 'Entrepreneurship'),
				('Law', 'Law'),
				('Adventure', 'Adventure'),
				('Novel', 'Novel'),
				('Engineering', 'Engineering'),
				('Other', 'Other'),
			)
	category = models.CharField(verbose_name="Genre", max_length=100, choices=cat_choice)
	date_uploaded = models.DateTimeField(auto_now=True)
	uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
	afri_choice = (
				('Yes', 'Yes'),
				('No', 'No')
			)
	african_author = models.CharField(max_length=30, blank=True, null=True, choices=afri_choice)

	def __str__(self):
		return self.title

	# WITH PIL
	# def save(self, *args, **kwargs):
	# 	"""Resizing uploaded image files"""
	# 	super().save(*args, **kwargs)
	# 	img = Image.open(self.cover.path)
	# 	if img.height > 200 or img.width > 200:
	# 		output_size = (200, 200)
	# 		img.thumbnail(output_size)
	# 		img.save(self.cover.path)

	# WITH IO
	def save(self, *args, **kwargs):
	    super().save(*args, **kwargs)

	    img_read = storage.open(self.cover.name, 'r')
	    img = Image.open(img_read)

	    if img.height > 300 or img.width > 300:
	        output_size = (300, 300)
	        img.thumbnail(output_size)
	        in_mem_file = io.BytesIO()
	        img.save(in_mem_file, format='PNG')
	        img_write = storage.open(self.cover.name, 'w+')
	        img_write.write(in_mem_file.getvalue())
	        img_write.close()

	    img_read.close()

	def get_absolute_url(self):
		# redirect to book_detail.html
		return reverse('book_detail', kwargs={'pk': self.pk})

