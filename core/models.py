from django.db import models
from django.contrib.auth.models import User


class Area(models.Model):
	nombre = models.CharField(max_length=100)
	creado = models.DateField(auto_now_add=True)
	actualizado = models.DateField(auto_now=True)
	# usuario = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.nombre	

class Aula(models.Model):
	nombre = models.CharField(max_length=60, blank=True, null=True)
	# tipo_aula = models.ForeignKey('TipoAula', on_delete=models.CASCADE)
	ubicacion = models.ForeignKey('UbicacionAula', on_delete=models.CASCADE)
	# proyecto = models.ForeignKey('Proyecto', on_delete=models.CASCADE)
	creado = models.DateTimeField(auto_now_add=True)
	actualizado = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.nombre	

class Carrera(models.Model):
	nombre = models.CharField(max_length=60)
	codigo = models.CharField(max_length=5)
	area = models.ForeignKey('Area', on_delete=models.CASCADE)

	def __str__(self):
		return self.nombre	

class Pensum(models.Model):
	nombre = models.CharField(max_length=60)
	fecha = models.DateField()
	# regimen = models.CharField(max_length=10)
	carrera = models.ForeignKey('Carrera', on_delete=models.CASCADE)

	def __str__(self):
		return "%s - %s - %s" % (self.nombre, self.carrera, self.fecha)	

class Proyecto(models.Model):
	nombre = models.CharField(max_length=60)

	# usuario = models.ForeignKey(User, on_delete=models.CASCADE)

	# lapso_academico = models.CharField(max_length=10)
	fecha = models.DateField(auto_now_add=True)
	# fecha_memo = models.DateField(blank=True, null=True)
	observaciones = models.TextField(blank=True, null=True)
	creado = models.DateTimeField(auto_now_add=True)
	update = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.nombre


class Materia(models.Model):
	codigo = models.CharField(max_length=10)	
	nombre = models.CharField(max_length=60)	
	# avr = models.CharField(max_length=60)
	# @TODO: averiguar para que son estos campos
	# u_c = models.IntegerField()	
	# h_s = models.IntegerField()
	pensum = models.ForeignKey('Pensum', on_delete=models.CASCADE)	
	# @TODO: averiguar como se usa este campo
	# nivel = models.IntegerField()
	# departamento = models.ForeignKey('Departamento', on_delete=models.CASCADE)

	def __str__(self):
		return '%s(%s)' % (self.nombre, self.codigo)

class Horas(models.Model):
	hora = models.IntegerField()

	def __str__(self):
		return str(self.hora)	

class Minutos(models.Model):
	minutos = models.IntegerField(default=0)

	def __str__(self):
		return str(self.minutos)	

# class BloqueHorario(models.Model):
# 	hora_inicio = models.ForeignKey('Horas', related_name='hora_inicio_bloque', on_delete=models.CASCADE)
# 	minutos_inicio = models.ForeignKey('Minutos', related_name='minutos_inicio_bloque', on_delete=models.CASCADE)
# 	hora_fin = models.ForeignKey('Horas', on_delete=models.CASCADE)
# 	minutos_fin = models.ForeignKey('Minutos', on_delete=models.CASCADE)

# 	def __str__(self):
# 		return "%s:%s - %s:%s" % (self.hora_inicio, self.minutos_inicio, self.hora_fin, self.minutos_fin)

# class Horario(models.Model):
# 	creado = models.DateTimeField(auto_now_add=True)
# 	actualizado = models.DateTimeField(auto_now=True)

class Seccion(models.Model):
	aula = models.ForeignKey('Aula', on_delete=models.CASCADE)
	# @TODO: verificar el cambio de este campo
	numero = models.IntegerField()
	materia = models.ForeignKey('Materia', on_delete=models.CASCADE)
	proyecto = models.ForeignKey('Proyecto', on_delete=models.CASCADE)
	cupo = models.IntegerField()
	turno = models.ForeignKey('Turno', on_delete=models.CASCADE)
	# bloque = models.ForeignKey('BloqueHorario', on_delete=models.CASCADE)
	hora_inicio = models.ForeignKey('Horas', related_name='hora_inicio_bloque', on_delete=models.CASCADE)
	minutos_inicio = models.ForeignKey('Minutos', related_name='minutos_inicio_bloque', on_delete=models.CASCADE)
	hora_fin = models.ForeignKey('Horas', on_delete=models.CASCADE)
	minutos_fin = models.ForeignKey('Minutos', on_delete=models.CASCADE)	
	creado = models.DateTimeField(auto_now_add=True)
	actualizado = models.DateTimeField(auto_now=True)

	def __str__(self):
		return "Seccion %s - %s" % (self.numero, self.materia)	

