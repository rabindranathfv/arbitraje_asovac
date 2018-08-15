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

$(document).ready(function(){
    $('.show-form').click(function(){
        $.ajax({
            url: '/dashboard/usuario/crear',
            type: 'get',
            dataType: 'json',
            beforeSend: function(){
              $('#modal-user').modal('show');  
            },
            success: function (data){
                $('#modal-user .modal-content').html(data.html_form);
            }
        })
    });

    $('#modal-user').on('submit', 'create-form', function(){
        var form= $(this);
        alert('modal-book');
        $.ajax({
            url: form.attr('data-url'),
            data: form.serialize(),
            type: form.attr('method'),
            dataType: 'json',

            success: function(data){
                if(data.form_is_valid){
                    console.log('data is saved')
                }else{
                    $('#modal-book .modal-content').html(data.html_form)
                }
            }
        })
        return false;
    });

});