import React, { useState, useEffect, useRef } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import { cityData, facilityData, roadsData, busRoutes } from './cityData';
import PublicTransportIcon from '@mui/icons-material/Train';
import CarIcon from '@mui/icons-material/DirectionsCar';
import ToggleButton from '@mui/material/ToggleButton';
import ToggleButtonGroup from '@mui/material/ToggleButtonGroup';

const CityMap = () => {
  const [showAllBusRoutes, setShowAllBusRoutes] = useState(true);
  const [showMetroRoutes, setShowMetroRoutes] = useState(true);
  const [showNormalRoads, setShowNormalRoads] = useState(true);
  const [fromId, setFromId] = useState('');
  const [toId, setToId] = useState('');
  const [alignment, setAlignment] = useState('public_transport');
  
  // Use refs instead of state for Leaflet objects
  const mapRef = useRef(null);
  const markersRef = useRef([]);
  const routesRef = useRef([]);
  const busRoutesRef = useRef([]);
  const metroRoutesRef = useRef([]);
  const customRouteRef = useRef(null);

  // Combine cityData and facilityData for dropdown options
  const allLocations = [
    ...cityData.map(city => ({ id: city.id, name: city.name, type: 'City' })),
    ...facilityData.map(facility => ({ id: facility.id, name: facility.name, type: 'Facility' }))
  ];

  // Initialize map
  useEffect(() => {
    if (!mapRef.current) {
      const leafletMap = L.map('cityMap', {
        center: [30.033, 31.233], // Centered at Cairo
        zoom: 12,
        zoomControl: true,
      });
      
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(leafletMap);
      mapRef.current = leafletMap;
      
      cityData.forEach(city => {
        const marker = L.marker([city.lat, city.lon])
          .bindPopup(`<b>${city.name}</b><br>Type: ${city.type}<br>ID: ${city.id}`)
          .addTo(leafletMap);
        markersRef.current.push(marker);
      });
      
      facilityData.forEach(facility => {
        const marker = L.marker([facility.lat, facility.lon])
          .bindPopup(`<b>${facility.name}</b><br>Type: ${facility.type}<br>ID: ${facility.id}`)
          .addTo(leafletMap);
        markersRef.current.push(marker);
      });
    }
    
    return () => {
      if (mapRef.current) {
        mapRef.current.remove();
        mapRef.current = null;
      }
    };
  }, []); 

  useEffect(() => {
    const map = mapRef.current;
    if (!map) return;
    routesRef.current.forEach(route => route.remove());
    routesRef.current = [];
    if (showNormalRoads) {
      roadsData.forEach(route => {
        const start = cityData.find(c => String(c.id) === String(route.from)) || facilityData.find(f => String(f.id) === String(route.from));
        const end = cityData.find(c => String(c.id) === String(route.to)) || facilityData.find(f => String(f.id) === String(route.to));
        if (start && end) {
          const line = L.polyline([[start.lat, start.lon], [end.lat, end.lon]], { color: 'gray' }).addTo(map);
          routesRef.current.push(line);
        }
      });
    }
  }, [showNormalRoads]);

  useEffect(() => {
    const map = mapRef.current;
    if (!map) return;
    busRoutesRef.current.forEach(route => route.remove());
    busRoutesRef.current = [];
    if (showAllBusRoutes) {
      busRoutes.forEach(route => {
        if (route.id.startsWith('B')) {
          const path = route.stops.map(stopId => {
            const city = cityData.find(c => c.id === parseInt(stopId));
            const facility = facilityData.find(f => f.id === stopId);
            return city ? [city.lat, city.lon] : facility ? [facility.lat, facility.lon] : null;
          }).filter(Boolean);
          if (path.length >= 2) {
            const line = L.polyline(path, { color: 'green' }).addTo(map);
            busRoutesRef.current.push(line);
          }
        }
      });
    }
  }, [showAllBusRoutes]);

  useEffect(() => {
    const map = mapRef.current;
    if (!map) return;
    metroRoutesRef.current.forEach(route => route.remove());
    metroRoutesRef.current = [];
    if (showMetroRoutes) {
      busRoutes.forEach(route => {
        if (route.id.startsWith('M')) {
          const path = route.stops.map(stopId => {
            const city = cityData.find(c => c.id === parseInt(stopId));
            const facility = facilityData.find(f => f.id === stopId);
            return city ? [city.lat, city.lon] : facility ? [facility.lat, facility.lon] : null;
          }).filter(Boolean);
          if (path.length >= 2) {
            const line = L.polyline(path, { color: 'red' }).addTo(map);
            metroRoutesRef.current.push(line);
          }
        }
      });
    }
  }, [showMetroRoutes]);

  const drawCustomRoute = () => {
    const map = mapRef.current;
    if (!map) return;
    if (customRouteRef.current) {
      customRouteRef.current.remove();
      customRouteRef.current = null;
    }

    const findLocationById = (id) => {
      const numericId = parseInt(id, 10);
      const city = cityData.find(c => c.id === numericId || String(c.id) === id);
      if (city) return { lat: city.lat, lon: city.lon, name: city.name };
      const facility = facilityData.find(f => f.id === id || String(f.id) === id);
      if (facility) return { lat: facility.lat, lon: facility.lon, name: facility.name };
      return null;
    };

    const startLocation = findLocationById(fromId);
    const endLocation = findLocationById(toId);

    if (startLocation && endLocation) {
      customRouteRef.current = L.polyline([[startLocation.lat, startLocation.lon], [endLocation.lat, endLocation.lon]], {
        color: 'blue',
        weight: 4,
        opacity: 0.9,
        dashArray: '1'
      }).addTo(map);

      customRouteRef.current.bindPopup(
        `<b>Custom Route</b><br>From: ${startLocation.name}<br>To: ${endLocation.name}`
      );

      map.fitBounds(customRouteRef.current.getBounds(), { padding: [50, 50] });
    } else {
      alert('One or both location IDs were not found. Please check and try again.');
    }

    printInputsAndToggle();
  };

  const printInputsAndToggle = () => {
    const data = {
      fromId: fromId,
      toId: toId,
      transportationMode: alignment,
    };
    console.log(JSON.stringify(data, null, 2));
  };

  const handleChange = (event, newAlignment) => {
    if (newAlignment !== null) {
      setAlignment(newAlignment);
    }
  };

  return (
    <div>
      <div className="controls" style={{ position: 'absolute', top: '20px', left: '50%', transform: 'translateX(-50%)', zIndex: 1000, padding: '15px', backgroundColor: 'rgba(255, 255, 255, 0.6)', borderRadius: '8px', boxShadow: '0 4px 8px rgba(0, 0, 0, 0.2)', width: '800px'}}>
        <div style={{ marginBottom: '15px', display: 'flex', gap: '10px' }}>
          <button onClick={() => setShowAllBusRoutes(prev => !prev)} style={{ padding: '8px 16px', backgroundColor: '#4CAF50', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
            {showAllBusRoutes ? 'Hide Bus Routes' : 'Show Bus Routes'}
          </button>
          <button onClick={() => setShowMetroRoutes(prev => !prev)} style={{ padding: '8px 16px', backgroundColor: '#f44336', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
            {showMetroRoutes ? 'Hide Metro Routes' : 'Show Metro Routes'}
          </button>
          <button onClick={() => setShowNormalRoads(prev => !prev)} style={{ padding: '8px 16px', backgroundColor: '#9e9e9e', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}>
            {showNormalRoads ? 'Hide Normal Roads' : 'Show Normal Roads'}
          </button>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '15px', width: '600px' }}>
          <ToggleButtonGroup
            color="primary"
            value={alignment}
            exclusive
            onChange={handleChange}
            aria-label="Transportation mode"
            size="small"
          >
            <ToggleButton value="public_transport" aria-label="Public Transport">
              <PublicTransportIcon />
            </ToggleButton>
            <ToggleButton value="private_car" aria-label="Private Car">
              <CarIcon />
            </ToggleButton>
          </ToggleButtonGroup>

          <div>
            <label htmlFor="fromId" style={{ fontSize: '14px', fontWeight: '500' }}>From: </label>
            <select
              id="fromId"
              value={fromId}
              onChange={(e) => setFromId(e.target.value)}
              style={{ padding: '10px', width: '250px', borderRadius: '3px', border: '1px solid #ccc', fontSize: '14px' }}
            >
              <option value="">Select Starting Location</option>
              {allLocations.map(location => (
                <option key={location.id} value={location.id}>{location.name}</option>
              ))}
            </select>
          </div>

          <div>
            <label htmlFor="toId" style={{ fontSize: '14px', fontWeight: '500' }}>To: </label>
            <select
              id="toId"
              value={toId}
              onChange={(e) => setToId(e.target.value)}
              style={{ padding: '10px', width: '250px', borderRadius: '3px', border: '1px solid #ccc', fontSize: '14px' }}
            >
              <option value="">Select Destination</option>
              {allLocations.map(location => (
                <option key={location.id} value={location.id}>{location.name}</option>
              ))}
            </select>
          </div>
          
        <button
          onClick={drawCustomRoute}
          style={{ padding: '10px 60px', backgroundColor: '#007bff', color: 'white', border: 'none', borderRadius: '4px', cursor: 'pointer' }}
        >
          Draw Route
        </button>
        </div>

      </div>
      
      <div id="cityMap" style={{ height: '100vh', width: '100%' }}></div>
    </div>
  );
};

export default CityMap;
