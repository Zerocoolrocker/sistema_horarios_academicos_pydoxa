import datetime
import json

from django.http import HttpResponseRedirect, HttpResponseBadRequest, HttpResponse
from django.views.generic import TemplateView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from .models import *


class DashboardView(TemplateView):
    template_name = 'dashboard.html'

class ProyectoEditDragDropView(TemplateView):
    template_name = 'proyecto_edit_drag_drop.html'

    def get(self, *args, pk=None, **kwargs):
        self.proyecto = Proyecto.objects.filter(pk=pk).first()
        if self.proyecto:
            return super(ProyectoEditDragDropView, self).get(*args, **kwargs)
        return HttpResponse(status=404)
            

    def get_context_data(self, *args, **kwargs):
        data = super(ProyectoEditDragDropView, self).get_context_data(*args, **kwargs)
        data['aulas'] = Aula.objects.filter(carrera=self.proyecto.pensum.carrera).order_by('nombre')
        data['proyecto'] = self.proyecto.pk
        data['carrera'] = self.proyecto.pensum.carrera.pk
        return data


class ProyectoEditView(TemplateView):
    template_name = 'proyecto_edit.html'

    def get(self, *args, **kwargs):
        if Proyecto.objects.filter(pk=kwargs['pk']).exists():
            self.proyecto = Proyecto.objects.get(pk=kwargs['pk'])
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
        data['pensums'] = Pensum.objects.all()
        data['pk_pensum_mas_reciente'] = getattr(Pensum.objects.last(), 'pk', '')
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


@method_decorator(csrf_exempt, name='dispatch')
class EncuentrosAPIUpdateView(View):
    def post(self, request, *args, **kwargs):
        obj = EncuentrosDias.objects.get(pk=request.POST['pk'])
        hora_inicio, minutos_inicio, segundos_inicio = map(int, request.POST['hora_inicio'].split(':'))
        dia = Dia.objects.get(pk=request.POST['dia'])
        bloque = Bloque.objects.get(hora_inicio=datetime.time(hour=hora_inicio, minute=minutos_inicio, second=segundos_inicio))
        obj.encuentro.bloque = bloque
        obj.encuentro.save()
        obj.dia = dia
        obj.encuentro.aula = Aula.objects.get(pk=request.POST['aula'])
        obj.encuentro.save()
        obj.save()
        return HttpResponse()


class EncuentrosAPIListView(View):

    def get(self, request, *args, **kwargs):
        # @TODO: validar que el usuario logueado tenga permiso a acceder a los datos del proyecto
        filtros = {}
        if 'proyecto' in request.GET:
            filtros['encuentro__seccion__proyecto__pk'] = request.GET['proyecto']
        if 'aula' in request.GET:
            filtros['encuentro__aula'] = request.GET['aula']
        objetos = EncuentrosDias.objects.filter(**filtros).all()
        objetos = sorted(objetos, key=lambda x: (x.encuentro.bloque.hora_inicio, x.dia.dia))
        datos = [
            {
                "pk": x.encuentro.pk,
                "encuentro_dia_pk": x.pk,
                "tipo": x.encuentro.tipo,
                "dia": x.dia.get_dia_display(),
                "dia_pk": x.dia.dia,
                "seccion": {
                    "pk": x.encuentro.seccion.pk,
                    "numero": x.encuentro.seccion.numero,
                    "docente": x.encuentro.seccion.docente.nombres,
                    "cupo": x.encuentro.seccion.cupo,
                    "materia": {
                        "pk": x.encuentro.seccion.materia.pk,
                        "codigo": x.encuentro.seccion.materia.codigo,
                        "nombre": x.encuentro.seccion.materia.nombre,
                        "pensum": x.encuentro.seccion.materia.pensum.nombre,
                    },
                },
                "aula": {
                    "pk": x.encuentro.aula.pk,
                    "numero": x.encuentro.aula.numero,
                    "nombre": x.encuentro.aula.nombre,
                    "tipo": x.encuentro.aula.tipo_aula.modalidad,
                    "ubicacion": x.encuentro.aula.ubicacion.nombre,
                },
                "bloque": {
                    "pk": x.encuentro.bloque.pk,
                    "hora_inicio": str(x.encuentro.bloque.hora_inicio),
                    "esquema_bloque": {
                        "pk": x.encuentro.bloque.esquema_bloque.pk,
                        "duracion": str(x.encuentro.bloque.esquema_bloque.duracion),
                        # "tipo_encuentro": x.encuentro.bloque.esquema_bloque.tipo_encuentro,
                        "carrera": {
                            "pk": x.encuentro.bloque.esquema_bloque.carrera.pk,
                            "nombre": x.encuentro.bloque.esquema_bloque.carrera.nombre,
                        },
                    },
                },


            }
            for x in objetos
        ]
        datos = json.dumps(datos, indent=2)
        return HttpResponse(datos, content_type='application/json')



class BloquesAPIListView(View):

    def get(self, request, *args, **kwargs):
        # @TODO: validar que el usuario logueado tenga permiso a acceder a los datos
        filtros = {}
        if 'carrera' in request.GET:
            objetos = Bloque.objects.filter(esquema_bloque__carrera=request.GET['carrera']).all()
            datos = [
                {
                    "pk": x.pk,
                    "hora_inicio": str(x.hora_inicio),
                    "representacion": str(x),
                    "turno": x.turno.nombre,
                }
                for x in objetos
            ]
            datos = json.dumps(datos, indent=2)
            return HttpResponse(datos, content_type='application/json')
        return HttpResponseBadRequest()

class DiasAPIListView(View):

    def get(self, request, *args, **kwargs):
        # @TODO: validar que el usuario logueado tenga permiso a acceder a los datos
        filtros = {}
        if 'carrera' in request.GET:
            objetos = Dia.objects.filter(esquema_dia__carrera=request.GET['carrera']).all()
            datos = [
                {
                    "pk": x.pk,
                    "numero": x.dia,
                    "dia": str(x),
                }
                for x in objetos
            ]
            datos = json.dumps(datos, indent=2)
            return HttpResponse(datos, content_type='application/json')
        return HttpResponseBadRequest()