function bindEmailCaptchaClick(){
  $("#get_code").click(function (event){
    var $this = $(this);
    event.preventDefault();

    var email = $("input[name='email']").val();
    $.ajax({
      url: "/authority/validation_code?email="+email,
      method: "GET",
      success: function (result){
        var code = result['code'];
        if(code == 200){
          var seconds = 60;
          $this.off("click");
          var timer = setInterval(function (){
            $this.text(seconds);
            seconds--;
            if(seconds <= 0){
              clearInterval(timer);
              $this.text("Get Code");
              bindEmailCaptchaClick();
            }
          }, 1000);
        }else{
        }
      },
      fail: function (error){
        console.log(error);
      }
    })
  });
}


$(function (){
  bindEmailCaptchaClick();
});