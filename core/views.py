import json

from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import Proyecto, Seccion, Materia, Turno, Aula, Docente
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
        data['proyecto'] = self.proyecto
        data['form_errors'] = self.request.session.pop('form_errors', False)
        data['form_data'] = self.request.session.pop('form_data', False)
        if not data['form_data'] and self.request.session.get('update_form_data', False):
            data['form_data'] = self.request.session.pop('update_form_data', False)
            data['update_action'] = True
        data['secciones'] = Seccion.objects.filter(proyecto=self.proyecto)
        data['aulas'] = Aula.objects.all()
        data['todas_materias_pertinentes'] = Materia.objects.all()
        # @TODO: filtrar docentes por area aqui
        data['todos_docentes_pertinentes'] = Docente.objects.all()
        data['turnos'] = Turno.objects.all()
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

    def form_invalid(self, form, **kwars):
        self.request.session['form_errors'] = dict(form.errors)
        self.request.session['form_data'] = dict(form.data)
        return HttpResponseRedirect('/proyecto/%s/' % dict(form.data)['proyecto'][0])

class ConfirmacionEliminacionSeccionView(TemplateView):
    template_name = 'seccion_confirm_delete.html'

class SeccionDeleteView(View):
    model = Seccion

    def get(self, *args, **kwargs):
        if 'pk' in kwargs and self.model.objects.filter(pk=kwargs['pk']).exists():
            self.object = self.model.objects.get(pk=kwargs['pk'])
            proyecto = self.object.proyecto.pk
            self.object.delete()
            return HttpResponseRedirect('/proyecto/%s/' % proyecto  ) 
        return HttpResponseRedirect('/')

class SeccionUpdateView(UpdateView):
    model = Seccion
    fields = '__all__'

    def get(self, *args, **kwargs):
        def is_serializable(x):
            try:
                json.dumps(x)
                return True
            except:
                return False        

        if 'pk' in kwargs and self.model.objects.filter(pk=kwargs['pk']).exists():
            seccion = self.model.objects.get(pk=kwargs['pk'])
            self.request.session['update_form_data'] = {key:[value] for key, value in seccion.__dict__.items() if is_serializable(value)}
            return HttpResponseRedirect('/proyecto/%s/' % seccion.proyecto.pk  ) 
        return HttpResponseRedirect('/')

    def get_success_url(self, *args, **kwars):
        return '/proyecto/%s/' % self.object.proyecto.pk    

