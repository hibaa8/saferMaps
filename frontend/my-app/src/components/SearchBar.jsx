import React, { useState, useEffect } from 'react';
import styled from 'styled-components';

// Container for the search bar
const SearchBarContainer = styled.div`
  position: fixed;
  top: 10px;
  left: 10px;
  z-index: 10;
  display: flex;
  align-items: center;
  background-color: rgba(255, 255, 255, 1);
  padding: 10px;
  border-radius: 0px;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
`;

// Styled search input
const SearchInput = styled.input`
  width: 300px;
  padding: 5px;
  font-size: 16px;
  border: none;
  border-radius: 50px;
  outline: none;
  background-color: transparent;
  box-shadow: none;
  color: #333;
  
  &::placeholder {
    color: #aaa;
  }
  
  &:focus {
    border-color: #f2f2f2;
  }
`;

// Container for the suggestions dropdown
const SuggestionsContainer = styled.div`
  position: fixed;
  top: 80px; /* Adjust based on your layout */
  left: 10px;
  z-index: 10;
  background-color: #fff;
  border: 1px solid #ddd;
  width: 300px;
  max-height: 200px;
  overflow-y: auto;
`;

// Each suggestion item
const SuggestionItem = styled.div`
  padding: 10px;
  cursor: pointer;
  &:hover {
    background-color: #f2f2f2;
  }
`;

const SearchBar = () => {
  // State to hold the current input and suggestions
  const [location, setLocation] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [autocompleteService, setAutocompleteService] = useState(null);

  // On component mount, initialize the AutocompleteService from Google Maps
  useEffect(() => {
    if (!autocompleteService && window.google && window.google.maps && window.google.maps.places) {
      const service = new window.google.maps.places.AutocompleteService();
      setAutocompleteService(service);
    }
  }, [autocompleteService]);

  // Called every time the user types in the input
  const handleInputChange = (e) => {
    const inputValue = e.target.value;
    setLocation(inputValue);

    // If we have a value and the AutocompleteService is ready...
    if (autocompleteService && inputValue) {
      autocompleteService.getPlacePredictions(
        { input: inputValue },
        (predictions, status) => {
          // Check if the request was successful and predictions exist
          if (
            status === window.google.maps.places.PlacesServiceStatus.OK &&
            predictions
          ) {
            setSuggestions(predictions);
          } else {
            setSuggestions([]);
          }
        }
      );
    } else {
      setSuggestions([]);
    }
  };

  // When a suggestion is clicked, update the input and clear suggestions
  const handleSuggestionClick = (suggestion) => {
    setLocation(suggestion.description);
    setSuggestions([]);
    // Optionally, trigger further actions like an API search
  };

  // Optional: function to perform search when the user hits Enter
  const handleSearch = () => {
    if (location) {
      console.log('Search triggered for:', location);
      // Implement further search logic (e.g., fetching detailed place info)
      setSuggestions([]);
    }
  };

  return (
    <div style={{ position: 'relative' }}>
      <SearchBarContainer>
        <SearchInput
          type="text"
          value={location}
          onChange={handleInputChange}
          onKeyDown={(e) => {
            if (e.key === 'Enter') {
              handleSearch();
            }
          }}
          placeholder="Search Safe Routes"
        />
      </SearchBarContainer>

      {/* Render the suggestions dropdown if there are any suggestions */}
      {suggestions.length > 0 && (
        <SuggestionsContainer>
          {suggestions.map((suggestion) => (
            <SuggestionItem
              key={suggestion.place_id}
              onClick={() => handleSuggestionClick(suggestion)}
            >
              {suggestion.description}
            </SuggestionItem>
          ))}
        </SuggestionsContainer>
      )}
    </div>
  );
};

export default SearchBar;
