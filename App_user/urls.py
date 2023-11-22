from django.urls import path
from . import views


urlpatterns = [
    path('registration/', views.registration, name = 'registro'),
    path('', views.loginWeb, name='login' ),
    path('home/', views.home, name = 'home'),
    path('logout/', views.logout_view, name = 'logout'),
    path('editarPerfil/', views.editarPerfil, name='editarPerfil'),
    path('editarContraseña/', views.editarContraseña, name='editarContraseña'),
    path('editarAvatar/', views.editarAvatar, name='editarAvatar'),
    path('productos/', views.crearProducto, name='productos'),
    path('productos/borrar/<int:producto_id>/', views.borrarProducto, name='borrarProducto'),
    path('productos/editarProducto/<int:producto_id>/', views.editarProducto, name='editarProducto'),
    path('ventas/', views.venta, name='ventas'),
    path('vistaClientes/<int:id>/', views.vistaClientes, name='vistaClientes'),
    path('invitados/', views.invitado, name= 'invitados'),
    path('crearPosteo/<int:id>/', views.crearPosteo, name='crearPosteo')
    

    


]