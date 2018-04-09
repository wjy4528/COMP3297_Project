$(".search_cate").click(function(e){
var search_url = '/image/search?searchstring=' + e.target.innerHTML
window.location.href = search_url
});

function add_likes(event){
x=event.target;
img=x.dataset.imgid;
x.parentElement.children[1].textContent=(parseInt(x.parentElement.children[1].textContent)+1);
$.get('/api/updatelike/'+img, function(){
});
}

function sortByOptions(event){
var compareFunc;

var opt = event.target.options[event.target.selectedIndex].value
console.log( opt )
if(opt=="time"){
	compareFunc = function(a,b){
		return a.dataset.upload - b.dataset.upload;
	}
}else if(opt=="popularity"){
	compareFunc = function(a,b){
		return a.dataset.like - b.dataset.like;
	}
}else{
	return 0;
}

var all_items = document.getElementsByClassName('item')
var all_parent = document.getElementsByClassName('column')
for (var i=0;i<4;i++){
	console.log(all_parent[i])
}

if (all_items.length <= 4){
	var parent = all_items[0].parentNode
	parent.style.display="-webkit-inline-box"
	all_items = Array.prototype.slice.call( all_items )
	all_items.sort( compareFunc )

	for( var i=0;i<all_items.length;i++ ){
		parent.insertBefore( all_items[i], parent.firstChild )
	}

}else{
	all_items = Array.prototype.slice.call( all_items )
	all_items.sort( compareFunc )
	for( var i=0;i<all_items.length;i++ ){
		console.log(all_items[i])
		var res=i%4
		console.log(all_parent[res])
		all_parent[res].appendChild( all_items[i] )
	}
	
}


}

function add_download(event){
x=event.target;
img=x.dataset.imgid;
x.parentElement.children[1].textContent=(parseInt(x.parentElement.children[1].textContent)+1);

/*
$.get('/api/update_download/'+img, function(){
	
});
*/
}
