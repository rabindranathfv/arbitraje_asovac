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
    $('[data-toggle="tooltip"]').tooltip();
});


$('#myModal').on('shown.bs.modal', function () {
  $('#myInput').trigger('focus')
});

// Ajax para modales

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
    
    //show areas 
    $('.show_areas').click(ShowForm);
    $('#modal-user').on('submit','.change_area',SaveForm);
   
    // validate ValidateAccess
    $('.show-form-access').click(ValidateAccess);
    $('#rol_validate').on('submit','.validate_access',ValidateAccess);
});