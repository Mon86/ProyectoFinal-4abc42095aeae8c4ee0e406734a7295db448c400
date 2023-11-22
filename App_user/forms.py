from typing import Any, Dict
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Producto, Venta, Posteos
from django.forms import formset_factory



class RegistroForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ['username', 'first_name','last_name','email']
        labels = {
            'username' : 'Nombre de usuario',
            'first_name' : 'Nombre completo',
            'last_name': 'Nombre del negocio',
            'email' : 'email'
        }

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if User.objects.filter(last_name=last_name).exists():
            raise forms.ValidationError('Ese nombre de negocio ya está registrado.')
        return last_name


class UserEditForm(UserChangeForm):
    username = forms.CharField(widget= forms.TextInput(attrs={"placeholder": "Username"}))
    email = forms.EmailField(widget= forms.TextInput(attrs={"placeholder": "Email"}))
    first_name = forms.CharField(widget= forms.TextInput(attrs={"placeholder": "Primer nombre"}), label= "Nombre completo")
    last_name = forms.CharField(widget= forms.TextInput(attrs={"placeholder": "Nombre del negocio"}), label="Nombre del negocio")
    password = None
    
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name']
        help_text = {k:"" for k in fields}


class UserChangePassword(PasswordChangeForm):
    old_password = forms.CharField(label= "Contraseña vieja", widget= forms.PasswordInput(attrs={"placeholder": "Contraseña vieja"}))
    new_password1 = forms.CharField(label= "Contraseña nueva", widget= forms.PasswordInput(attrs={"placeholder": "Contraseña nueva"}))
    new_password2 = forms.CharField(label= "Contraseña nueva", widget= forms.PasswordInput(attrs={"placeholder": "Confirmar contraseña nueva"}))
    
    
    class Meta:
        model = User
        fields = ['old_password','new_password1','new_password2']
        help_text = {k:"" for k in fields}


class AvatarForm(forms.Form):
    avatar = forms.ImageField(required= False)

class AvatarDescriptionForm(forms.Form):
    description = forms.CharField(widget= forms.Textarea(attrs={"placeholder": "Descripcion del negocio con vista al publico"}), label= "Descripcion del negocio con vista al publico", required= False)



class productoForm(forms.ModelForm):
    id = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Producto
        fields = ['id', 'bars_code', 'nombre_producto', 'descripcion_producto', 'stock_producto', 'precio_producto', 'imagen_producto']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['imagen_producto'].required = False



class ventaForm(forms.ModelForm):
    producto = forms.ModelChoiceField(queryset=Producto.objects.none(), to_field_name='id', widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = Venta
        fields = ['producto', 'cantidad']
        widgets = {
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['producto'].queryset = Producto.objects.filter(usuario=user)




class posteoForm(forms.ModelForm):
    class Meta:
        model = Posteos
        fields = ["contenido", 'imagen']
        widgets = {
            'contenido': forms.Textarea()
        }