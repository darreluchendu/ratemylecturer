$(document).ready(function() {
        $(".user_radio" ).checkboxradio({
            icon:false
        })

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
  $.getJSON('/static/js/uni_ranking.json', function(data) {
      var data_list = []
      data.forEach(function (dict) {
          data_list.push({"label": dict["name"], "category": "University"})
      });
      lecturers.forEach(function (dict) {
        data_list.push(dict)
    });

      $.widget("custom.catcomplete", $.ui.autocomplete, {
          _create: function () {
              this._super();
              this.widget().menu("option", "items", "> :not(.ui-autocomplete-category)");
          },
          _renderMenu: function (ul, items) {
              var that = this,
                  currentCategory = "";
              $.each(items, function (index, item) {
                  var li;
                  ul.addClass('autocpm')
                  if (item.category != currentCategory) {
                      ul.append("<li class='ui-autocomplete-category'>" + item.category + "</li>");
                      currentCategory = item.category;
                  }
                  li = that._renderItemData(ul, item);
                  if (item.category) {
                      li.attr("aria-label", item.category + " : " + item.label);
                  }
              });
          }
      });

      $(".main-search").catcomplete({
          delay: 0,
          minLength: 2,
          source: data_list,
          select: function (event, ui) {
              event.preventDefault();
             window.location.href = '/ratemylecturer/profile/'+ui.item.username
          }
      });
    $(".b1").hover(function() {
        $("#var").html('the school')
    },function(){
        $("#var").html('what')
    })
      $(".b2").hover(function() {
        $("#var").html('the outlet')
    },function(){
        $("#var").html('what')
    })
      $(".b3").hover(function() {
        $("#var").html('the professor')
    },function(){
        $("#var").html('what')
    })

      $('.register').click(function(event) {
          $('#user_form_lecturer').submit()
      })

$("#review_rating").rating().on("rating:change", function(event, value, caption) {


        $('#id_rating').val(value)
    });
$("#id_edit_picture").hide()
      $(".edit_pic").click(function(event) {
          event.preventDefault()

    $("input[id='id_edit_picture']").click();


});


$("label[for='id_edit_picture']").hide();
$("label[for='id_picture_url']").hide();
$("input[type='url']").hide()
//
  $("input[id='id_edit_picture']").change(function() {
        $("#picture_form").submit()
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


  })

})

