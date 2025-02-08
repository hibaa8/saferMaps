import { ContainerFilled } from '@ant-design/icons';
import React from 'react';
import styled from 'styled-components';
import SearchBar from './SearchBar';

const Container = styled.div`
  margin: 20px;
  position: relative;
  z-index: 10900;
  background-color: pink;
`;

const RouteOption = styled.div`
  background-color: #f1f3f4; // Light gray background for options
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 4px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);

  h3 {
    font-size: 18px;
    margin: 0 0 5px 0;
  }

  p {
    font-size: 14px;
    margin: 0;
  }
`;

const Directions = () => {

  return(
    <Container>
        <h1>Get Directions</h1>

        {/* Start and Destination Inputs */}
        <div>
            <SearchBar />
            Text: destination
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