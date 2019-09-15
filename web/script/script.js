//提供通用的根据id绑定单击事件的工具方法
function $(btnId , fun){
	var btn = document.getElementById(btnId);
	btn.onclick = fun;
}