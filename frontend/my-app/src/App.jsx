// App.jsx
import './App.css';
import React, { useState, useEffect } from 'react';
import SearchBar from './components/SearchBar';
import Directions from './components/Directions';
import logo from './assets/logo.png';
import BgMapRoutes from './components/BgMapRoutes';

function App() {
  const [origin, setOrigin] = useState(null);
  const [destination, setDestination] = useState(null);
  const [responseData, setResponseData] = useState(null);
  const [routes, setRoutes] = useState([]);

  const handleOriginSelect = (place) => {
    // Expecting 'place' to be an object like: { lat: 40.7128, lng: -74.0060 }
    setOrigin(place);
  };

  const handleDestinationSelect = (place) => {
    setDestination(place);
  };

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
          <Directions routeData={routes} />
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

      {/* "Powered by Groq" Link */}
      <a href="https://groq.com" target="_blank" rel="noopener noreferrer" 
         style={{
           position: 'absolute',
           top: '75px',
           width: '70px',
           height: 'auto',
           right: '20px',
           display: 'flex',
           alignItems: 'center',
           gap: '8px',
         }}
      >
        <img
          src="https://groq.com/wp-content/uploads/2024/03/PBG-mark1-color.svg"
          alt="Powered by Groq for fast inference."
          style={{
            width: '120px',
            height: 'auto',
          }}
        />
      </a>

    </div>
  );
}

export default App;