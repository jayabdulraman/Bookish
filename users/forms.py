from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

class UserRegisterForm(UserCreationForm):
	email = forms.EmailField(help_text="Enter valid email address! Useful to change password!")
	# register = forms.CharField(widget=forms.Textarea, help_text='Tell us briefly into about you!')

	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

	def clean_email(self):
		email = self.cleaned_data.get('email')

		try:
			match = User.objects.get(email=email)
		except:
			return email
		raise forms.ValidationError('A user with that email already exists.')

class UserUpdateForm(forms.ModelForm):
	"""UPDATE USER PROFILE ON THE FRONT END"""
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ['username', 'email']

	def clean_email(self):
		# Check that email is not duplicate
		username = self.cleaned_data["username"]
		email = self.cleaned_data["email"]
		users = User.objects.filter(email__iexact=email).exclude(username__iexact=username)
		if users:
			raise forms.ValidationError('A user with that email already exists.')
		return email.lower()

class ProfileUpdateForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['image', 'biography']
		
