import { ContainerFilled } from '@ant-design/icons';
import React from 'react';
import styled from 'styled-components';
import SearchBar from './SearchBar';

const Container = styled.div`
    position: absolute;
    top: 92px;
    left: 10px;
    width: 420px;
    background-color: white;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    z-index: 100;
`;

const Destination = styled.div`
    width: 100%;
    padding: 10px;
    margin-bottom: 15px;
    font-size: 16px;
    color: #333;
`;


const RouteOption = styled.div`
  padding: 10px;
  margin-bottom: 10px; 
  color: #333;
  text-align: left; 

  h3 {
    font-size: 18px;
    margin: 0 0 5px 0;
  }

  p {
    font-size: 14px;
    margin: 0;
  }
`;

const Directions = ({ origin }) => {
  // Handler for destination selection in the second SearchBar
  const handleDestinationSelect = (place) => {
    console.log('Destination selected: ', place);
    // Additional logic for destination can be added here.
  };

  return(
    <Container>
        {/* Start and Destination Inputs */}
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center'}}>
            <div style={{ display: 'flex', justifyContent: 'center'  }}>
              <SearchBar fixed={false} style={{ width: '28%' }} onPlaceSelected={handleDestinationSelect} />
            </div>
            <br />
            <br />
            <br />
            <Destination>
                Text: destination
            </Destination>
        </div>

        <button>
          Get Directions
        </button>

        {/* Route Options Placeholder */}
        <div>
            <RouteOption>
                <h3>Route 1</h3>
                <p>Duration: N/A</p>
                <p>Distance: N/A</p>
            </RouteOption>
            <RouteOption>
                <h3>Route 2</h3>
                <p>Duration: N/A</p>
                <p>Distance: N/A</p>
            </RouteOption>
        </div>
    </Container>
  );
};

export default Directions;