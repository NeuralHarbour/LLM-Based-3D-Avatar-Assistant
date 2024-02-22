import React from 'react';
import styled from "styled-components";

function Title({ value }) {
    return (
        <Div>
            <h1>{value}</h1>
        </Div>
    );
}

const Div = styled.div`
position: relative;
h1 {
  position: absolute;
  transform: translateX(-30%) translateY(20vw) rotate(-90deg);
  font-size: 7rem;
  text-transform: uppercase;
  color: var(--secondary-color);
  font-weight: 400;
  @media screen and (min-width: 280px) and (max-width: 1080px) {
    display: none;
  }
}
`;

export default Title