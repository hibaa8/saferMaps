import React, { useState } from 'react'
import styled from 'styled-components';

const SearchBarContainer = styled.div`
  position: absolute;
  top: 40px;
  left: 10px;
  z-index: 10;
  display: flex;
  align-items: center;
  background-color: rgba(255, 255, 255, 1); /* Lighter, more subtle background */
  padding: 10px;
  border-radius: 0px; /* Rounded for a more Google-like feel */
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
`;

const SearchInput = styled.input`
  width: 300px;
  padding: 5px;
  font-size: 16px;
  border: none;
  border-radius: 50px; /* Match rounded edges of the Google Maps search box */
  outline: none;
  background-color: transparent; /* Clean background */
  box-shadow: none; /* Remove any shadow */
  color: #333;
  
  &::placeholder {
    color: #aaa; /* Slightly gray placeholder */
  }
  
  &:focus {
    border-color: #f2f2f2;
  }
`;

const SearchButton = styled.button`
  display: none; //keep it????
`;


const SearchBar = ({ onSearch }) => {
    const [location, setLocation] = useState('');

    const handleSearch = () => {
        if (location) {
          onSearch(location); // Call the onSearch function passed as a prop
          setLocation('');
        }
    };

    return (
        <SearchBarContainer>
            <SearchInput
                type="text"
                value={location}
                onChange={(e) => setLocation(e.target.value)}
                onKeyDown={(e) => {
                    if (e.key === 'Enter') {
                        handleSearch();
                    }
                }}
                placeholder="Search Safe Routes"
            />
            <SearchButton onClick={handleSearch}>Search</SearchButton>
        </SearchBarContainer>
    )
}

export default SearchBar