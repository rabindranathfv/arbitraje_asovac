$(document).ready(function () {
    $(function () {
        $.ajaxSetup({
            headers: { "X-CSRFToken": getCookie("csrftoken") }
        });
    });

    function getCookie(c_name)
    {
        if (document.cookie.length > 0)
        {
            c_start = document.cookie.indexOf(c_name + "=");
            if (c_start != -1)
            {
                c_start = c_start + c_name.length + 1;
                c_end = document.cookie.indexOf(";", c_start);
                if (c_end == -1) c_end = document.cookie.length;
                return unescape(document.cookie.substring(c_start,c_end));
            }
        }
        return "";
    }
    
});

    function operateFormatter(value, row, index) {
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
        }
    };




  
