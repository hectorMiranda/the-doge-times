import React from 'react';
import Countdown from 'react-countdown';
import styled from 'styled-components';

// Styles
const ComingSoonContainer = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background-color: #f5f5f5;
  font-family: 'Arial', sans-serif;
`;

const Title = styled.h1`
  color: #333;
  font-size: 48px;
  margin-bottom: 20px;
`;

const CountdownStyle = styled.div`
  font-size: 32px;
  color: #ff4500;
  margin-bottom: 30px;
`;

const Message = styled.p`
  color: #555;
  font-size: 24px;
`;

// Renderer for countdown
const CountdownRenderer = ({ days, hours, minutes, seconds, completed }) => {
  if (completed) {
    return <Message>Welcome to The Doge Times!</Message>;
  } else {
    return (
      <CountdownStyle>
        {days} days {hours} hours {minutes} minutes {seconds} seconds
      </CountdownStyle>
    );
  }
};

function App() {
  // Set your expected launch date here
  const launchDate = new Date('2024-04-20:00:00');

  return (
    <ComingSoonContainer>
      <Title>The Doge Times</Title>
      <Countdown date={launchDate} renderer={CountdownRenderer} />
      <Message>Something exciting is coming soon...</Message>
    </ComingSoonContainer>
  );
}

export default App;
