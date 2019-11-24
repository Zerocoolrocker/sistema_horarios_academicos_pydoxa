$('.crear-proyecto-button').click(function(e){
	e.preventDefault();
	$('#myModal').modal({show: true});
	return false;
});


$(document).on('submit', '.ajax-form',function(e){
    $.ajax({
        type: 'POST',
        url: $(this).attr('action'),
        data: {

        	
            title:$('#title').val(),
            description:$('#description').val(),





            csrfmiddlewaretoken:$(this).find('input[name=csrfmiddlewaretoken]').val(),
            action: 'post'
        },
        success:function(json){
            document.getElementById("post-form").reset();
            $(".posts").prepend('<div class="col-md-6">'+
                '<div class="row no-gutters border rounded overflow-hidden flex-md-row mb-4 shadow-sm h-md-250 position-relative">' +
                    '<div class="col p-4 d-flex flex-column position-static">' +
                        '<h3 class="mb-0">' + json.title + '</h3>' +
                        '<p class="mb-auto">' + json.description + '</p>' +
                    '</div>' +
                '</div>' +
            '</div>' 
            )
        },
        error : function(xhr,errmsg,err) {
        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
    }
    });
});