// ./components/BgMapRoutes.jsx
import React, { useState, useEffect } from 'react';
import { GoogleMap, Polyline, useLoadScript } from '@react-google-maps/api';

const containerStyle = {
  position: 'absolute',
  width: '100vw',
  height: '100vh',
  top: 0,
  left: 0,

};

const BgMapRoutes = ({ origin, destination }) => {
  const { isLoaded, loadError } = useLoadScript({
    googleMapsApiKey: import.meta.env.VITE_GOOGLE_API_KEY,
    libraries: ['geometry'], // For decoding polylines
  });

  // Default center if no coordinates are provided
  const defaultCenter = { lat: 40.760, lng: -73.980 };
  const center =
    origin && destination && origin.lat && destination.lat
      ? {
          lat: (origin.lat + destination.lat) / 2,
          lng: (origin.lng + destination.lng) / 2,
        }
      : defaultCenter;

  // State to store routes fetched from the backend
  const [routes, setRoutes] = useState([]);

  // Fetch route data when origin and destination are available
  useEffect(() => {
    if (origin && destination) {
      fetch('http://127.0.0.1:5000/get_routes', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ origin, destination }),
      })
        .then((response) => response.json())
        .then((data) => {
          if (data.error) {
            console.error('Backend error:', data.error);
          } else if (data.routes) {
            console.log('Routes received:', data.routes);
            // Pick the first two routes
            setRoutes(data.routes.slice(0, 2));
          }
        })
        .catch((error) => console.error('Error fetching routes:', error));
    }
  }, [origin, destination]);

  if (loadError) return <div>Error loading Google Maps</div>;
  if (!isLoaded) return <div>Loading...</div>;

  return (
    <GoogleMap mapContainerStyle={containerStyle} center={center} zoom={13}>
      {routes.map((route, index) => {
        // Try to use the route-level polyline first.
        // If not available, fall back to the first leg's polyline.
        const encodedPolyline =
          (route.polyline && route.polyline.encodedPolyline) ||
          (route.legs &&
            route.legs[0] &&
            route.legs[0].polyline &&
            route.legs[0].polyline.encodedPolyline);

        if (!encodedPolyline) {
          console.warn(`No encoded polyline found for route index ${index}`);
          return null;
        }

        // Decode the polyline using Google Maps geometry library
        const decodedPath = window.google.maps.geometry.encoding.decodePath(encodedPolyline);
        const path = decodedPath.map((latLng) => ({
          lat: latLng.lat(),
          lng: latLng.lng(),
        }));
        // Choose color: first route gets #8B0000, second gets #FF7F7F
        const color = index === 0 ? '#8B0000' : '#D2042D';

        return (
          <Polyline
            key={index}
            path={path}
            options={{
              strokeColor: color,
              strokeOpacity: 1.0,
              strokeWeight: 6,
            }}
          />
        );
      })}
    </GoogleMap>
  );
};

export default BgMapRoutes;
