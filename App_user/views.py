from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegistroForm, UserEditForm, UserChangePassword, AvatarForm, productoForm, AvatarDescriptionForm, ventaForm, posteoForm
from .models import Avatar, Producto as Productos, Posteos
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory

# Create your views here.
def get_default_user():
    return User.objects.get(id=1)

def invitado(request):
    usuario = User.objects.all()
    return render(request, 'App_user/invitados.html', {'users': usuario})

def registration(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exists():
                form.add_error('email', 'El email ya está registrado.')
            else:
                form.save()
                messages.success(request, '¡Registro exitoso! Ahora puedes iniciar sesión.')
                return redirect('../')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error en el campo "{field}": {error}')
    
    else: 
        form = RegistroForm()
    
    return render(request, 'App_user/registro.html', {'form': form})

def loginWeb(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("../home")
            else:
                return render(request, 'App_user/login.html', {'form': form, 'error': 'Usuario o contraseña incorrectos'})
    else:
        form = AuthenticationForm()
    
    return render(request, 'App_user/login.html', {'form': form})

@login_required    
def home(request):
    return render(request, "App_user/home.html")

@login_required
def logout_view(request):
    logout(request)
    return redirect("../")

@login_required
def editarPerfil(request):
    avatar = getAvatar(request)
    usuario = request.user
    user_basic_info = User.objects.get(id=usuario.id)
    if request.method == "POST":
        form = UserEditForm(request.POST, instance=usuario)
        if form.is_valid():
            user_basic_info.username = form.cleaned_data.get('username')
            user_basic_info.email = form.cleaned_data.get('email')
            user_basic_info.first_name = form.cleaned_data.get('first_name')
            user_basic_info.last_name = form.cleaned_data.get('last_name')
            user_basic_info.save()
            messages.success(request, '¡Perfil actualizado exitosamente!')
            return redirect('../home')
        else:
            form = UserEditForm(initial={'username': usuario.username, 'email': usuario.email, 'first_name': usuario.first_name, 'last_name': usuario.last_name})
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error en el campo "{field}": {error}')
            return render(request, 'App_user/editarPerfil.html', {"form": form })
    else:
        form = UserEditForm(initial={'username': usuario.username, 'email': usuario.email, 'first_name': usuario.first_name, 'last_name': usuario.last_name})
        return render(request, 'App_user/editarPerfil.html', {"form": form, "avatar": avatar})
    


@login_required
def editarContraseña(request):
    avatar = getAvatar(request)
    usuario = request.user 
    if request.method == 'POST':
        form = UserChangePassword(data=request.POST, user=usuario)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Contraseña actualizada exitosamente.')
            return redirect('../editarPerfil')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error en el campo "{field}": {error}')
            return redirect('../editarContraseña')
    else: 
        form = UserChangePassword(user=usuario)
        return render(request, 'App_user/editarContraseña.html', {"form": form, "avatar": avatar})
    


@login_required
def editarAvatar(request):
    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES)
        form2 = AvatarDescriptionForm(request.POST)
        if form.is_valid() and form2.is_valid():
            avatar_anterior = Avatar.objects.filter(user=request.user)
            if (len(avatar_anterior) > 0):
                avatar_anterior.delete()
            usuario = User.objects.get(username=request.user)
            avatar = Avatar(user=usuario, image=form.cleaned_data['avatar'], description=form2.cleaned_data['description'])
            avatar.save()
            messages.success(request, '¡Avatar actualizado exitosamente!')
            return redirect('../editarPerfil')
    else:
        form = AvatarForm()
        form2 = AvatarDescriptionForm()
        avatar = getAvatar(request)
    return render(request, 'App_user/editarAvatar.html', {'form': form, 'form2': form2, 'avatar': avatar})


@login_required
def getDescription(request):
    avatar = Avatar.objects.filter(user = request.user.id).first()
    if avatar.description:
        return avatar.description
    else:
        return 'Actualmente no hay ninguna descripcion'
    

@login_required
def getAvatar(request):
    avatar = Avatar.objects.filter(user=request.user.id)
    try:
        avatar = avatar[0].image.url
    
    except:
        avatar = None

    return avatar


@login_required
def crearProducto(request):
    avatar = getAvatar(request)
    if request.method == 'POST':
        miFormulario = productoForm(request.POST, request.FILES)
        if miFormulario.is_valid():
            producto = miFormulario.save(commit=False)
            producto.usuario = request.user 
            producto.save()

            miFormulario.save()
            messages.success(request, "Producto registrado exitosamente") 
            return redirect('productos')
    productos = Productos.objects.filter(usuario = request.user)

    miFormulario = productoForm()
    return render(request, 'App_user/productos.html', {'form': miFormulario, "avatar": avatar, "productos": productos})




@login_required
def borrarProducto(request, producto_id):
    producto = get_object_or_404(Productos, id=producto_id)
    if producto.usuario == request.user:
        producto.delete()
        messages.success(request, 'Producto eliminado exitosamente.')
    else:
        messages.error(request, 'No tienes permiso para eliminar este producto.')
    return redirect('productos')


@login_required
def editarProducto(request, producto_id):
    avatar = getAvatar(request)
    producto = get_object_or_404(Productos, id=producto_id, usuario=request.user)

    if request.method == 'POST':
        form = productoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado exitosamente.')
            return redirect('productos')
    else:
        form = productoForm(instance=producto)

    return render(request, 'App_user/editarProducto.html', {'form': form, 'avatar': avatar})

@login_required
def venta(request):
    if request.method == 'POST':
        form = ventaForm(request.POST, user = request.user)
        if form.is_valid():
            producto = form.cleaned_data['producto']
            cantidad = form.cleaned_data['cantidad']
            if cantidad is not None and cantidad > producto.stock_producto:
                form.add_error('cantidad', 'La cantidad solicitada supera el stock disponible')
                messages.error(request, 'No hay suficiente stock para vender esa cantidad')
            else:
                producto.stock_producto -= cantidad
                producto.save()
                messages.success(request, 'Venta realizada con exito.')
                return redirect('ventas')
    else:
        form = ventaForm(user = request.user)

    return render(request, 'App_user/ventas.html', {'form': form})


def vistaClientes(request, id):
    usuario = get_object_or_404(User, id = id)
    productos = Productos.objects.filter(usuario_id = id)
    posteos = Posteos.objects.filter(usuario = usuario)
    return render(request, 'App_user/vistaClientes.html', {'usuario': usuario, 'productos': productos, 'posteos':posteos })



@login_required
def crearPosteo(request, id):
    avatar = getAvatar(request)
    if request.method == 'POST':
        posteoform =  posteoForm(request.POST   , request.FILES)
        if posteoform.is_valid():
            posteo = posteoform.save(commit=False)
            posteo.usuario = request.user
            posteo.save()
            return redirect('vistaClientes', id = id)
    else:
        posteoform = posteoForm()

    return render(request, 'App_user/crearPosteo.html', {'posteoform':posteoform, 'avatar':avatar })







    