$(document).ready(function() {

    $( "#id_name" ).autocomplete({
        source: name_list,
        select: function (event, ui) {
            event.preventDefault();
            $("#id_name").val(ui.item.name)
        }
    });




});
