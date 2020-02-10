function openwin(){ 
	console.log("abcabcacb") ;
}

// $("#reg").dialog({title:"asdf",buttons:{"check":openwin,"cancel":$(this).dialog("close")},position:"center"});


//复制
var toCopy = "abcabacababab";
var input = document.createElement('input');
input.setAttribute('readonly', 'readonly');
input.setAttribute('value', toCopy);
document.body.appendChild(input);
input.setSelectionRange(0, 9999);

var name=prompt("xpath抓取到的内容如下","填充抓取内容");
if(name){
	 alert("欢迎您："+ name)
} else {
	 alert("不能为空")
}

// alert(toCopy);

// if(confirm("check")){
//     console.log("true");
//     if (document.execCommand('copy')) {
// 		document.execCommand('copy');
// 		console.log('复制成功');
//     }else console.log("复制失败");
// }else{
//     console.log("false");
// }


document.body.removeChild(input);

