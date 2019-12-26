from django.contrib.auth.forms import UserCreationForm , forms , AuthenticationForm , UsernameField
from django.contrib.auth.models import User 
from django.contrib.auth import authenticate
from django.utils.translation import gettext, gettext_lazy as _

class UserLoginForm(forms.Form):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password'}),
    )

    error_message = {
        'username': _('The %(username)s doesn\'t Exists Please Register to come in our members ^_^'),
        'password': 'Incorrect password. please Try again with correct Password',  
        
    }

    def clean(self, *args , **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get('password')

        user = User.objects.get(username=username)

        if  not user.check_password(password):
            raise forms.ValidationError(self.error_message['password'] , code=self.error_message['password'])

    
            
        return super(UserLoginForm, self).clean(*args , **kwargs)

class UserRegisterForm(forms.ModelForm):

    first_name = forms.CharField(max_length=100 , min_length=4 , help_text='should enter at least 4 characters and at most 100 characters')
    last_name  = forms.CharField(max_length=100 , min_length=4 , help_text='should enter at least 4 characters and at most 100 characters')
    email      = forms.EmailField(max_length=150)
    username   = forms.CharField(help_text="Required. 150 characters or fewer.Letters,digits and @/./+/-/_ only.")
    password   = forms.CharField(min_length=8 , widget=forms.PasswordInput ,help_text=[
        "Your Password can't be too similar to your other personal information.",
        "Your Password must contain at least 8 characters."
        "Your Password can't be a commonly used password.",
        "Your Password can't be entirely numeric."]
        )
    password1  = forms.CharField(min_length=8 , widget=forms.PasswordInput , 
                                 help_text="Enter the same password as before,for validtion.") 
    
    errors_messages = {
        'password_mismatch': "The two password fields didn’t match.",
    }
    class Meta:
        model = User
        fields = ['first_name' , 'last_name' , 'username' , 'email' , 'password']
        
    def clean_password1(self):

        password  = self.cleaned_data.get('password')
        password1 = self.cleaned_data.get('password1')
        
        if password and password1 and password != password1:
            raise forms.ValidationError( self.errors_messages['password_mismatch'], code='password_mismatch' )

        return password1
    
    def clean_email(self):
        
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Please use another Email,That is already taken')
        
        return email


    def save(self , commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class PasswordResetForm(forms.Form):
    username_email = forms.CharField(label='Username or Email' , widget=forms.TextInput(attrs={'autofocus': True}))


class ResetNewPasswordForm(forms.ModelForm):
    password   = forms.CharField(min_length=8 , widget=forms.PasswordInput ,help_text=[
        "Your Password can't be too similar to your other personal information.",
        "Your Password must contain at least 8 characters."
        "Your Password can't be a commonly used password.",
        "Your Password can't be entirely numeric."]
        )
    password1  = forms.CharField(min_length=8 , widget=forms.PasswordInput , 
                                 help_text="Enter the same password as before,for validtion.") 
    
    errors_messages = {
        'password_mismatch': "The two password fields didn’t match.",
    }

    class Meta:
        model = User
        fields = ['password']
        
    def clean_password1(self):

        password  = self.cleaned_data.get('password')
        password1 = self.cleaned_data.get('password1')
        
        if password and password1 and password != password1:
            raise forms.ValidationError( self.errors_messages['password_mismatch'], code='password_mismatch' )

        return password1
