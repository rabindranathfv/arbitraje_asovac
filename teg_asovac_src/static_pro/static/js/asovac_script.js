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
    var ShowForm= function(){
        var btn= $(this);
        console.log('ShowForm');
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

    var SaveForm= function(){
        var form= $(this);
        alert('Save');
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
                    $('#modal-book .modal-content').html(data.html_form)
                }
            }
        });
        return false;
    };

    // create
    $('.show-form').click(ShowForm);
    $('#modal-user').on('submit', '.create-form',SaveForm);

    //update
    $('#show_users').on('click','.show-form-update',ShowForm);
    $('#modal-user').on('submit','.update-form',SaveForm);

    //delete
    $('#show_users').on('click','.show-form-delete',ShowForm);
    $('#modal-user').on('submit','.delete-form',SaveForm);
});