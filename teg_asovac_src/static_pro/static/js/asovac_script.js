
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

    (function ($) {

        $('#filter').keyup(function () {

            var rex = new RegExp($(this).val(), 'i');
            $('.searchable tr').hide();
            $('.searchable tr').filter(function () {
                return rex.test($(this).text());
            }).show();

        })

    }(jQuery));

    var ShowForm= function(){
        var btn= $(this);
        // alert('ShowForm');
        $.ajax({
            url: btn.attr('data-url'),
            type: 'get',
            dataType: 'json',
            beforeSend: function(){
              $('#modal-user').modal('show');  
            },
            success: function (data){
                // console.log(data.html_form);
                $('#modal-user .modal-content').html(data.html_form);
            }
        });
    };
// Ocultar ventana modal y enviar formulario via ajax
    var SaveForm= function(){
        // console.log("SE envia el formulario");
        var form= $(this);
        // alert('SaveForm');
        $.ajax({
            url: form.attr('data-url'),
            data: form.serialize(),
            type: form.attr('method'),
            dataType: 'json',

            success: function(data){

                if(data.form_is_valid){
                    console.log('data is saved')
                    $('#show_users tbody').html(data.user_list);
                    $('#modal-user').modal('hide');
                }else{
                    console.log('data is invalid')
                    $('#modal-user .modal-content').html(data.html_form)
                }
            }
        });
        return false;
    };

// Mantener el formulario abierto
    var SaveFormAndStayInModal= function(){
        // console.log("SE envia el formulario");
        var form= $(this);
        // alert('SaveForm');
        $.ajax({
            url: form.attr('data-url'),
            data: form.serialize(),
            type: form.attr('method'),
            dataType: 'json',

            success: function(data){
                $('#modal-user .modal-content').html(data.html_form);
            }
        });
        return false;
    };
// Seguir en el formulario a menos que todo vaya bien
    var SaveFormAndRedirect= function(){
        // console.log("SE envia el formulario");
        var form= $(this);
        // alert('SaveForm');
        $.ajax({
            url: form.attr('data-url'),
            data: form.serialize(),
            type: form.attr('method'),
            dataType: 'json',

            success: function(data){
                if(data.form_is_valid){
                    window.location.replace(data.url);
                }else{
                    $('#modal-user .modal-content').html(data.html_form)
                }
            }
        });
        return false;
    };

