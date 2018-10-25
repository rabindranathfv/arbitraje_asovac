//Sidebar Toggle Script 
$("#menu-toggle").click(function(e) {
    e.preventDefault();
    $("#wrapper").toggleClass("toggled");
    $("#menu-toggle-icon").toggleClass("fa-angle-double-left");
    $("#menu-toggle-icon").toggleClass("fa-angle-double-right");
});

$(".submenu-toggle").click(function(e) {
    //e.preventDefault();
    $(this).find("i").toggleClass("fa-angle-down");
    $(this).find("i").toggleClass("fa-angle-right");
});



$(document).ready(function(){
    // To style only selects with the selectpicker class
    $('.selectpicker').selectpicker();
    
    $('[data-toggle="tooltip"]').tooltip();

    $( function(){
        $( ".dateinput" ).datepicker({ dateFormat: 'dd/mm/yy'});
    });
});



$('#myModal').on('shown.bs.modal', function () {
  $('#myInput').trigger('focus')
});

// Ajax para modales

// Manejo del token en solicitudes post
$(function(){
    //Obtenemos la información de csfrtoken que se almacena por cookies en el cliente
    var csrftoken = getCookie('csrftoken');

    //Agregamos en la configuración de la funcion $.ajax de Jquery lo siguiente:
    $.ajaxSetup({
                    beforeSend: function(xhr, settings) {
                        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                            // Send the token to same-origin, relative URLs only.
                            // Send the token only if the method warrants CSRF protection
                            // Using the CSRFToken value acquired earlier
                            xhr.setRequestHeader("X-CSRFToken", csrftoken);
                        }
                    }
    });

function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}

// usando jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


    function csrfSafeMethod(method) {
        // estos métodos no requieren CSRF
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
});



// Mostrar ventana modal con el contenido correspondiente
$(document).ready(function(){

    var ShowForm= function(){
        var btn= $(this);
        // alert('ShowForm');
        $.ajax({
            url: btn.attr('data-url'),
            type: 'get',
            dataType: 'json',
            beforeSend: function(){
              $('#modal-user, #modal-job, #modal-pay, #modal-observations' ).modal('show');  
            },
            success: function (data){
                // console.log(data.html_form);
                $('#modal-user .modal-content, #modal-job .modal-content, #modal-pay .modal-content, #modal-observations .modal-content').html(data.html_form);
            }
        });
    };
// Ocultar ventana modal y enviar formulario via ajax
    var SaveForm= function(){
        var form= $(this);
        // alert('SaveForm');
        $.ajax({
            url: form.attr('data-url'),
            data: form.serialize(),
            type: form.attr('method'),
            dataType: 'json',

            success: function(data){

                if(data.form_is_valid){
                    // console.log('data is saved')
                    $('#show_users tbody').html(data.user_list);
                    $('#modal-user').modal('hide');
                }else{
                    // console.log('data is invalid')
                    $('#modal-user .modal-content').html(data.html_form)
                }
            }
        });
        return false;
    };

// Se valida el acceso al evento segun el rol y su clave 
var ValidateAccess= function(){
    var form= $(this);
    // alert('ValidateAccess');
    $.ajax({
        url: form.attr('data-url'),
        data: form.serialize(),
        type: form.attr('method'),
        dataType: 'json',
        beforeSend: function(){
            $('#rol_validate').modal('show');  
          },
        success: function(data){

            if(data.form_is_valid){
                if (data.method == 'get') {
                    console.log('Caso valido, metodo get')
                    $('#rol_validate .modal-content').html(data.html_form)
                }else{
                    console.log('Caso valido, metodo post')
                    $('#rol_validate .modal-content').html(data.html_form)
                }
            }else{
                console.log('Caso no valido')
                $('#rol_validate .modal-content').html(data.html_form)
            }
        }
    });
    return false;
};
    // Para manejar la selección de rol y contraseña
    $('#rol').change(function(){
        alert("rol cambiado");
        console.log("El rol fue cambiado a "+rol);
    });

    // Para manejar la seleccion de areas y mostrar subareas conventana modal
    $('#area_select').change(function(){

        var area = $(this).val();
        $('#enviar').attr('disabled', true);
        $("#subarea_select option").each(function(){
                 $(this).css('display','block');
         });
        
        if(area != ""){
            $('#content_subarea').css("display", "block");
            
            $("#subarea_select option").each(function(){
            
               if( $(this).attr('data-area') != area){
                   if($(this).val() != "" ){
                    //$(this).val("0");
                    //$(this).remove();
                    $(this).css('display','none');
                    $(this).attr("selected",false); 
                   }
                  
                }else{
                    $(this).attr("selected",false);
                }
    
            });
    
        }else{
            $('#content_subarea').css("display", "none");
        }

        // Obtener subareas
        var route= $(this).attr('data-url');
        // Se reemplaza el valor por defeto de la ruta por el id del area
        route=route.replace("0",area);
        id=area;
        // console.log("La ruta es "+route+ " y el area es: "+ area);

       $.ajax({
           type: "post",
           url: route,
           data: id,
           dataType: "json",
           success: function (data) {
            //    console.log(data.html_select);
               $('#content_subarea .subareas-content').html(data.html_select);
               $('.selectpicker').selectpicker();
           }
       });

    
    });

     //Para habilitar boton de cambio de área y subarea 
     $('#subarea_select').change(function(){
        
        if($(this).val() != ""){
            $('#enviar').removeAttr("disabled");
        }else{
            $('#enviar').attr('disabled', true);
        }
    });

    // create
    $('.show-form').click(ShowForm);
    $('#modal-user').on('submit', '.create-form',SaveForm);

    // //update
    $('#show_users').on('click','.show-form-update',ShowForm);
    $('#modal-user').on('submit','.update-form',SaveForm);

    //delete
    $('#show_users').on('click','.show-form-delete',ShowForm);
    $('#modal-user').on('submit','.delete-form',SaveForm);

    // update rol
    $('#show_users').on('click','.show-form-rol',ShowForm);
    $('#modal-user').on('submit','.rol-form',SaveForm);


    // Delete Job
    $('#show-job').on('click','.show-form-delete',ShowForm);

    // Editar datos de pago
    $('.show-pays').on('click','.show-edit-pay',ShowForm);

    //Mostrar observaciones de la versión final del trabajo
    $('#show-job-final-version').on('click', '.show-job-observations', ShowForm)

    //Añadir observaciones a la versión final del trabajo
    $('#show-job-final-version').on('click', '.show-form-job-observations', ShowForm)

    
    //show areas 
    $('.show_areas').click(ShowForm);
    $('#modal-user').on('submit','.change_area',SaveForm);
   
    // validate ValidateAccess
    $('.show-form-access').click(ValidateAccess);
    $('#rol_validate').on('submit','.validate_access',ValidateAccess);

    // Delete Event
    $('#event-list').on('click','.show-form-delete',ShowForm);

    // Delete Location
    $('#location-list').on('click','.show-form-delete',ShowForm);

    // Delete Location
    $('#organizer-list').on('click','.show-form-delete',ShowForm);
});

