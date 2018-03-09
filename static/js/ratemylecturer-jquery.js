$(document).ready(function() {
        $('#lec_id').hide();

        $('.user_radio').click(function () {
            var user = this.value;
            if (user === "lecturer") {
                $("#stu_id").hide();
                $("#lec_id").show();
                $("#register_header").html("Register as a Lecturer");

            }
            else {
                $("#stu_id").show();
                $("#lec_id").hide();
                $("#register_header").html("Register as a Student");
            }
        });


        $("#lecturer_name").autocomplete({
            source: name_list,
            select: function (event, ui) {
                event.preventDefault();
                $("#lecturer_name").val(ui.item.name);
                $("#lecturer_uni").val(ui.item.uni);
                $("#lecturer_depart").val(ui.item.depart);
                var changed = JSON.stringify({"name": ui.item.name, "user": ui.item.user});
                $.ajax({
                    method: 'POST',
                    url: "/ratemylecturer/register/lecturer_ajax_data/",
                    dataType: 'text',
                    data: changed,
                    contentType: 'application/json'
                })
            }
        });


    });

