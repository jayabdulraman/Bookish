from django.db import models
from django.contrib.auth.models import User
import io
from django.core.files.storage import default_storage as storage
from PIL import Image


class UsefulLinks(models.Model):
	title = models.CharField(max_length=100)
	logo = models.ImageField(default='default.jpg', upload_to='links/logos/', null=True, blank=True)
	description = models.TextField(help_text='Short description about website/course/link', max_length=500, blank=True)
	category = models.CharField(verbose_name="Genre", max_length=100, help_text="Genre can be in Computer Programming,\
								Business, Law, Medicine, Engineering, Accounting etc. Just one that fit the description of the url!")
	url_link = models.URLField(max_length=200, help_text='Please indicate the correct url!')
	date = models.DateTimeField(auto_now=True)
	uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.title


	# def save(self, *args, **kwargs):
	# 	"""Resizing uploaded image files"""
	# 	super().save(*args, **kwargs)
	# 	img = Image.open(self.logo.path)
	# 	if img.height > 200 or img.width > 200:
	# 		output_size = (200, 200)
	# 		img.thumbnail(output_size)
	# 		img.save(self.logo.path)

	def save(self, *args, **kwargs):
	    super().save(*args, **kwargs)

	    img_read = storage.open(self.logo.name, 'r')
	    img = Image.open(img_read)

	    if img.height > 300 or img.width > 300:
	        output_size = (300, 300)
	        img.thumbnail(output_size)
	        in_mem_file = io.BytesIO()
	        img.save(in_mem_file, format='PNG')
	        img_write = storage.open(self.logo.name, 'w+')
	        img_write.write(in_mem_file.getvalue())
	        img_write.close()

	    img_read.close()


