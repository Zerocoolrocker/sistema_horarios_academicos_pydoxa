var drag_source_element = null;
var esquemas_dias = [];
var bloques_horas = [];
var turnos_bloques_horas = [];
var esquemas_bloques = [];
var pks_dias = [];
var data_encuentros = {};
var data_aulas_encuentros = {};


function handleDragStart(e) {
  // Target (this) element is the source node.
  // this.style.opacity = '0.4';
  drag_source_element = this;
  if($(this).attr('class') && $(this).attr('class').indexOf('dnd-encuentro') != -1){
  	drag_source_element_real = this;
  }
  console.log('drag_source_element', drag_source_element);
  e.dataTransfer.effectAllowed = 'move';
  e.dataTransfer.setData('text/html', this.innerHTML);
  // debugger;
}	

function handleDragOver(e) {
  if (e.preventDefault) {
    e.preventDefault(); // Necessary. Allows us to drop.
  }

  e.dataTransfer.dropEffect = 'move';  // See the section on the DataTransfer object.

  return false;
}

function handleDragEnter(e) {
  // this / e.target is the current hover target.
  this.classList.add('over');
}

function handleDragLeave(e) {
  this.classList.remove('over');  // this / e.target is previous target element.
}


function handleDrop(e) {
  // this/e.target is current target element.
  this.classList.remove('over');  // this / e.target is previous target element.


  if (e.stopPropagation) {
    e.stopPropagation(); // Stops some browsers from redirecting.
  }

  // Don't do anything if dropping the same column we're dragging.
  if (drag_source_element_real != this) {

  	// @TODO: validar que no haya encuentro en el bloque en el que se solto el encuentro
  	// (mostrar advertencia o no permitir, dependiendo de configuracion)
    
    // Set the source column's HTML to the HTML of the column we dropped on.
    drag_source_element.innerHTML = this.innerHTML;
    this.innerHTML = e.dataTransfer.getData('text/html');
    var encuentro_data = data_encuentros[Number($(drag_source_element_real).data('encuentro-dia-pk'))];
  	console.log('drop function drag_source_element', drag_source_element);
    $.post('/api/encuentros/update/', {
    	pk: encuentro_data.encuentro_dia_pk,
    	hora_inicio: esquemas_bloques[$(this).data('hora')],
    	dia: pks_dias[$(this).data('dia')],
    	aula: aula_pk,
    });
    encuentro_data.bloque.hora_inicio = esquemas_bloques[$(this).data('hora')];
    encuentro_data.dia = esquemas_dias[$(this).data('dia')];
    encuentro_data.dia_pk = pks_dias[$(this).data('dia')];
  	var jquery_dse = $(drag_source_element_real);
  	if(jquery_dse.attr('class') && jquery_dse.attr('class').indexOf('resultado-busqueda') !=-1 && jquery_dse.data('aula') == aula){
		console.log('se limpia la tabla');
		limpiar_encuentros_tabla(function(){
			if(Boolean(data_aulas_encuentros[aula])){
				llenar_encuentros(aula);
			}
		})
  	}
  	if($(drag_source_element).attr('rowspan') > 1 || $(drag_source_element).attr('id') == 'resultados_busqueda'){
	  	if($(drag_source_element).attr('id') == 'resultados_busqueda'){
	  		$(this).attr('rowspan', encuentro_data.numero_bloques);
	  		var tmp_fila = $(this).parent().next('tr');
			for (var cont = 1; cont < encuentro_data.numero_bloques; cont++){
	  			// @TODO: validar que no haya encuentro en el bloque que se va a eliminar
		  		tmp_fila.find('td:nth-child(' + ($(this).data('dia') + 2) + ')').remove();
	  			tmp_fila = $(tmp_fila).next('tr');
			};

	  	} else {
	  		$(drag_source_element).attr('rowspan', 1);
	  		var hora_bloque_anterior = $(drag_source_element).data('hora');
	  		var dia_bloque_anterior = $(drag_source_element).data('hora');
	  		var tmp_fila = $(drag_source_element).parent().next('tr');
			for (var cont = 1; cont < encuentro_data.numero_bloques; cont++){
		  		// @TODO: validar que quepa dependiendo de la cantidad de bloques que ocupe el encuentro
	  			hora_bloque_anterior += 1
	  			tmp_fila.find('td:nth-child(' + ($(drag_source_element).data('dia') + 1) + ')').after($('<td>').attr('data-hora', hora_bloque_anterior).attr('data-dia', dia_bloque_anterior));
	  			tmp_fila = $(tmp_fila).next('tr');
			}

	  		$(this).attr('rowspan', encuentro_data.numero_bloques);
	  		var tmp_fila = $(this).parent().next('tr');
			for (var cont = 1; cont < encuentro_data.numero_bloques; cont++){
	  			// @TODO: validar que no haya encuentro en el bloque que se va a eliminar
		  		tmp_fila.find('td:nth-child(' + ($(this).data('dia') + 2) + ')').remove();
	  			tmp_fila = $(tmp_fila).next('tr');
			};  		
	  	}
	asignar_handlers_drag_and_drop();
	}
  }
  return false;
}

