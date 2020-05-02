
var check = false;

window.onload=function(){
  changeTotal();
}



function changeVal(el) {
  var qt = parseFloat(el.parent().children(".qt").html());
  var price = parseFloat(el.parent().children(".price").html());
  var eq = Math.round(price * qt * 100) / 100;
  
  el.parent().children(".full-price").html( eq + "$" );
  
  changeTotal();			
}

function changeTotal() {
  
  var price = 0;
  
  $(".full-price").each(function(index){
    price += parseFloat($(".full-price").eq(index).html());
  });
  
  price = Math.round(price * 100) / 100;
  var tax = Math.round(price * 0.05 * 100) / 100
  var shipping = parseFloat($(".shipping span").html());
  var fullPrice = Math.round((price + tax + shipping) *100) / 100;
  
  if(price == 0) {
    fullPrice = 0;
  }
  
  $(".subtotal span").html(price);
  $(".tax span").html(tax);
  $(".total span").html(fullPrice);
  $(".price").val(fullPrice);

}

$(document).ready(function(){
  // use ajax to submit data to server
  $(".remove").click(function(){
    var pid =  $(this).parent().children(".pid").html();
    var data = {"pid": pid}; 
    $.ajax({
      method:"GET",
      url: '/app/cart/delete',
      dataType: "json",
      async : false,
      data: 
      {
        pid: pid,

      },
    }).done(function(data){
    })
  });
  $(".remove").click(function(){
    var el = $(this);
    el.parent().parent().addClass("removed");
    window.setTimeout(
      function(){
        el.parent().parent().slideUp('fast', function() { 
          el.parent().parent().remove(); 
          if($(".product").length == 0) {
            if(check) {
              $("#cart").html("<h1>The shop does not function, yet!</h1><p>If you liked my shopping cart, please take a second and heart this Pen on <a href='https://codepen.io/ziga-miklic/pen/xhpob'>CodePen</a>. Thank you!</p>");
            } else {
              $("#cart").html("<h1>No products!</h1>");
            }
          }
          changeTotal(); 
        });
      }, 200);
  });

  
  $(".qt-plus").click(function(){
    var left = $(this).parent().children(".stock").html();

    child = $(this).parent().children(".qt");
    if(parseInt(child.html()) < left) {
      child.html(parseInt($(this).parent().children(".qt").html()) + 1);

    }
    child.parent().children(".full-price").addClass("added");


    

    var el = $(this);
    window.setTimeout(function(){el.parent().children(".full-price").removeClass("added"); changeVal(el);}, 150);
  });
  // use ajax to submit data to server
  $(".qt-plus").click(function(){
    var pid =  $(this).parent().children(".pid").html();

    var data = {"pid": pid}; 

    $.ajax({
      method:"GET",
      url: '/app/cart/edit1',
      dataType: "json",
      async : false,
      data: 
      {
        pid: pid,

      },
    }).done(function(data){
    })
  })
  
  $(".qt-minus").click(function(){
    child = $(this).parent().children(".qt");
    
    if(parseInt(child.html()) > 1) {
      child.html(parseInt(child.html()) - 1);
    }
    
    $(this).parent().children(".full-price").addClass("minused");
    
    var el = $(this);
    window.setTimeout(function(){el.parent().children(".full-price").removeClass("minused"); changeVal(el);}, 150);
  })
  // use ajax to submit data to server
  $(".qt-minus").click(function(){
    var pid =  $(this).parent().children(".pid").html();
    var data = {"pid": pid}; 
    $.ajax({
      method:"GET",
      url: '/app/cart/edit2',
      dataType: "json",
      async : false,
      data: 
      {
        pid: pid,
      },
    }).done(function(data){
    })
  })

  
  window.setTimeout(function(){$(".is-open").removeClass("is-open")}, 1200);
  
  $(".btn").click(function(){
    //window.location.href = "/app/checkout/";
    changeTotal();
  });
  //$(".btn").click(function(){
  //   var price =  $('.totalprice').html();
  //   var shippingfee = $('.shippingfee').html();
  //   console.log(price)
  //   var data = {"price": price , "shippingfee": shippingfee}; 
  //   $.ajax({
  //     method:"GET",
  //     url: '/app/checkout',
  //     dataType: "json",
  //     async : false,
  //     data: 
  //     {
  //       price: price,
  //       shippingfee: shippingfee,
  //     },
  //   }).done(function(data){
  //     var str='';

  //   })

  // });
//   $.ajax({
//     type:"POST",
//     url: //你的请求程序页面随便啦
//     async:false,//同步：意思是当有返回值以后才会进行后面的js程序。
//     data://请求需要发送的处理数据
//     success:function(msg){
//         if (msg) {//根据返回值进行跳转
//             window.location.href = '你的跳转的目标地址';
//         }
// }

});