class Docente(models.Model):
	cedula = models.IntegerField()
	nombres = models.CharField(max_length=60)
	apellidos = models.CharField(max_length=60)
	area = models.ForeignKey('Area', on_delete=models.CASCADE)
	# telf_movil = models.CharField(max_length=20, blank=True, null=True)
	# telf_casa = models.CharField(max_length=20, blank=True, null=True)
	email = models.CharField(max_length=100, blank=True, null=True)
	estado = models.ForeignKey('Estado', on_delete=models.CASCADE)
	municipio = models.ForeignKey('Estado', on_delete=models.CASCADE, related_name='estado_docente')
	direccion = models.TextField(blank=True, null=True)
	creado = models.DateTimeField(auto_now_add=True)
	actualizado = models.DateTimeField(auto_now=True)

	def __str__(self):
		return '%s %s CI: %s' % (self.nombres, self.apellidos, self.cedula)

class TelefonoDocente(models.Model):
	docente = models.ForeignKey('Docente', on_delete=models.CASCADE)
	telefono = models.CharField(max_length=15)
	tipo = models.CharField(max_length=2, choices=(
		('ce', 'Celular'),
		('ca', 'Casa'),
	), default='ce')
	
	def __str__(self):
		return self.telefono

class DocentesSecciones(models.Model):
	docente = models.ForeignKey('Docente', on_delete=models.CASCADE)
	seccion = models.ForeignKey('Seccion', on_delete=models.CASCADE)



# class Direccion(models.Model):
# 	nombre = models.CharField(max_length=30)
# 	area = models.ForeignKey('Area', on_delete=models.CASCADE)

# class Departamento(models.Model):
# 	nombre = models.CharField(max_length=30)
# 	direccion = models.ForeignKey('Direccion', on_delete=models.CASCADE)
# 	docente = models.ForeignKey('Docente', on_delete=models.CASCADE)
# 	avr = models.CharField(max_length=12)

# 	def __str__(self):
# 		return self.nombre

# class Materia(models.Model):
# 	codigo = models.CharField(max_length=10)	
# 	nombre = models.CharField(max_length=60)	
# 	avr = models.CharField(max_length=60)
# 	# @TODO: averiguar para que son estos campos
# 	u_c = models.IntegerField()	
# 	h_s = models.IntegerField()
# 	pensum = models.ForeignKey('Pensum', on_delete=models.CASCADE)	
# 	# @TODO: averiguar como se usa este campo
# 	nivel = models.IntegerField()
# 	departamento = models.ForeignKey('Departamento', on_delete=models.CASCADE)

# 	def __str__(self):
# 		return '%s(%s)' % (self.nombre, self.codigo)		

class Turno(models.Model):
	nombre = models.CharField(max_length=60)

	def __str__(self):
		return self.nombre	

# class Seccion(models.Model):
# 	aula = models.ForeignKey('Aula', on_delete=models.CASCADE)
# 	# @TODO: verificar el cambio de este campo
# 	numero = models.IntegerField()
# 	materia = models.ForeignKey('Materia', on_delete=models.CASCADE)
# 	proyecto = models.ForeignKey('Proyecto', on_delete=models.CASCADE)
# 	cupo = models.IntegerField()
# 	turno = models.ForeignKey('Turno', on_delete=models.CASCADE)
# 	# @TODO: consultar este cambio de haber agregado este campo aqui
# 	bloque = models.ForeignKey('Bloque', on_delete=models.CASCADE)
# 	creado = models.DateTimeField(auto_now_add=True)
# 	actualizado = models.DateTimeField(auto_now=True)

# 	def __str__(self):
# 		return "Seccion %s - %s" % (self.numero, self.materia)

# class TipoAula(models.Model):
# 	nombre = models.CharField(max_length=60)
# 	descripcion = models.TextField(blank=True, null=True)
# 	modalidad = models.IntegerField()

# 	def __str__(self):
# 		return self.nombre	

# class Encuentro(models.Model):
# 	# materia = models.ForeignKey('Materia', on_delete=models.CASCADE)
# 	cant_horas = models.IntegerField()
# 	tipo_aula = models.ForeignKey('TipoAula', on_delete=models.CASCADE)

# class EncuentrosSeccion(models.Model):
# 	seccion = models.ForeignKey('Seccion', on_delete=models.CASCADE)
# 	encuentro = models.ForeignKey('Encuentro', on_delete=models.CASCADE)

class Estado(models.Model):
	nombre = models.CharField(max_length=100)

	def __str__(self):
		return self.nombre	

class Municipio(models.Model):
	nombre = models.CharField(max_length=100)

	def __str__(self):
		return self.nombre	