function handleDragEnd(e) {
  // this/e.target is the source node.
  // var cols = [e.target];
  // e.target.classList.remove('over');

  // [].forEach.call(cols, function (col) {
  //   col.classList.remove('over');
  // 	// col.style.opacity = '1';
  // });
}

function isEmpty(obj) {
    for(var key in obj) {
        if(obj.hasOwnProperty(key))
            return false;
    }
    return true;
}	


function asignar_handlers_drag_and_drop(){
	var cols = document.querySelectorAll('.dnd-encuentro');
	var cols2 = document.querySelectorAll('.tabla-encuentros td');
	var cols3 = document.querySelectorAll('#resultados_busqueda');

	var elements = Array.prototype.slice.call(cols);
	var elements2 = Array.prototype.slice.call(cols2);
	var elements3 = Array.prototype.slice.call(cols3);

	elements = elements.concat(elements2);
	elements = elements.concat(elements3);

	[].forEach.call(elements, function(col) {
	  col.addEventListener('dragstart', handleDragStart, false);
	  col.addEventListener('dragenter', handleDragEnter, false)
	  col.addEventListener('dragover', handleDragOver, false);
	  col.addEventListener('dragleave', handleDragLeave, false);
	  col.addEventListener('drop', handleDrop, false);
	  col.addEventListener('dragend', handleDragEnd, false);
	});

}

function callWhenReady(selector, callback) {
    var self = this;
    if ($(selector).closest('body').length) {
        callback();
    } else {
        setTimeout(function () {
            self.callWhenReady(selector, callback);
        }, 1);
    }
}	

function obtener_datos_encuentros(callback){
	$.getJSON('/api/encuentros/?proyecto=' + proyecto, function(data){
		for (var i = 0; i < data.length; i++) {
			data_encuentros[data[i].encuentro_dia_pk] = data[i];
			data_aulas_encuentros[data[i].aula.nombre] = (data_aulas_encuentros[data[i].aula.nombre] || []).concat(data[i]);
			data_aulas_encuentros['aulas_en_orden'] = (data_aulas_encuentros['aulas_en_orden'] || []).concat(data[i]);

			data_aulas_encuentros['aulas_en_orden'].sort(
				function(a, b) {
				  // Use toUpperCase() to ignore character casing
				  var ele1 = a.aula.numero.toUpperCase();
				  var ele2 = b.aula.numero.toUpperCase();
				  var comparison = 0;
				  if (ele1 > ele2) {
				    comparison = 1;
				  } else if (ele1 < ele2) {
				    comparison = -1;
				  }
				  return comparison;
				}
			);
		};
		callback();
	});
}

function limpiar_encuentros_tabla(callback){
	// $('.tabla-encuentros .dnd-encuentro').remove().ready(callback);
	renderizar_tabla();
}

