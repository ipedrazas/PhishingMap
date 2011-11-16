

function phiIp(ip,longitude,latitude){
	this.ip = ip;
	this.longitude = longitude;
	this.latitude = latitude;
}

	function setData(){
		  $.getJSON("getGeoData.php",
	      function(data){		
				if(data!=null){
					$.each(data, function(i,item){
									newGMarker(item);
					});		
				}
		  });		
		}

	 function setClusterData(){
		 var markers = [];
		 var markerCluster = null;
		  $.getJSON("getGeoData.php", function(data){		
				if(data!=null){
					$.each(data, function(i,item){
						marker = newMarkerForCluster(item);
						markers.push(marker);
					});	
					 markerCluster = new MarkerClusterer(map, markers);
				}
		  });	
		}

	 function newMarkerForCluster(item){
		 var latLng = 
			 new google.maps.LatLng(item.latitude,item.longitude);
		 var marker = new google.maps.Marker({
	            position: latLng
	          });
		 return marker;
	}
	 
	function newGMarker(item){
		 var latlng = new google.maps.LatLng(item.latitude,item.longitude);
		 var marker = new google.maps.Marker({
				map: map, 
				position: latlng,
				title: checkValue(item.ip)
			});
		 return marker;
	}
	
	function checkValue(value){
		if(value!=null){
			if(value!="null"){
				return value;
			}
		}
		return "&nbsp;"
	}
	