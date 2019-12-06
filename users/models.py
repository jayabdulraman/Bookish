from django.db import models
from django.contrib.auth.models import User
import io
from django.core.files.storage import default_storage as storage
from PIL import Image
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	image = models.ImageField(default='default.jpg', upload_to='profile_pics')
	biography = models.TextField(blank=True, help_text='Tell us briefly about youself!')

	def __str__(self):
		return f'{self.user.username} Profile'


	# def save(self, *args, **kwargs):
	# 	"""Resizing uploaded image files"""
	# 	super().save(*args, **kwargs)
	# 	img = Image.open(self.image.path)
	# 	if img.height > 300 or img.width > 300:
	# 		output_size = (300, 300)
	# 		img.thumbnail(output_size)
	# 		img.save(self.image.path)


	def save(self, *args, **kwargs):
	    super().save(*args, **kwargs)

	    img_read = storage.open(self.image.name, 'r')
	    img = Image.open(img_read)

	    if img.height > 300 or img.width > 300:
	        output_size = (300, 300)
	        img.thumbnail(output_size)
	        in_mem_file = io.BytesIO()
	        img.save(in_mem_file, format='PNG')
	        img_write = storage.open(self.image.name, 'w+')
	        img_write.write(in_mem_file.getvalue())
	        img_write.close()

	    img_read.close()

