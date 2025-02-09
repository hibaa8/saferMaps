// ./components/BgMapRoutes.jsx
import React, { useState, useEffect } from 'react';
import { GoogleMap, Polyline, useLoadScript } from '@react-google-maps/api';

const containerStyle = {
  width: '100vw',
  height: '100vh',
};

const BgMapRoutes = ({ origin, destination }) => {
  const { isLoaded, loadError } = useLoadScript({
    googleMapsApiKey: VITE_GOOGLE_API_KEY, // Replace with your actual API key
    libraries: ['geometry'], // Load the geometry library to decode polylines
  });

  // Default center for the map
  const defaultCenter = { lat: 40.760, lng: -73.980 };
  // Center the map between origin and destination if available
  const center =
    origin && destination
      ? {
          lat: (origin.lat + destination.lat) / 2,
          lng: (origin.lng + destination.lng) / 2,
        }
      : defaultCenter;

  // State to store routes fetched from the backend
  const [routes, setRoutes] = useState([]);

  // When both origin and destination are provided, fetch route data from backend
  useEffect(() => {
    if (origin && destination) {
      // Post the origin and destination to your backend API
      fetch('/api/routes', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ origin, destination }),
      })
        .then((response) => response.json())
        .then((data) => {
          // Expecting data in the format: { routes: [ { encodedPolyline: '...' }, { encodedPolyline: '...' } ] }
          setRoutes(data.routes);
        })
        .catch((error) => console.error('Error fetching routes:', error));
    }
  }, [origin, destination]);

  if (loadError) return <div>Error loading Google Maps</div>;
  if (!isLoaded) return <div>Loading...</div>;

  return (
    <GoogleMap mapContainerStyle={containerStyle} center={center} zoom={13}>
      {routes.map((route, index) => {
        // Decode the encoded polyline using the Google Maps geometry library
        const decodedPath = window.google.maps.geometry.encoding.decodePath(
          route.encodedPolyline
        );
        // Convert the decoded path to an array of simple {lat, lng} objects
        const path = decodedPath.map((latLng) => ({
          lat: latLng.lat(),
          lng: latLng.lng(),
        }));
        // Choose a color based on the index: first route gets #8B0000, second gets #FF7F7F
        const color = index === 0 ? '#8B0000' : '#FF7F7F';

        return (
          <Polyline
            key={index}
            path={path}
            options={{
              strokeColor: color,
              strokeOpacity: 1.0,
              strokeWeight: 4,
            }}
          />
        );
      })}
    </GoogleMap>
  );
};

export default BgMapRoutes;