# class Docente(models.Model):
# 	cedula = models.IntegerField()
# 	nombres = models.CharField(max_length=60)
# 	apellidos = models.CharField(max_length=60)
# 	area = models.ForeignKey('Area', on_delete=models.CASCADE)
# 	telf_movil = models.CharField(max_length=20, blank=True, null=True)
# 	telf_casa = models.CharField(max_length=20, blank=True, null=True)
# 	email = models.CharField(max_length=100, blank=True, null=True)
# 	estado = models.ForeignKey('Estado', on_delete=models.CASCADE)
# 	municipio = models.ForeignKey('Estado', on_delete=models.CASCADE, related_name='estado_docente')
# 	direccion = models.TextField(blank=True, null=True)
# 	creado = models.DateTimeField(auto_now_add=True)
# 	actualizado = models.DateTimeField(auto_now=True)

# 	def __str__(self):
# 		return '%s %s CI: %s' % (self.nombres, self.apellidos, self.cedula)

# class DocentesSecciones(models.Model):
# 	docente = models.ForeignKey('Docente', on_delete=models.CASCADE)
# 	seccion = models.ForeignKey('Seccion', on_delete=models.CASCADE)

# class Asistencia(models.Model):
# 	proyecto = models.ForeignKey('Proyecto', on_delete=models.CASCADE)
# 	encuentros_seccion = models.ForeignKey('EncuentrosSeccion', on_delete=models.CASCADE)
# 	docente = models.ForeignKey('Docente', on_delete=models.CASCADE)
# 	asistio = models.BooleanField(default=False)
# 	fecha = models.DateField()

class UbicacionAula(models.Model):
	nombre = models.CharField(max_length=60)
	descripcion = models.TextField(blank=True, null=True)

	def __str__(self):
		return self.nombre	

# # @TODO: entender el uso de esta tabla
# class EsquemaDia(models.Model):
# 	nombre = models.CharField(max_length=60)

# # @TODO: entender el uso de esta tabla
# class EsquemaHora(models.Model):
# 	nombre = models.CharField(max_length=60)
# 	sep_num = models.IntegerField(null=True)

# class Aula(models.Model):
# 	nombre = models.CharField(max_length=60)
# 	tipo_aula = models.ForeignKey('TipoAula', on_delete=models.CASCADE)
# 	ubicacion = models.ForeignKey('UbicacionAula', on_delete=models.CASCADE)
# 	proyecto = models.ForeignKey('Proyecto', on_delete=models.CASCADE)
# 	esquema_dia = models.ForeignKey('EsquemaDia', on_delete=models.CASCADE)
# 	esquema_hora = models.ForeignKey('EsquemaHora', on_delete=models.CASCADE)
# 	creado = models.DateTimeField(auto_now_add=True)
# 	actualizado = models.DateTimeField(auto_now=True)

# 	def __str__(self):
# 		return '%s - %s - %s' % (self.nombre, self.tipo_aula, self.ubicacion)

# # @TODO: entender el uso de esta tabla
# class Dia(models.Model):
# 	numero = models.IntegerField(null=True)
# 	nombre = models.CharField(max_length=12)
# 	esquema_dia = models.ForeignKey('EsquemaDia', on_delete=models.CASCADE)

# class Hora(models.Model):
# 	# @TODO: entender el uso de este campo
# 	numero = models.IntegerField(null=True)
# 	inicio = models.TimeField(null=True)
# 	fin = models.TimeField(null=True)
# 	# @TODO: entender el uso de este campo
# 	esquema_hora = models.ForeignKey('EsquemaHora', on_delete=models.CASCADE)

# 	def __str__(self):
# 		return '%s - %s' % (self.inicio, self.fin)

# class HorasTurnos(models.Model):
# 	hora = models.ForeignKey('Hora', on_delete=models.CASCADE)
# 	turno = models.ForeignKey('Turno', on_delete=models.CASCADE)


# # @TODO: esta tabla y la de hora quizas sean redundantes
# class Bloque(models.Model):
# 	# aula = models.ForeignKey('Aula', on_delete=models.CASCADE)
# 	# @TODO: entender el uso de este campo
# 	dia = models.ForeignKey('Dia', on_delete=models.CASCADE)
# 	hora = models.ForeignKey('Hora', on_delete=models.CASCADE)
# 	activo = models.BooleanField(default=True)
# 	# encuentros_seccion = models.ForeignKey('EncuentrosSeccion', on_delete=models.CASCADE)
# 	creado = models.DateTimeField(auto_now_add=True)
# 	actualizado = models.DateTimeField(auto_now=True)

# 	def __str__(self):
# 		return '%s - %s' % (self.hora.inicio, self.hora.fin)

# class Ficha(models.Model):
# 	docente = models.ForeignKey('Docente', on_delete=models.CASCADE)
# 	ingreso = models.TimeField()
# 	contrato = models.CharField(max_length=50)
# 	categoria = models.CharField(max_length=50)
# 	dedicacion = models.CharField(max_length=50)
# 	observacion = models.TextField()
# 	estatus = models.BooleanField(default=True)
# 	creado = models.DateTimeField(auto_now_add=True)
# 	actualizado = models.DateTimeField(auto_now=True)





# --------------




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