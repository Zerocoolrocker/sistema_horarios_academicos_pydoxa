import json

from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponse
from django.views.generic import TemplateView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .models import *
# from .forms import ProyectoCreateForm


class DashboardView(TemplateView):
    template_name = 'dashboard.html'

class ProyectoEditDragDropView(TemplateView):
    template_name = 'proyecto_edit_drag_drop.html'

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
        data['mostrar_modal'] = self.request.session.pop('mostrar_modal', False)
        if not data['form_data'] and self.request.session.get('update_form_data', False):
            data['form_data'] = self.request.session.pop('update_form_data', False)
            data['update_action'] = True
        if data['mostrar_modal'] == 'encuentro_create':
            data['seccion_encuentro'] = self.request.session.pop('seccion_encuentro')
            data['encuentros_dias'] = EncuentrosDias.objects.filter(encuentro__seccion__pk=data['seccion_encuentro'])
        data['secciones'] = Seccion.objects.filter(proyecto=self.proyecto)
        data['bloques'] = Bloque.objects.filter()
        data['aulas'] = Aula.objects.all()
        data['dias'] = Dia.objects.all()
        data['tipos_encuentros'] = (
            ('pr', 'Presencial'),
            ('vi', 'Virtual'),
        )
        data['todas_materias_pertinentes'] = Materia.objects.all()
        # @TODO: filtrar docentes por area aqui
        data['todos_docentes_pertinentes'] = Docente.objects.all()
        data['turnos'] = Turno.objects.all()
        return data

class ProyectoCreateView(CreateView):
    template_name = 'proyecto_edit.html'
    model = Proyecto
    fields = '__all__'

    def get_success_url(self, *args, **kwargs):
        return '/proyecto/%s/' % self.object.pk

class SeccionCreateView(CreateView):
    template_name = 'proyecto_edit.html'
    model = Seccion
    fields = '__all__'

    def get_success_url(self, *args, **kwargs):
        return '/proyecto/%s/' % self.object.proyecto.pk

    def form_invalid(self, form, **kwargs):
        self.request.session['mostrar_modal'] = 'seccion_create'
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
            self.request.session['mostrar_modal'] = 'seccion_create'
            return HttpResponseRedirect('/proyecto/%s/' % seccion.proyecto.pk  ) 
        return HttpResponseRedirect('/')

    def get_success_url(self, *args, **kwargs):
        return '/proyecto/%s/' % self.object.proyecto.pk


class EncuentroCreateView(CreateView):
    template_name = 'proyecto_edit.html'
    model = Encuentro
    fields = '__all__'

    def get_success_url(self, *args, **kwargs):
        self.request.session['mostrar_modal'] = 'encuentro_create'
        self.request.session['seccion_encuentro'] = self.object.seccion.pk
        return '/proyecto/%s/' % self.object.seccion.proyecto.pk

    def form_valid(self, form, **kwargs):
        res = super(EncuentroCreateView, self).form_valid(form, **kwargs)
        EncuentrosDias.objects.create(encuentro=self.object, dia=Dia.objects.get(pk=form.data['dia'][0]))
        return res


    def form_invalid(self, form, **kwargs):
        seccion = Seccion.objects.get(pk=dict(form.data)['seccion'][0])
        self.request.session['mostrar_modal'] = 'encuentro_create'
        self.request.session['seccion_encuentro'] = seccion.pk
        self.request.session['form_errors'] = dict(form.errors)
        self.request.session['form_data'] = dict(form.data)
        return HttpResponseRedirect('/proyecto/%s/' % seccion.proyecto.pk)

class SeccionEncuentrosListView(TemplateView):
    template_name = 'proyecto_edit.html'

    def get(self, *args, **kwargs):
        self.request.session['mostrar_modal'] = 'encuentro_create'
        self.request.session['seccion_encuentro'] = self.request.GET.get('seccion')
        return HttpResponseRedirect('/proyecto/%s/' % self.request.GET.get('seccion'))





# class EncuentroUpdateView(UpdateView):
#     model = Seccion
#     fields = '__all__'

#     def get(self, *args, **kwargs):
#         def is_serializable(x):
#             try:
#                 json.dumps(x)
#                 return True
#             except:
#                 return False        

#         if 'pk' in kwargs and self.model.objects.filter(pk=kwargs['pk']).exists():
#             seccion = self.model.objects.get(pk=kwargs['pk'])
#             self.request.session['update_form_data'] = {key:[value] for key, value in seccion.__dict__.items() if is_serializable(value)}
#             return HttpResponseRedirect('/proyecto/%s/' % seccion.proyecto.pk  ) 
#         return HttpResponseRedirect('/')

#     def get_success_url(self, *args, **kwargs):
#         return '/proyecto/%s/' % self.object.proyecto.pk           



class EncuentrosAPIListView(View):

    def get(self, request, *args, **kwargs):
        # @TODO: filtrar aqui por proyecto actual
        # @TODO: validar que el usuario logueado tenga permiso a acceder a los datos del proyecto
        filtros = {}
        if 'proyecto' in request.GET:
            filtros['seccion__proyecto__pk'] = request.GET['proyecto']
        if 'aula' in request.GET:
            filtros['aula'] = request.GET['aula']
        objetos = Encuentro.objects.filter(**filtros).all()
        datos = [
            {
                "pk": x.pk,
                "tipo": x.tipo,
                "seccion": {
                    "pk": x.seccion.pk,
                    "numero": x.seccion.numero,
                    "materia": {
                        "pk": x.seccion.materia.pk,
                        "codigo": x.seccion.materia.codigo,
                        "nombre": x.seccion.materia.nombre,
                        "pensum": x.seccion.materia.pensum.nombre,
                    },
                },
                "aula": {
                    "pk": x.aula.pk,
                    "numero": x.aula.numero,
                    "nombre": x.aula.nombre,
                    "tipo": x.aula.tipo_aula.modalidad,
                    "ubicacion": x.aula.ubicacion.nombre,
                },


            }
            for x in objetos
        ]
        datos = json.dumps(datos)
        return HttpResponse(datos, content_type='application/json')
