var dragSrcEl = null;
// var esquemas_dias = ['Lunes', 'Martes', 'Miercoles', 'Jueves', 'Viernes']
var esquemas_dias = [];
// var data_dias = [];
var bloques_horas = [];
var esquemas_bloques = [];
var pks_dias = [];
var data_proyecto = {};



function handleDragStart(e) {
  // Target (this) element is the source node.
  // this.style.opacity = '0.4';

  dragSrcEl = this;

  e.dataTransfer.effectAllowed = 'move';
  e.dataTransfer.setData('text/html', this.innerHTML);
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

// var cols = document.querySelectorAll('.dnd-encuentro');
// [].forEach.call(cols, function(col) {
//   col.addEventListener('dragstart', handleDragStart, false);
//   col.addEventListener('dragenter', handleDragEnter, false);
//   col.addEventListener('dragover', handleDragOver, false);
//   col.addEventListener('dragleave', handleDragLeave, false);
// });

function handleDrop(e) {
  // this/e.target is current target element.
  this.classList.remove('over');  // this / e.target is previous target element.


  if (e.stopPropagation) {
    e.stopPropagation(); // Stops some browsers from redirecting.
  }

  // Don't do anything if dropping the same column we're dragging.
  if (dragSrcEl != this) {
    // Set the source column's HTML to the HTML of the column we dropped on.
    dragSrcEl.innerHTML = this.innerHTML;
    this.innerHTML = e.dataTransfer.getData('text/html');
    var encuentro_data = data_proyecto[Number($(e.target).find('.dnd-encuentro').data('encuentro-dia-pk'))];
    $.post('/api/encuentros/update/', {
    	pk: encuentro_data.encuentro_dia_pk,
    	hora_inicio: esquemas_bloques[$(this).data('hora')],
    	dia: pks_dias[$(this).data('dia')],
    })
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



	elements = Array.prototype.slice.call(cols);
	elements2 = Array.prototype.slice.call(cols2);

	var elements = elements.concat(elements2);



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

// @TODO: hacer que se cargue el proyecto actual
function llenar_encuentros(){
	$.getJSON('/api/encuentros/?proyecto=' + proyecto, function(data){
		console.log('datos de encuentros recibida.')
		var indice_bloques_dias = 0;
		var indice_bloques_horas = 0;
		for (var i = 0; i < data.length; i++) {
			console.log('iteracion en for de datos de encuentros');
			var bloque_objetivo = null;
			indice_bloques_dias = esquemas_dias.indexOf(data[i].dia) + 2;
			indice_bloques_horas = esquemas_bloques.indexOf(data[i].bloque.hora_inicio) + 1;
			// console.log(esquemas_bloques);
			// console.log(esquemas_bloques.indexOf(data[i].bloque.hora_inicio), data[i].bloque.hora_inicio);
			var selector_bloque_objetivo = '.tabla-encuentros tr:nth-child(' + indice_bloques_horas + ') td:nth-child(' + indice_bloques_dias + ')'
			bloque_objetivo = $(selector_bloque_objetivo);
			console.log('bloque_objetivo', bloque_objetivo[0]);
			// if(!bloque_objetivo.length){
				
			callWhenReady(selector_bloque_objetivo, function(){
				var nuevo_encuentro  = $('<div>');
				nuevo_encuentro.attr('class', 'dnd-encuentro');
				nuevo_encuentro.attr('draggable', 'true');
				var titulo_encuentro  = $('<div>');
				titulo_encuentro.attr('class', 'titulo');
				titulo_encuentro.append($('<strong>').text(data[i].seccion.materia.nombre));
				nuevo_encuentro.append(titulo_encuentro);
				var texto = $('<p>');
				texto.text('Sección: ' + data[i].seccion.numero)
				texto.append($('<br>'))
				texto.append($('<strong>').append(data[i].seccion.docente))
				texto.append($('<br>'))
				texto.append('Cupo: ' + data[i].seccion.cupo)
				nuevo_encuentro.append(texto);
				nuevo_encuentro.attr('data-encuentro-dia-pk', data[i].encuentro_dia_pk);
				bloque_objetivo.append(nuevo_encuentro);
				data_proyecto[data[i].encuentro_dia_pk] = data[i];
			})




			// }
		};
		
	});
}

var tabla_recien_creada = false;
$(document).ready(function(){

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
				esquemas_bloques.push(data_bloques[i].hora_inicio);
			};
			thead.append('<th>');
			for (var i = 0; i < esquemas_dias.length; i++) {
				thead.append($('<th>').text(esquemas_dias[i]));
			};
			for (var i = 0; i < bloques_horas.length; i++) {
				var fila = $('<tr>');
				fila.append($('<td>').append($('<strong>').text(bloques_horas[i])));
				for (var j = 0; j < esquemas_dias.length; j++) {
					fila.append($('<td>').attr('data-hora', i).attr('data-dia', j));
				};
				tbody.append(fila);
			};
			console.log(tabla);
			tabla.append(thead);
			tabla.append(tbody);
			if(tabla_recien_creada){
				tabla_recien_creada = false;
				$('div.tabla-encuentros-wrapper').html(tabla).ready(llenar_encuentros()).ready(asignar_handlers_drag_and_drop());
			}
		});
	});

});

