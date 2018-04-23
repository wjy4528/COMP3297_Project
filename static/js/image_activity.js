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



function add_download(event){
	x=event.target;
	img=x.dataset.imgid;
	x.parentElement.children[1].textContent=(parseInt(x.parentElement.children[1].textContent)+1);

/*
$.get('/api/update_download/'+img, function(){
	
});
*/
}


var delete_image_confirm = function(event){
		if (confirm('Are you sure you want to delete this image?')) {
			let url = "/image/delete/data/" + event.target.dataset.imgid;
			window.location = url;
		}		
}