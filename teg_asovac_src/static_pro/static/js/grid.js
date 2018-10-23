
// A $( document ).ready() block.
$( document ).ready(function() {
    console.log( "ready!" );

    var table = $('#table').val();
    // your custom ajax request here

    $(function() {
        console.log("test");
        function ajaxRequest(params) {
            // data you need
            console.log(params.data);
            // just use setTimeout
            setTimeout(function () {
                params.success({
                    total: 100,
                    rows: [{
                        "id": 0,
                        "name": "Item 0",
                        "price": "$0"
                    }]
                });
            }, 1000);
        }
    })



});