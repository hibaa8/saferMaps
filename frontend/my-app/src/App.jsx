// App.jsx
import './App.css';
import React, { useState } from 'react';
import SearchBar from './components/SearchBar';
import Directions from './components/Directions';
import logo from './assets/logo.png';
import BgMapRoutes from './components/BgMapRoutes';

function App() {
  const [origin, setOrigin] = useState(null);
  const [destination, setDestination] = useState(null);
  const [responseData, setResponseData] = useState(null);

  const handleOriginSelect = (place) => {
    // Expecting 'place' to be an object like: { lat: 40.7128, lng: -74.0060 }
    setOrigin(place);
  };

  const handleDestinationSelect = (place) => {
    setDestination(place);
  };

  useEffect(() => {
    // Send request to backend when both origin and destination are selected
    if (origin && destination) {
      const fetchData = async () => {
        try {
          const response = await fetch('http://127.0.0.1:5000/get_routes', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              origin: origin,
              destination: destination,
            }),
          });

          if (!response.ok) {
            throw new Error('Error fetching data');
          }

          const data = await response.json();
          console.log('Route data:', data);
          setResponseData(data);
        } catch (error) {
          console.error('Error:', error);
        }
      };

      fetchData();
    }
  }, [origin, destination]);

  return (
    <div>
      {/* Container for the two search bars */}
      <div
        style={{
          position: 'fixed',
          top: '10px',
          left: '10px',
          zIndex: 1000,
          display: 'flex',
          flexDirection: 'column',
          gap: '10px',
        }}
      >
        <SearchBar onPlaceSelected={handleOriginSelect} placeholder="Enter origin" />
        <SearchBar onPlaceSelected={handleDestinationSelect} placeholder="Enter destination" />
      </div>

      {/* Directions Panel (if needed) */}
      {origin && destination && (
        <div
          style={{
            position: 'fixed',
            top: '100px', // Adjust as needed
            left: '10px',
            zIndex: 100,
          }}
        >
          <Directions origin={origin} destination={destination} />
        </div>
      )}

      {/* Background Map with Routes */}
       <BgMapRoutes origin={origin} destination={destination} /> 

      <img
        src={logo}
        alt="Top Right Logo"
        style={{
          position: 'absolute',
          top: '20px',
          right: '20px',
          width: '200px',
          height: 'auto',
        }}
      />
    </div>
  );
}

export default App;