function llenar_encuentros(aul){
	console.log('datos de encuentros recibida.')
	var indice_bloques_dias = 0;
	var indice_bloques_horas = 0;
	if(Boolean(data_aulas_encuentros[aul])){
		for (var i = 0; i < data_aulas_encuentros[aul].length; i++) {
			var bloque_objetivo = null;
			indice_bloques_dias = esquemas_dias.indexOf(data_aulas_encuentros[aul][i].dia) + 2;
			indice_bloques_horas = esquemas_bloques.indexOf(data_aulas_encuentros[aul][i].bloque.hora_inicio) + 1;
			var selector_bloque_objetivo = '.tabla-encuentros tr:nth-child(' + indice_bloques_horas + ') td:nth-child(' + indice_bloques_dias + ')'
			bloque_objetivo = $(selector_bloque_objetivo);
				
			callWhenReady(selector_bloque_objetivo, function(){
				var nuevo_encuentro = $('<div>');
				nuevo_encuentro.attr('class', 'dnd-encuentro');
				nuevo_encuentro.attr('draggable', 'true');
				var titulo_encuentro  = $('<div>');
				titulo_encuentro.attr('class', 'titulo');
				titulo_encuentro.append($('<strong>').text(data_aulas_encuentros[aul][i].seccion.materia.nombre));
				nuevo_encuentro.append(titulo_encuentro);
				var texto = $('<p>');
				texto.text('Sección: ' + data_aulas_encuentros[aul][i].seccion.numero)
				texto.append($('<br>'))
				texto.append($('<strong>').append(data_aulas_encuentros[aul][i].seccion.docente))
				texto.append($('<br>'))
				texto.append('Cupo: ' + data_aulas_encuentros[aul][i].seccion.cupo)
				nuevo_encuentro.append(texto);
				nuevo_encuentro.attr('data-encuentro-dia-pk', data_aulas_encuentros[aul][i].encuentro_dia_pk);
				bloque_objetivo.append(nuevo_encuentro);

				// @TODO: Hacer validaciones de numero de bloques de encuentro aqui
				var numero_bloques = data_aulas_encuentros[aul][i].numero_bloques;
				bloque_objetivo.attr('rowspan', numero_bloques);
				for (var ind_blo = indice_bloques_horas + 1; ind_blo < esquemas_bloques.length && ind_blo < indice_bloques_horas + numero_bloques; ind_blo++) {
					var selector_bloque_eliminar = '.tabla-encuentros tr:nth-child(' + ind_blo + ') td:nth-child(' + indice_bloques_dias + ')'
					$(selector_bloque_eliminar).remove();
				};
			})
		}
	}
		
}

function renderizar_tabla(){
	var tabla = $('.tabla-encuentros');
	tabla = $('<div>').attr('class', 'box-body').append('<table>').attr('class', 'table table-bordered tabla-encuentros').append('<tbody>');
	tabla.append($('<div>').attr('class', 'box-footer'));
	tabla_recien_creada = true
	var thead = $('<thead>');
	var tbody = $('<tbody>');
	thead.append('<th>');
	for (var i = 0; i < esquemas_dias.length; i++) {
		thead.append($('<th>').text(esquemas_dias[i]));
	};
	var tmp_turno = turnos_bloques_horas[0];
	for (var i = 0; i < bloques_horas.length; i++) {
		var fila = $('<tr>');
		fila.append($('<td>').append($('<strong>').text(bloques_horas[i])));
		for (var j = 0; j < esquemas_dias.length; j++) {
			fila.append($('<td>').attr('data-hora', i).attr('data-dia', j));
		};
		if(tmp_turno != turnos_bloques_horas[i]){
			fila.attr('class', 'separador-turno');
		}
		tmp_turno = turnos_bloques_horas[i];
		tbody.append(fila);
	};
	console.log(tabla);
	tabla.append(thead);
	tabla.append(tbody);
	$('div.tabla-encuentros-wrapper').html(tabla).ready(
		llenar_encuentros(aula)
	).ready(
		asignar_handlers_drag_and_drop()
	)
}

