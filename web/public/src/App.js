import React from 'react';
import Countdown from 'react-countdown';

// Renderer for countdown
const CountdownRenderer = ({ days, hours, minutes, seconds, completed }) => {
  if (completed) {
    return <div className="Message">Welcome to The Doge Times!</div>;
  } else {
    return (
      <div className="CountdownStyle">
        {days} days {hours} hours {minutes} minutes {seconds} seconds
      </div>
    );
  }
};

function App() {
  // Set your expected launch date here
  const launchDate = new Date('2024-04-20:00:00');

  return (
    <div className="ComingSoonContainer">
      <img src="/thedogetimes.png" alt="The Doge Times Logo" />
      <div className="Message">Something exciting is coming soon...</div>

      <Countdown date={launchDate} renderer={CountdownRenderer} />
      <p></p>
    </div>
  );
}

export default App;
