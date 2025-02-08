import './App.css';
import React, { useState } from 'react';
import BgMap from './components/BgMap';
import SearchBar from './components/SearchBar';

function App() {

  const [location, setLocation] = useState(null);

  const handleSearch = (searchTerm) => {
    // Handle search logic here. You can update state or perform actions.
    console.log('Search for:', searchTerm);
    // For example, setting the location to the new search term
    setLocation(searchTerm);
  };

  return (
    <div className="w-full">
      <BgMap location={location}/>
      <SearchBar onSearch={handleSearch} />
    </div>
  )
}

export default App;