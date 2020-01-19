"""pycronos URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from core.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('proyecto/', ProyectoCreateView.as_view(), name='dashboard'),
    path('proyecto/<int:pk>/', ProyectoEditView.as_view(), name='editar_proyecto'),
    path('seccion/', SeccionCreateView.as_view(), name='crear_seccion'),
    path('encuentro/', EncuentroCreateView.as_view(), name='crear_encuentro'),
    path('seccion-encuentros/', SeccionEncuentrosListView.as_view(), name='seccion_encuentros_list'),
    # path('seccion/<int:pk>/delete/', ConfirmacionEliminacionSeccionView.as_view(), name='eliminar_seccion'),
    path('seccion/<int:pk>/delete/', SeccionDeleteView.as_view(), name='eliminar_seccion'),
    path('seccion/<int:pk>/update/', SeccionUpdateView.as_view(), name='actualizar_seccion'),
    path('', DashboardView.as_view(), name='project-edit'),
    path('proyectodnd/<int:pk>/', ProyectoEditDragDropView.as_view(), name='editar_proyecto_dnd'),
    path('api/encuentros/', EncuentrosAPIListView.as_view(), name='api_encuentros_list'),
    path('api/bloques/', BloquesAPIListView.as_view(), name='api_bloques_list'),
    path('api/aulas/', AulasAPIListView.as_view(), name='api_aulas_list'),
    path('api/dias/', DiasAPIListView.as_view(), name='api_dias_list'),
    path('api/encuentros/update/', EncuentrosAPIUpdateView.as_view(), name='api_encuentros_update'),
]
