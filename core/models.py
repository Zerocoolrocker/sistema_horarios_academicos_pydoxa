from django.db import models
from django.contrib.auth.models import User


class Area(models.Model):
	nombre = models.CharField(max_length=100)
	created = models.DateField(auto_now_add=True)
	updated = models.DateField(auto_now=True)
	usuario = models.ForeignKey(User, on_delete=models.CASCADE)

class Carrera(models.Model):
	nombre = models.CharField(max_length=60)
	codigo = models.CharField(max_length=5)
	area = models.ForeignKey('Area', on_delete=models.CASCADE)

class Pensum(models.Model):
	nombre = models.CharField(max_length=60)
	fecha = models.DateField()
	regimen = models.CharField(max_length=10)
	carrera = models.ForeignKey('Carrera', on_delete=models.CASCADE)

class Proyecto(models.Model):
	nombre = models.CharField(max_length=60)
	pensum = models.ForeignKey('Pensum', on_delete=models.CASCADE)
	lapso_academico = models.CharField(max_length=10)
	fecha = models.DateField()
	fecha_memo = models.DateField()
	observaciones = models.TextField(blank=True, null=True)
	created = models.DateTimeField(auto_now_add=True)
	update = models.DateTimeField(auto_now=True)

	def __str__(self):
		return "%s - %s" % (self.nombre, self.lapso_academico)

class Direccion(models.Model):
	nombre = models.CharField(max_length=30)
	area = models.ForeignKey('Area', on_delete=models.CASCADE)

class Departamento(models.Model):
	nombre = models.CharField(max_length=30)
	direccion = models.ForeignKey('Direccion', on_delete=models.CASCADE)
	docente = models.ForeignKey('Docente', on_delete=models.CASCADE)
	avr = models.CharField(max_length=12)

class Materia(models.Model):
	codigo = models.CharField(max_length=10)	
	nombre = models.CharField(max_length=60)	
	avr = models.CharField(max_length=60)
	# @TODO: averiguar para que son estos campos
	u_c = models.IntegerField()	
	h_s = models.IntegerField()
	pensum = models.ForeignKey('Pensum', on_delete=models.CASCADE)	
	# @TODO: averiguar como se usa este campo
	nivel = models.IntegerField()
	departamento = models.ForeignKey('Departamento', on_delete=models.CASCADE)	

class Turno(models.Model):
	nombre = models.CharField(max_length=60)

class Seccion(models.Model):
	nombre = models.CharField(max_length=6)
	materia = models.ForeignKey('Materia', on_delete=models.CASCADE)
	proyecto = models.ForeignKey('Proyecto', on_delete=models.CASCADE)
	cupo = models.IntegerField()
	# @TODO: creo que este campo deberia cambiarse para que especifique la hora de entrada y de salida
	turno = models.ForeignKey('Turno', on_delete=models.CASCADE)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

class TipoAula(models.Model):
	nombre = models.CharField(max_length=60)
	descripcion = models.TextField(blank=True, null=True)
	modalidad = models.IntegerField()

class Encuentro(models.Model):
	materia = models.ForeignKey('Materia', on_delete=models.CASCADE)
	cant_horas = models.IntegerField()
	tipo_aula = models.ForeignKey('TipoAula', on_delete=models.CASCADE)

class EncuentrosSeccion(models.Model):
	seccion = models.ForeignKey('Seccion', on_delete=models.CASCADE)
	encuentro = models.ForeignKey('Encuentro', on_delete=models.CASCADE)

class Estado(models.Model):
	nombre = models.CharField(max_length=100)

class Municipio(models.Model):
	nombre = models.CharField(max_length=100)

class Docente(models.Model):
	cedula = models.IntegerField()
	nombres = models.CharField(max_length=60)
	apellidos = models.CharField(max_length=60)
	area = models.ForeignKey('Area', on_delete=models.CASCADE)
	telf_movil = models.CharField(max_length=20, blank=True, null=True)
	telf_casa = models.CharField(max_length=20, blank=True, null=True)
	email = models.CharField(max_length=100, blank=True, null=True)
	estado = models.ForeignKey('Estado', on_delete=models.CASCADE)
	municipio = models.ForeignKey('Estado', on_delete=models.CASCADE, related_name='estado_docente')
	direccion = models.TextField(blank=True, null=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

class DocentesSecciones(models.Model):
	docente = models.ForeignKey('Docente', on_delete=models.CASCADE)
	seccion = models.ForeignKey('Seccion', on_delete=models.CASCADE)

class Asistencia(models.Model):
	proyecto = models.ForeignKey('Proyecto', on_delete=models.CASCADE)
	encuentros_seccion = models.ForeignKey('EncuentrosSeccion', on_delete=models.CASCADE)
	docente = models.ForeignKey('Docente', on_delete=models.CASCADE)
	asistio = models.BooleanField(default=False)
	fecha = models.DateField()

class UbicacionAula(models.Model):
	nombre = models.CharField(max_length=60)
	descripcion = models.TextField()

# @TODO: entender el uso de esta tabla
class EsquemaDia(models.Model):
	nombre = models.CharField(max_length=60)

# @TODO: entender el uso de esta tabla
class EsquemaHora(models.Model):
	nombre = models.CharField(max_length=60)
	sep_num = models.IntegerField(null=True)

class Aula(models.Model):
	nombre = models.CharField(max_length=60)
	tipo_aula = models.ForeignKey('TipoAula', on_delete=models.CASCADE)
	ubicacion = models.ForeignKey('UbicacionAula', on_delete=models.CASCADE)
	proyecto = models.ForeignKey('Proyecto', on_delete=models.CASCADE)
	esquema_dia = models.ForeignKey('EsquemaDia', on_delete=models.CASCADE)
	esquema_hora = models.ForeignKey('EsquemaHora', on_delete=models.CASCADE)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)


