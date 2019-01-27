/*------------------------------------------------------------------------------------------*/
/*                        Para incluir el CSRF token en el headers                          */
/*------------------------------------------------------------------------------------------*/

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

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

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

/*-----------------------------------------------------------------------------------------*/
/*                      Para dar formato a los botones de las tablas                       */
/*-----------------------------------------------------------------------------------------*/

    function operateAreas(value, row, index) {
        return [
            '<a class="viewArea" href="javascript:void(0)" title="Ver">',
            '<i class="far fa-eye"></i>',
            '</a>  ',
            '<a class="editArea" href="javascript:void(0)" title="Editar" >',
            '<i class="far fa-edit"></i>',
            '</a>  ',
            '<a class="removeArea" href="javascript:void(0)" title="Eliminar">',
            '<i class="fa fa-trash"></i>',
            '</a>'
        ].join('');
    }

    function operateSubareas(value, row, index) {
        
        return [
            '<a class="viewSubarea" href="javascript:void(0)" title="Ver">',
            '<i class="far fa-eye"></i>',
            '</a>  ',
            '<a class="editSubarea" href="javascript:void(0)" title="Editar" >',
            '<i class="far fa-edit"></i>',
            '</a>  ',
            '<a class="removeSubarea" href="javascript:void(0)" title="Eliminar">',
            '<i class="fa fa-trash"></i>',
            '</a>'
        ].join('');
    }

    function operateUsuarios(value, row, index) {
        return [
            
            '<a class="viewUsuario" href="javascript:void(0)" title="Ver">',
            '<i class="far fa-eye"></i>',
            '</a>  ',
            '<a class="editUsuario" href="javascript:void(0)" title="Editar" >',
            '<i class="far fa-edit"></i>',
            '</a>  ',
            '<a class="removeUsuario" href="javascript:void(0)" title="Eliminar">',
            '<i class="fa fa-trash"></i>',
            '</a>  ' ,
            '<a class="changeRol" href="javascript:void(0)" title="Roles" >', 
                '<i class="fas fa-users"></i>', 
            '</a>' 
        ].join('');
    }

    function operateArbitros(value, row, index) {
        return [
            
            '<a class="viewArbitro" href="javascript:void(0)" title="Ver">',
            '<i class="far fa-eye"></i>',
            '</a>  ',
            '<a class="editArbitro" href="javascript:void(0)" title="Editar" >',
            '<i class="far fa-edit"></i>',
            '</a>  ',
            '<a class="removeArbitro" href="javascript:void(0)" title="Eliminar">',
            '<i class="fa fa-trash"></i>',
            '</a>  ' ,
        ].join('');
    }

