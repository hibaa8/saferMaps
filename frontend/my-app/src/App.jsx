import './App.css';
import React, { useState, useEffect } from 'react';
import BgMap from './components/BgMap';
import SearchBar from './components/SearchBar';
import Directions from './components/Directions';
import logo from './assets/logo.png';
import BgMapJS from './components/BgMapJS';
import TestAPI from './components/TestAPI';

function App() {

  const [origin, setOrigin] = useState(null);
  const [destination, setDestination] = useState(null);
  const [responseData, setResponseData] = useState(null);

  const handleOriginSelect = (place) => {
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
          gap: '10px'
        }}
      >
        <SearchBar 
          fixed={false} 
          onPlaceSelected={handleOriginSelect} 
          placeholder="Enter origin"
        />
        <SearchBar 
          fixed={false} 
          onPlaceSelected={handleDestinationSelect} 
          placeholder="Enter destination"
        />

      </div>
      
      {/* Directions Panel: appears below the search bars after both are selected */}
      {origin && destination && (
        <div 
          style={{ 
            position: 'fixed', 
            top: '100px',  // Adjust to position below the search bars
            left: '10px', 
            zIndex: 100,
          }}
        >
          <Directions origin={origin} destination={destination} />
        </div>
      )}

      {/* Background Map Component */}
      <BgMap location={origin} />
      
      <img
        src={logo}  // Use the path of the image
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
  )
}

export default App;