//Para obtener la informacin del archivo enviado
var loadAreas= function(){
    console.log("Se envia el formulario");
    var form= $(this);

    var inputFile = document.getElementById("id_file");
    var file = inputFile.files[0];
    var formData = new FormData();
    
    formData.append('archivo', file);
    console.log(file);
    
    var data = new FormData();
    jQuery.each($('input[type=file]')[0].files, function(i, file) {
        data.append('file-'+i, file);
    });
    var other_data = $('loadAreasForm').serializeArray();
    $.each(other_data,function(key,input){
        data.append(input.name,input.value);
    });
   
    $.ajax({
        url: form.attr('data-url'),
        // data: form.serialize(),
        data: data,
        type: form.attr('method'),
        dataType: false,
        processData: false,

        success: function(data){

            if(data.form_is_valid){
                console.log('data is saved')
                $('#show_users tbody').html(data.user_list);
                $('#modal-user').modal('hide');
            }else{
                console.log('data is invalid')
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


// Para manejar las peticiones POST de añadir pago
var SaveAñadirPagoForm= function(){
        var form= $(this);
        // alert('SaveForm');
        $.ajax({
            url: form.attr('data-url'),
            data: form.serialize(),
            type: form.attr('method'),
            dataType: 'json',

            success: function(data){
                //$('#modal-user .modal-content').html(data.html_form)
                //Continuar desde aquí, al momento de eliminar las siguientes dos lineas, puedo hacer que cargue directamente las otras 2 vistas o puedo colocar una alerta entre cada formulario que llene el usuario
                //$('#modal-user').modal('hide');
                //
                //alert(data.message)
                if(data.form_is_valid)
                {    
                    $.ajax({
                        url: data.url,
                        type: 'get',
                        dataType: 'json',

                        beforeSend: function(){
                          $('#modal-user' ).modal('show');  
                        },
                        success: function (data){
                            // console.log(data.html_form);
                            $('#modal-user .modal-content').html(data.html_form);
                            
                        }
                    });
                }
                else
                {
                    $('#modal-user .modal-content').html(data.html_form);
                }
                //
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

    //bootstrap-tables edit 
    var bootstrapTableForm= function(){
        var form= $(this);
        $.ajax({
            url: form.attr('data-url'),
            data: form.serialize(),
            type: form.attr('method'),
            dataType: 'json',

            success: function(data){
                // console.log(data);
                if(data.status == 200 ){
                    // console.log('actualizacion exitosa')
                    // $('#bootstrapTableModal .modal-body').html("Se ha actualizado el registro de forma exitosa.");
                    // $('#modal-user').modal('hide');
                }else{
                    // console.log('error en la actualizacion')
                    // $('#bootstrapTableModal .modal-body').html(data.body)
                }
            }
        });
    
    };
    var saveFileFormAndRedirect = function () {
        var form = $(this);
        var formData = new FormData(form[0]);
        $.ajax({
          url: form.attr('data-url'),
          data: formData,
          type: form.attr('method'),
          dataType: 'json',
          async: true,
          cache: false,
          contentType: false,
          enctype: form.attr("enctype"),
          processData: false,
          success: function (data) {
            if(data.form_is_valid){
                window.location.replace(data.url);
            }else{
                $('#modal-user .modal-content').html(data.html_form)
            }
          }
        });
        return false;
      };

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

    // Añadir coautores al trabajo
    $('#show-job').on('click','.show-form-add-author',ShowForm);
    $('#modal-user').on('submit', '.add-autor-form',SaveFormAndRedirect);

    //Mostrar observaciones de la versión final del trabajo
    $('#show-job-final-version').on('click', '.show-job-observations', ShowForm)

    //Añadir observaciones a la versión final del trabajo
    $('#show-job-final-version').on('click', '.show-form-job-observations', ShowForm)

    // Añadir pago a un trabajo
    $('.añadir-pago-form').click(ShowForm);
    $('#modal-user').on('submit','.create-datos-pagador',SaveAñadirPagoForm);
    $('#modal-user').on('submit','.create-datos-factura',SaveAñadirPagoForm);
    $('#modal-user').on('submit','.create-datos-pago',saveFileFormAndRedirect);

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

    // Delete Organizer
    $('#organizer-list').on('click','.show-form-delete',ShowForm);

    // Organizer's details
    $('#organizer-list').on('click','.show-details',ShowForm);

    // Add organizer to event
    $('#event-list').on('click','.show-form-add-organizer-to-event',ShowForm);

     // Add organizer to event
    $('#event-list').on('click','.show-form-observations',ShowForm);

    // Add organizer to event
    $('#location-list').on('click','.show-form-observations',ShowForm);

    // Add organizer to event
    $('#organizer-list').on('click','.show-form-observations',ShowForm);

    // Para cargar areas
    $('.showAreasForm').click(ShowForm);
    // $('#modal-user').on('submit', '.loadAreasForm',loadAreas);
    $('.showSubAreasForm').click(ShowForm);
    // Modal para que los usuarios creen su instancia de autor
    $('#user-create-author').click(ShowForm);
    $('#modal-user').on('submit', '.author-create-author-form',SaveFormAndRedirect);
    // Modal para que los usuarios editen su instancia de autor
    $('#edit-author-profile').click(ShowForm);
    $('#modal-user').on('submit', '.edit-author-form',SaveFormAndStayInModal);

    // Modal para que los usuarios creen su instancia de autor en sistema
    $('.show-register-user-in-sistema-modal').click(ShowForm);

    // Modal para que los usuarios creen su instancia de autor
    $('#changepassword-user').click(ShowForm);
    $('#modal-user').on('submit', '.changepassword-modal-form',SaveFormAndStayInModal);

    // CRUD Areas
    $('#bootstrapTableModal').on('submit','.editarArea',bootstrapTableForm);
    $('#bootstrapTableModal').on('submit','.eliminarArea',bootstrapTableForm);
    // CRUD Subareas
    $('#bootstrapTableModal').on('submit','.editarSubarea',bootstrapTableForm);
    $('#bootstrapTableModal').on('submit','.eliminarSubarea',bootstrapTableForm);
    // CRUD Usuarios
    $('#bootstrapTableModal').on('submit','.editarUsuario',bootstrapTableForm);
    $('#bootstrapTableModal').on('submit','.eliminarUsuario',bootstrapTableForm);
    $('#bootstrapTableModal').on('submit','.cambiarRol',bootstrapTableForm);
    

});