function myTrim(x){
	var replaced = x.trim().replace(/[^a-zA-Z0-9]+$/,"").replace(/^[^a-zA-Z0-9]+/,"")
	console.log("replace result: ",replaced);
    return replaced;
}


window.onkeyup=function(){
	if(18 == event.keyCode){
		selStr = myTrim(window.getSelection().toString());
		console.log("selStr is ",selStr)

		var textAreaList = document.getElementsByTagName("textarea");
		var target = textAreaList[0];
		var ori_content = target.value;
		console.log("ori_content is ",ori_content);
		if(selStr!=""){
		    if(ori_content==""){
		        target.value=selStr;
		    }else{
		        target.value=ori_content+","+selStr;
		    }
		}
		console.log("new content is ",target.value);
	}
}