$(document).ready(function(){
	tabla_recien_creada = false;
	obtener_datos_encuentros(function(){
		var tabla = $('.tabla-encuentros');
		if(!tabla.length){
			tabla = $('<div>').attr('class', 'box-body').append('<table>').attr('class', 'table table-bordered tabla-encuentros').append('<tbody>');
			tabla.append($('<div>').attr('class', 'box-footer'));
			tabla_recien_creada = true
		}
		var thead = $('<thead>');
		var tbody = $('<tbody>');
		$.getJSON('/api/dias/?carrera=' + carrera, function(data){
			for (var i = 0; i < data.length; i++) {
				esquemas_dias.push(data[i].dia);
				pks_dias.push(data[i].numero);
			};
			$.getJSON('/api/bloques/?carrera=' + carrera, function(data_bloques){
				for (var i = 0; i < data_bloques.length; i++) {
					bloques_horas.push(data_bloques[i].representacion);
					turnos_bloques_horas.push(data_bloques[i].turno);
					esquemas_bloques.push(data_bloques[i].hora_inicio);
				};
				thead.append('<th>');
				for (var i = 0; i < esquemas_dias.length; i++) {
					thead.append($('<th>').text(esquemas_dias[i]));
				};
				var tmp_turno = turnos_bloques_horas[0];
				for (var i = 0; i < bloques_horas.length; i++) {
					var fila = $('<tr>');
					fila.append($('<td>').append($('<strong>').text(bloques_horas[i])));
					for (var j = 0; j < esquemas_dias.length; j++) {
						fila.append($('<td>').attr('data-hora', i).attr('data-dia', j));
					};
					if(tmp_turno != turnos_bloques_horas[i]){
						fila.attr('class', 'separador-turno');
					}
					tmp_turno = turnos_bloques_horas[i];
					tbody.append(fila);
				};
				console.log(tabla);
				tabla.append(thead);
				tabla.append(tbody);
				if(tabla_recien_creada){
					tabla_recien_creada = false;
					$('div.tabla-encuentros-wrapper').html(tabla).ready(
						llenar_encuentros(aula)
					).ready(
						asignar_handlers_drag_and_drop()
					);
				}
			});
		});
		if(data_aulas_encuentros['aulas_en_orden'].length){
			$('.aula-actual').text(aula);
			llenar_encuentros(aula);
		}
	});

});

// ######## Eventos ##############


$('.aula-button').click(function(){
	aula = $(this).text();
	aula_pk = $(this).data('pk');
	$('.aula-actual').text(aula);
	limpiar_encuentros_tabla();
	// limpiar_encuentros_tabla(function(){
	// 	if(Boolean(data_aulas_encuentros[aula])){
	// 		llenar_encuentros(aula);
	// 	}
	// })
});

$('#busqueda_encuentro').click(function(){
	var materia = $('#busqueda_materia').val().toLowerCase();
	var seccion = $('#busqueda_seccion').val();
	if(materia && seccion){
		for (var i = data_aulas_encuentros['aulas_en_orden'].length - 1; i >= 0; i--) {
			if(data_aulas_encuentros['aulas_en_orden'][i].seccion.materia.nombre.toLowerCase().indexOf(materia) != -1){
				if(data_aulas_encuentros['aulas_en_orden'][i].seccion.numero == Number(seccion)){
					
					var nuevo_encuentro  = $('<div>');
					nuevo_encuentro.attr('class', 'dnd-encuentro resultado-busqueda');
					nuevo_encuentro.attr('draggable', 'true');
					var titulo_encuentro  = $('<div>');
					titulo_encuentro.attr('class', 'titulo');
					titulo_encuentro.append($('<strong>').text(data_aulas_encuentros['aulas_en_orden'][i].seccion.materia.nombre));
					nuevo_encuentro.append(titulo_encuentro);
					var texto = $('<p>');
					texto.text('Sección: ' + data_aulas_encuentros['aulas_en_orden'][i].seccion.numero)
					texto.append($('<br>'))
					texto.append($('<strong>').append(data_aulas_encuentros['aulas_en_orden'][i].seccion.docente))
					texto.append($('<br>'))
					texto.append('Cupo: ' + data_aulas_encuentros['aulas_en_orden'][i].seccion.cupo)
					nuevo_encuentro.append(texto);
					nuevo_encuentro.attr('data-aula', data_aulas_encuentros['aulas_en_orden'][i].aula.nombre);
					// nuevo_encuentro.attr('data-encuentro-dia-pk', data[i].encuentro_dia_pk)
					nuevo_encuentro.attr('data-encuentro-dia-pk', data_aulas_encuentros['aulas_en_orden'][i].encuentro_dia_pk);
					nuevo_encuentro.attr('rowspan', data_aulas_encuentros['aulas_en_orden'][i].numero_bloques);
					console.log('se agrega res busqueda');

					$('#resultados_busqueda').append(nuevo_encuentro);
					asignar_handlers_drag_and_drop();
				}
			}
		};
	}
});




// ###############################