/*-----------------------------------------------------------------------------------------*/
/*                  Para capturar el evento de los botones de las tablas                   */
/*-----------------------------------------------------------------------------------------*/

    window.operateEvents = {
        'click .viewArea': function (e, value, row, index) {
            var route=e.currentTarget.baseURI+$(this).attr("class")+"/"+row.id;
        
            $.ajax({
                url: route,
                type: 'get',
                data: row.id,
                dataType: 'json',
                beforeSend: function(){
                    $('#bootstrapTableModal').modal('show');  
                },
                success: function (data){
                    // console.log(data);
                    $('#bootstrapTableModal .modal-content').html(data.content);
                }
            });


        },
        'click .editArea': function (e, value, row, index) {
            var route=e.currentTarget.baseURI+$(this).attr("class")+"/"+row.id;
            $.ajax({
                url: route,
                type: 'get',
                data: row.id,
                dataType: 'json',
                beforeSend: function(){
                    $('#bootstrapTableModal').modal('show');  
                },
                success: function (data){
                    // console.log(data);
                    $('#bootstrapTableModal .modal-content').html(data.content);
                }
            });
        },
        'click .removeArea': function (e, value, row, index) {
            var route=e.currentTarget.baseURI+$(this).attr("class")+"/"+row.id;
            console.log(route);
            $.ajax({
                url: route,
                type: 'get',
                data: row.id,
                dataType: 'json',
                beforeSend: function(){
                    $('#bootstrapTableModal').modal('show');  
                },
                success: function (data){
                    // console.log(data);
                    $('#bootstrapTableModal .modal-content').html(data.content);
                    // $table.bootstrapTable('remove', {
                    //     field: 'id',
                    //     values: [row.id]
                    // });
                }
            });
        },
        'click .viewSubarea': function (e, value, row, index) {
            var route=e.currentTarget.baseURI+$(this).attr("class")+"/"+row.id;
            
            $.ajax({
                url: route,
                type: 'get',
                data: row.id,
                dataType: 'json',
                beforeSend: function(){
                    $('#bootstrapTableModal').modal('show');  
                },
                success: function (data){
                    // console.log(data);
                    $('#bootstrapTableModal .modal-content').html(data.content);
                }
            });


        },
        'click .editSubarea': function (e, value, row, index) {
            var route=e.currentTarget.baseURI+$(this).attr("class")+"/"+row.id;
            console.log(route);
            $.ajax({
                url: route,
                type: 'get',
                data: row.id,
                dataType: 'json',
                beforeSend: function(){
                    $('#bootstrapTableModal').modal('show');  
                },
                success: function (data){
                    // console.log(data);
                    $('#bootstrapTableModal .modal-content').html(data.content);
                }
            });
        },
        'click .removeSubarea': function (e, value, row, index) {
            var route=e.currentTarget.baseURI+$(this).attr("class")+"/"+row.id;
            console.log(route);
            $.ajax({
                url: route,
                type: 'get',
                data: row.id,
                dataType: 'json',
                beforeSend: function(){
                    $('#bootstrapTableModal').modal('show');  
                },
                success: function (data){
                    // console.log(data);
                    $('#bootstrapTableModal .modal-content').html(data.content);
                    // $table.bootstrapTable('remove', {
                    //     field: 'id',
                    //     values: [row.id]
                    // });
                }
            });
        },
        'click .viewUsuario': function (e, value, row, index) {
            var route=e.currentTarget.baseURI+$(this).attr("class")+"/"+row.id;
            console.log(route);
            $.ajax({
                url: route,
                type: 'get',
                data: row.id,
                dataType: 'json',
                beforeSend: function(){
                    $('#bootstrapTableModal').modal('show');  
                },
                success: function (data){
                    // console.log(data);
                    $('#bootstrapTableModal .modal-content').html(data.content);
                }
            });


        },
        'click .editUsuario': function (e, value, row, index) {
            var route=e.currentTarget.baseURI+$(this).attr("class")+"/"+row.id;
            console.log(route);
            console.log(row.id);
            $.ajax({
                url: route,
                type: 'get',
                data: row.id,
                dataType: 'json',
                beforeSend: function(){
                    $('#bootstrapTableModal').modal('show');  
                },
                success: function (data){
                    // console.log(data);
                    $('#bootstrapTableModal .modal-content').html(data.content);
                },
                error: function () {
                    $('#bootstrapTableModal .modal-content').html("No se puede procesar su solicitud el id "+row.id+" no existe");
                }
            });
        },
        'click .removeUsuario': function (e, value, row, index) {
            var route=e.currentTarget.baseURI+$(this).attr("class")+"/"+row.id;
            console.log(route);
            $.ajax({
                url: route,
                type: 'get',
                data: row.id,
                dataType: 'json',
                beforeSend: function(){
                    $('#bootstrapTableModal').modal('show');  
                },
                success: function (data){
                    // console.log(data);
                    $('#bootstrapTableModal .modal-content').html(data.content);
                    // $table.bootstrapTable('remove', {
                    //     field: 'id',
                    //     values: [row.id]
                    // });
                }
            });
        },
        'click .changeRol': function (e, value, row, index) {
            var route=e.currentTarget.baseURI+$(this).attr("class")+"/"+row.id;
            console.log(route);
            $.ajax({
                url: route,
                type: 'get',
                data: row.id,
                dataType: 'json',
                beforeSend: function(){
                    $('#bootstrapTableModal').modal('show');  
                },
                success: function (data){
                    // console.log(data);
                    $('#bootstrapTableModal .modal-content').html(data.content);
                    // $table.bootstrapTable('remove', {
                    //     field: 'id',
                    //     values: [row.id]
                    // });
                }
            });
        },
        'click .editArbitro': function (e, value, row, index) {
            var route=e.currentTarget.baseURI+$(this).attr("class")+"/"+row.id;
            console.log(route);
            $.ajax({
                url: route,
                type: 'get',
                data: row.id,
                dataType: 'json',
                beforeSend: function(){
                    $('#bootstrapTableModal').modal('show');  
                },
                success: function (data){
                    // console.log(data);
                    $('#bootstrapTableModal .modal-content').html(data.content);
                }
            });
        },
        'click .viewArbitro': function (e, value, row, index) {
            var route=e.currentTarget.baseURI+$(this).attr("class")+"/"+row.id;
            console.log(route);
            $.ajax({
                url: route,
                type: 'get',
                data: row.id,
                dataType: 'json',
                beforeSend: function(){
                    $('#bootstrapTableModal').modal('show');  
                },
                success: function (data){
                    // console.log(data);
                    $('#bootstrapTableModal .modal-content').html(data.content);
                }
            });
        },
        'click .removeArbitro': function (e, value, row, index) {
            var route=e.currentTarget.baseURI+$(this).attr("class")+"/"+row.id;
            console.log(route);
            $.ajax({
                url: route,
                type: 'get',
                data: row.id,
                dataType: 'json',
                beforeSend: function(){
                    $('#bootstrapTableModal').modal('show');  
                },
                success: function (data){
                    // console.log(data);
                    $('#bootstrapTableModal .modal-content').html(data.content);
                }
            });
        },
    };


// Para generar excel 
function buildBoostrapTable(idTabla, type) {
    $tabla = $(idTabla);

    $tabla.bootstrapTable("refresh",{
        url: $tabla.attr("data-url"),
        query: {
        export: type,
    }
    }
    );
        
}

  
