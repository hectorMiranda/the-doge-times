
import React from 'react';
import CurrentPrice from './CurrentPrice';
import MarketCap from './MarketCap';

const App = () => {
    return (
        <div className="App">
            <h1>DogeDataHub Control Panel</h1>
            <CurrentPrice />
            <MarketCap />
            {/* Other components here */}
        </div>
    );
}

export default App;
