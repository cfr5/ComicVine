var map = new google.maps.Map(document.getElementById('map'), {
    mapTypeControl: true,
    mapTypeControlOptions: {
      style: google.maps.MapTypeControlStyle.DROPDOWN_MENU
    },
    mapTypeId: google.maps.MapTypeId.ROADMAP,
    streetViewControl: true
  }),
  infowindow = new google.maps.InfoWindow(),
  marker,
  latlng,
  watchID


function createMarker(place) {
  var placeLoc = place.geometry.location,
    marker = new google.maps.Marker({
      map: map,
      position: place.geometry.location,
    }),
    content = '<strong>' + place.name + '</strong><br>' + place.vicinity;

  google.maps.event.addListener(marker, 'click', function() {
    infowindow.setContent(content);
    infowindow.open(map, this);
  });
}

function processLocation(position) {
  // Get position
  var lat = position.coords.latitude,
    lng = position.coords.longitude,
    latlng = new google.maps.LatLng(lat, lng);

  // Set map location
  map.setOptions({
        center: latlng,
        scrollwheel: false,
        zoom: 12
      });

      // Add marker to map
      marker = new google.maps.Marker({
    position: latlng,
    map: map,
    title: 'Test Title'
  });

  // Event listener for users current location marker
  google.maps.event.addListener(marker, 'click', function() {
    infowindow.setContent('This is your current location!<br>We\'re now showing you all the Libraries in a 8 km radius');
    infowindow.open(map, this);
  });

  // Open the window when the app has loaded
  google.maps.event.trigger(marker, 'click', function() {
    infowindow.setContent('This is your current location!<br>We\'re now showing you all the Libraries in a 8 km radius');
    infowindow.open(map, this);
  });

  // Request any Comic's shop within 8 km from the current location
  var request = {
    location: latlng,
    radius: 8000.00,
    type:['book_store'],
    name: 'Comics'
  };

  // Create the Places request
  var service = new google.maps.places.PlacesService(map);
    service.search(request, function(results, status){
      if (status == google.maps.places.PlacesServiceStatus.OK) {
        for (var i = 0; i < results.length; i++) {
          var place = results[i];
          createMarker(results[i]);
        }
      }
    });
}

// Doesn't appear to be executed??
function handleLocationErrors(err) {
  switch(err.code) {
    case err.PERMISSION_DENIED:
      alert('You have decided not to share your location information');
      break;
    case err.POSITION_UNAVAILABLE:
      alert('I\'m sorry but we could not detect your location');
      break;
    case err.TIMEOUT:
      alert('I\'m sorry but the system timed out while waiting to retrieve your location information');
      break;
    default:
      alert('I\'m sorry but an unknown error occurred');
      break;
  }
}
navigator.geolocation.getCurrentPosition(processLocation, handleLocationErrors);
