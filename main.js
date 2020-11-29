var backend_url = 'http://localhost:5000/';
var search_books = backend_url+'search-books';
var params = '';

function clearFilter(){
	console.log('clear');
	document.getElementById('name').value = '';
	document.getElementById('genre').value = '';
	document.getElementById('rating').value = '--';
}

function search(){
	var name = document.getElementById('name').value;
	var genre = document.getElementById('genre').value;
	var rating = document.getElementById('rating').value;
	if(name !== undefined && name.length>0){
		params+='name='+name+'&';
	}
	if(genre !== undefined && genre.length>0){
		params+='genre='+genre+'&';
	}
	if(rating !== undefined && rating !== '--' && rating.length>0){
		params+='rating='+rating+'&';
	}
	if(params.length !== 0){
		params = "?"+params.substring(0,params.length-1);	
	}
	console.log(params);
	var xhttp = new XMLHttpRequest();
  	xhttp.onreadystatechange = function() {
	    if (this.readyState == 4 && this.status == 200) {
	      console.log(this.responseText);
	      loadDataIntoTable(this.responseText);
	    }
	  };
	  xhttp.open("GET", search_books+params, true);
	  xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
	  xhttp.setRequestHeader("Access-Control-Allow-Origin", "*");
	  xhttp.send();
	  params = "";
}

function loadDataIntoTable(data) {
  var i;
  var json = JSON.parse(data);
  if(json.length === 0){
  	document.getElementById("table").innerHTML = "<tr><th>There is no data</th></tr>";
  }else{
	var table="<tr><th>Name</th><th>Genre</th><th>Price</th><th>UPC</th><th>inStock</th><th>Available</th><th>Rating</th></tr>";
	  for (i = 0; i <json.length; i++) { 
	    table += "<tr><td>" +
	    json[i].name +
	    "</td><td>" +
	    json[i].genre +
	    "</td><td>" +
	    json[i].price +
	    "</td><td>" +
	    json[i].upc +
	     "</td><td>" +
	    json[i].stock +
	     "</td><td>" +
	    json[i].available +
	     "</td><td>" +
	    json[i].rating +
	    "</td></tr>";
	  }
	  document.getElementById("table").innerHTML = table;
  }
}