import React, { useState, useEffect } from 'react';
import styled, { css } from 'styled-components';

// Container for the search bar; uses the fixed prop to decide positioning.
const SearchBarContainer = styled.div`
  ${(props) =>
    props.fixed
      ? css`
          position: fixed;
          /* These values are not used when placing in a container */
          top: 10px;
          left: 10px;
          width: 200px;
          background-color: #fff;
          padding: 10px;
          border-radius: 0;
          box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
          z-index: 1000;
        `
      : css`
          position: relative;
          width: 100%;
          background-color: #fff;
          padding: 10px;
          border-radius: 0;
          box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        `}
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

const SuggestionsContainer = styled.div`
  ${(props) =>
    props.fixed
      ? css`
          position: fixed;
          top: 80px; /* Adjust as needed */
          left: 10px;
          z-index: 10;
          background-color: #fff;
          border: 1px solid #ddd;
          width: 300px;
          max-height: 200px;
          overflow-y: auto;
        `
      : css`
          position: absolute;
          top: 100%;
          left: 0;
          z-index: 10;
          background-color: #fff;
          border: 1px solid #ddd;
          width: 100%;
          max-height: 200px;
          overflow-y: auto;
        `}
`;

const SuggestionItem = styled.div`
  padding: 10px;
  cursor: pointer;
  &:hover {
    background-color: #f2f2f2;
  }
`;

const SearchBar = ({ fixed, onPlaceSelected, placeholder }) => {
  const [location, setLocation] = useState('');
  const [suggestions, setSuggestions] = useState([]);
  const [autocompleteService, setAutocompleteService] = useState(null);

  // Initialize Google Maps AutocompleteService on mount.
  useEffect(() => {
    if (!autocompleteService && window.google && window.google.maps && window.google.maps.places) {
      const service = new window.google.maps.places.AutocompleteService();
      setAutocompleteService(service);
    }
  }, [autocompleteService]);

  const handleInputChange = (e) => {
    const inputValue = e.target.value;
    setLocation(inputValue);

    if (autocompleteService && inputValue) {
      autocompleteService.getPlacePredictions(
        { input: inputValue },
        (predictions, status) => {
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

  const handleSuggestionClick = (suggestion) => {
    setLocation(suggestion.description);
    setSuggestions([]);
    if (onPlaceSelected) {
      onPlaceSelected(suggestion.description);
    }
  };

  const handleSearch = () => {
    if (location) {
      console.log('Search triggered for:', location);
      setSuggestions([]);
    }
  };

  return (
    <div style={{ position: 'relative' }}>
      <SearchBarContainer fixed={fixed}>
        <SearchInput
          type="text"
          value={location}
          onChange={handleInputChange}
          onKeyDown={(e) => {
            if (e.key === 'Enter') {
              handleSearch();
            }
          }}
          placeholder={placeholder || "Search Safe Routes"}
        />
      </SearchBarContainer>
      {suggestions.length > 0 && (
        <SuggestionsContainer fixed={fixed}>
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
