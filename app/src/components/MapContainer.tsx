import { GoogleMap, Marker, useJsApiLoader } from '@react-google-maps/api';
import { useSelector, useDispatch } from 'react-redux';
import { RootState } from '../redux/store';
import { setPosition } from '../redux/mapSlice';

const containerStyle = {
  width: '100%',
  height: '100vh',
};

// Data points
const points = [
  { ID: 'F1', Name: 'Cairo International Airport', Type: 'Airport', lat: 31.41, lng: 30.11 },
  { ID: 'F2', Name: 'Ramses Railway Station', Type: 'Transit Hub', lat: 31.25, lng: 30.06 },
  { ID: 'F3', Name: 'Cairo University', Type: 'Education', lat: 31.21, lng: 30.03 },
  { ID: 'F4', Name: 'Al-Azhar University', Type: 'Education', lat: 31.26, lng: 30.05 },
  { ID: 'F5', Name: 'Egyptian Museum', Type: 'Tourism', lat: 31.23, lng: 30.05 },
  { ID: 'F6', Name: 'Cairo International Stadium', Type: 'Sports', lat: 31.3, lng: 30.07 },
  { ID: 'F7', Name: 'Smart Village', Type: 'Business', lat: 30.97, lng: 30.07 },
  { ID: 'F8', Name: 'Cairo Festival City', Type: 'Commercial', lat: 31.4, lng: 30.03 },
  { ID: 'F9', Name: 'Qasr El Aini Hospital', Type: 'Medical', lat: 31.23, lng: 30.03 },
  { ID: 'F10', Name: 'Maadi Military Hospital', Type: 'Medical', lat: 31.25, lng: 29.95 },
  { ID: '1', Name: 'Maadi', Type: 'Residential', lat: 31.25, lng: 29.96 },
  { ID: '2', Name: 'Nasr City', Type: 'Mixed', lat: 31.34, lng: 30.06 },
  { ID: '3', Name: 'Downtown Cairo', Type: 'Business', lat: 31.24, lng: 30.04 },
  { ID: '4', Name: 'New Cairo', Type: 'Residential', lat: 31.47, lng: 30.03 },
  { ID: '5', Name: 'Heliopolis', Type: 'Mixed', lat: 31.32, lng: 30.09 },
  { ID: '6', Name: 'Zamalek', Type: 'Residential', lat: 31.22, lng: 30.06 },
  { ID: '7', Name: '6th October City', Type: 'Mixed', lat: 30.98, lng: 29.93 },
  { ID: '8', Name: 'Giza', Type: 'Mixed', lat: 31.21, lng: 29.99 },
  { ID: '9', Name: 'Mohandessin', Type: 'Business', lat: 31.2, lng: 30.05 },
  { ID: '10', Name: 'Dokki', Type: 'Mixed', lat: 31.21, lng: 30.03 },
  { ID: '11', Name: 'Shubra', Type: 'Residential', lat: 31.24, lng: 30.11 },
  { ID: '12', Name: 'Helwan', Type: 'Industrial', lat: 31.33, lng: 29.85 },
  { ID: '13', Name: 'New Administrative Capital', Type: 'Government', lat: 31.8, lng: 30.02 },
  { ID: '14', Name: 'Al Rehab', Type: 'Residential', lat: 31.49, lng: 30.06 },
  { ID: '15', Name: 'Sheikh Zayed', Type: 'Residential', lat: 30.94, lng: 30.01 },
];

const MapContainer: React.FC = () => {
  const position = useSelector((state: RootState) => state.map.position);
  const dispatch = useDispatch();

  // Default position if the position is not set in the Redux store
  const defaultPosition = { lat: 31.25, lng: 29.96 };

  const { isLoaded, loadError } = useJsApiLoader({
    googleMapsApiKey: 'AIzaSyAj97q6dp3zkYeI6RgBGcwOQUkAcDfvIyQ', // Replace with your actual API key
  });

  if (loadError) return <div>Error loading map</div>;
  if (!isLoaded) return <div>Loading Map...</div>;

  const handleDragEnd = (e: google.maps.MapMouseEvent) => {
    if (e.latLng) {
      dispatch(setPosition({
        lat: e.latLng.lat(),
        lng: e.latLng.lng(),
      }));
    }
  };

  return (
    <GoogleMap
      mapContainerStyle={containerStyle}
      center={position || defaultPosition} // Use default position if no position is set
      zoom={12}
    >
      {/* Render the main marker */}
      <Marker
        position={position || defaultPosition}
        draggable
        onDragEnd={handleDragEnd}
      />
      
      {/* Render the points on the map */}
      {points.map((point) => (
        <Marker
          key={point.ID}
          position={{ lat: point.lat, lng: point.lng }}
          label={point.Name} // Display the name of the point as the label
          title={point.Name} // Tooltip with the name when hovered
        />
      ))}
    </GoogleMap>
  );
};

export default MapContainer;
