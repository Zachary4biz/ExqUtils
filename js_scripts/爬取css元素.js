// css = "caption~ tbody th a";
// css = "#mw-pages .mw-category-group a";
// css = ".div_title_question";
css = ".title-article";
var elements = document.querySelectorAll(css);
// 和Xpath提取不同，elements 是一个NodeList；
// 不要尝试使用 for...in 或者 for each...in 来遍历一个NodeList 对象中的元素
var result = new Array();
for (var i = 0; i < elements.length; ++i) {
  result.push(elements[i].textContent);
}
result_set = [...new Set(result)];
console.log(result_set.length)
var result_text = result_set.join("\n");
console.log(result_text);
prompt("cssPath: "+css+"\nfindResult as follow: [totalCnt="+result.length+"]",result_text);

// prompt("xpath抓取到的内容如下",result_text);




