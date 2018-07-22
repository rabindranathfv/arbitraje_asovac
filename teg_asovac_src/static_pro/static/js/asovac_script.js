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
})

