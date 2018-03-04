$(document).ready(function () {
        var csrftoken = Cookies.get('csrftoken')
    $('#lec_id').hide();
   $('input[type=radio]').click(function(){
        var user = this.value;
       if (user === "lecturer") {
           $("#stu_id").hide();
           $("#lec_id").show();
       }else {
           $("#stu_id").show();
           $("#lec_id").hide();
       }
   });
});