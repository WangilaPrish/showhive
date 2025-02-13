from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import get_user_model

# Get the actual user model (supporting custom user models)
User = get_user_model()

class CustomAuthenticationForm(AuthenticationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
        label="Email",
    )
   
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter your password'}),
        label="Password",
    )

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError("This account is inactive.", code='inactive')

    def clean_username(self):
        email = self.cleaned_data.get('email')
        # Check if the email exists in the database
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise forms.ValidationError("The email you entered is not registered. Please register.")
        
        # Set the username field to the email for authentication purposes
        self.cleaned_data['username'] = user.username
        return email
