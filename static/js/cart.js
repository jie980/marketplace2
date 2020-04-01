//Check All Function
window.onload=function(){
	document.getElementById("ckAll").onclick=function(){
		var cks=document.getElementsByName("ck");
		for(var i=0; i<cks.length;i++){
			//selected all items
			cks[i].checked=this.checked;
		}
	}
}

var cks=document.getElementsByName("ck");
 for(var i=0;i<cks.length;i++){ //循环得到单个tr
	 cks[i].onclick=function(){ // 当点击每个当tr的时候都会触发点击事件
		    for(var i=0;i<cks.length;i++){// 循环得到单个td
			    if(!cks[i].checked){ //如果单个特点的点击等于false 就返回
				    document.getElementById("ckAll").checked = false;//那么ckAll就等于false
				    return;
			    }
		    }
		 document.getElementById("ckAll").checked = true;//否则就等于true 说明为全选状态
	 }
 }
 getSum();

 function getSum(){
	 var tbody=document.getElementsByTagName("tbody")[0];
	 var sum=0;
	 for(var i=0; i<tbody.children.length;i++){
		 var tr=tbody.children[i];
		 var td=tr.children;
		 var price=td[2].innerText;
		 var count=$("#qty").val();
		 
	 }
 }




