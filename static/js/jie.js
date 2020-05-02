$(document).ready(function(){
  $(".delete").click(function(){
    var pid = $(".pid").html();
    var data = {"pid": pid}; 
    $.ajax({
      method:"GET",
      url: '/app/myaccount/myproducts/deleted/',
      dataType: "json",
      async : false,
      data: 
      {
        pid: pid,

      },
    }).done(function(data){
    })
  });
})