# @TODO: entender el uso de esta tabla
class Dia(models.Model):
	numero = models.IntegerField(null=True)
	nombre = models.IntegerField()
	esquema_dia = models.ForeignKey('EsquemaDia', on_delete=models.CASCADE)

class Hora(models.Model):
	numero = models.IntegerField(null=True)
	inicio = models.TimeField(null=True)
	fin = models.TimeField(null=True)
	esquema_hora = models.ForeignKey('EsquemaHora', on_delete=models.CASCADE)

class HorasTurnos(models.Model):
	hora = models.ForeignKey('Hora', on_delete=models.CASCADE)
	turno = models.ForeignKey('Turno', on_delete=models.CASCADE)

class Bloque(models.Model):
	aula = models.ForeignKey('Aula', on_delete=models.CASCADE)
	dia = models.ForeignKey('Dia', on_delete=models.CASCADE)
	hora = models.ForeignKey('Hora', on_delete=models.CASCADE)
	activo = models.BooleanField(default=True)
	encuentros_seccion = models.ForeignKey('EncuentrosSeccion', on_delete=models.CASCADE)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

class Ficha(models.Model):
	docente = models.ForeignKey('Docente', on_delete=models.CASCADE)
	ingreso = models.TimeField()
	contrato = models.CharField(max_length=50)
	categoria = models.CharField(max_length=50)
	dedicacion = models.CharField(max_length=50)
	observacion = models.TextField()
	estatus = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

# @TODO: entener el uso de esta tabla

# CREATE TABLE `v_bloques_group` (
# `EncuentrosSeccion_id_exist` int(11)
# ,`Aula_id` int(11)
# ,`Aula_nombre` varchar(60)
# ,`Dia_numero` tinyint(4)
# ,`Dia_nombre` varchar(12)
# ,`Hora_numero_inicio` tinyint(4)
# ,`Hora_inicio` time
# ,`Hora_numero_fin` tinyint(4)
# ,`Hora_fin` time
# );

# @TODO: entener el uso de esta tabla

# CREATE TABLE `v_encuentros_seccions` (
# `Carrera_id` int(11)
# ,`Carrera_nombre` varchar(60)
# ,`Carrera_codigo` varchar(5)
# ,`Area_id` int(11)
# ,`Proyecto_id` int(11)
# ,`Seccion_id` int(11)
# ,`Seccion_nombre` varchar(6)
# ,`Seccion_cupo` int(3)
# ,`Materia_id` int(11)
# ,`Materia_nombre` varchar(60)
# ,`Materia_avr` varchar(12)
# ,`Materia_codigo` varchar(10)
# ,`Materia_nivel` tinyint(2)
# ,`Pensum_id` int(11)
# ,`Direccion_id` int(11)
# ,`Direccion_nombre` varchar(30)
# ,`Departamento_id` int(11)
# ,`Departamento_nombre` varchar(30)
# ,`Turno_id` int(11)
# ,`Turno_nombre` varchar(60)
# ,`EncuentrosSeccion_id` int(11)
# ,`Encuentro_cant_horas` tinyint(4)
# ,`Encuentro_tipo_aula_id` int(11)
# ,`TipoAula_nombre` varchar(60)
# ,`Encuentro_modalidad` int(11)
# );


# @TODO: entener el uso de esta tabla

# CREATE TABLE `v_resumen` (
# `Carrera_id` int(11)
# ,`Carrera_nombre` varchar(60)
# ,`Carrera_codigo` varchar(5)
# ,`Area_id` int(11)
# ,`Proyecto_id` int(11)
# ,`Seccion_id` int(11)
# ,`Seccion_nombre` varchar(6)
# ,`Seccion_cupo` int(3)
# ,`Materia_id` int(11)
# ,`Materia_nombre` varchar(60)
# ,`Materia_avr` varchar(12)
# ,`Materia_codigo` varchar(10)
# ,`Materia_nivel` tinyint(2)
# ,`Pensum_id` int(11)
# ,`Direccion_id` int(11)
# ,`Direccion_nombre` varchar(30)
# ,`Departamento_id` int(11)
# ,`Departamento_nombre` varchar(30)
# ,`Turno_id` int(11)
# ,`Turno_nombre` varchar(60)
# ,`EncuentrosSeccion_id` int(11)
# ,`Encuentro_cant_horas` tinyint(4)
# ,`Encuentro_tipo_aula_id` int(11)
# ,`TipoAula_nombre` varchar(60)
# ,`Encuentro_modalidad` int(11)
# ,`EncuentrosSeccion_id_exist` int(11)
# ,`Aula_id` int(11)
# ,`Aula_nombre` varchar(60)
# ,`Dia_numero` tinyint(4)
# ,`Dia_nombre` varchar(12)
# ,`Hora_numero_inicio` tinyint(4)
# ,`Hora_inicio` time
# ,`Hora_numero_fin` tinyint(4)
# ,`Hora_fin` time
# );