$(function(){
            var ifCOD = document.getElementById("cod");
            var ifPAL = document.getElementById("paypal");
            // var firstname = document.getElementById("first_name");
            // var lastname = document.getElementById("last_name");
            // localStorage.setItem("firstname", firstname);
            // localStorage.setItem("lastname", lastname);
            $('.btn').on('click', function(){
                if(ifCOD.checked){
                    if(ifPAL.checked){
                        alert("cannot choose both");
                        return;
                    }
                    // alert("pay by cash is checked");
                    window.location.href = "cod.html";
                }
                else if(ifPAL.checked){
                    // alert("pay by paypal is checked");
                    window.location.href = "paypal.html";
                }else{
                    alert("have to choose one method to pay");
                    return;
                }
            });

        });