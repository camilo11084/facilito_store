from django import forms
#from django.contrib.auth.models import User
from users.models import User
class RegisterForm(forms.Form):

    username = forms.CharField(required=True, min_length=4, max_length=50, 
        widget=forms.TextInput(attrs=
        {'class':'form-control', 'id': 'username', }))


    email = forms.EmailField(required=True, widget=forms.EmailInput(
        attrs={ 'class': 'form-control',
        'id': 'email', 'placeholder': 'example@gmail.com'}))


    password = forms.CharField(required=True, widget=forms.PasswordInput(
        attrs={ 'class': 'form-control'}))

    password2 = forms.CharField(label='Confirma tu pasword', required=True, widget=forms.PasswordInput(attrs={'class':'form-control'}))


    

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('El username ya se encuentra en uso')

        return username


    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('El email ya se encuentra en uso')

        return email

    def clean(self):#utilizo este metodo cuando validemos un campo que dependa del otro, para este caso password2 de password1
        cleaned_data = super().clean()#andes de validar es importante ejecutar toda la informacion del formilario para eso el method clean

        if cleaned_data.get('password2') != cleaned_data.get('password'):
            self.add_error('password2', 'El password no coincide')

    def save(self): #se encargar de crear y persisitir el nuevo ususario apartir del username,email and password
        return User.objects.create_user(
            self.cleaned_data.get('username'),
            self.cleaned_data.get('email'),
            self.cleaned_data.get('password'),
        )
