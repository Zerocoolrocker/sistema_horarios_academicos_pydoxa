from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView

from .models import Proyecto, Seccion, Materia
# from .forms import ProyectoCreateForm


class DashboardView(TemplateView):
	template_name = 'dashboard.html'

class ProyectoEditView(TemplateView):
	template_name = 'proyecto_edit.html'

	def get(self, *args, **kwargs):
		if Proyecto.objects.filter(pk=kwargs['pk']).exists():
			proyecto = Proyecto.objects.get(pk=kwargs['pk'])
			self.proyecto = proyecto
			return super(ProyectoEditView, self).get(*args, **kwargs)
		return HttpResponseRedirect('/')

	def get_context_data(self, *args, **kwargs):
		data = super(ProyectoEditView, self).get_context_data(*args, **kwargs)
		data['proyecto'] = self.proyecto.nombre
		data['secciones'] = Seccion.objects.filter(proyecto=self.proyecto)
		data['todas_materias_pertinentes'] = Materia.objects.all()
		return data

class ProyectoCreateView(CreateView):
	template_name = 'proyecto_edit.html'
	model = Proyecto
	fields = '__all__'

	def get_success_url(self, *args, **kwars):
		return '/proyecto/%s/' % self.object.pk

class SeccionCreateView(CreateView):
	template_name = 'proyecto_edit.html'
	model = Seccion
	fields = '__all__'

	def get_success_url(self, *args, **kwars):
		return '/proyecto/%s/' % self.object.proyecto.pk


