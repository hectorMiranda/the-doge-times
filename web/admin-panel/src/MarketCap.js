
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const MarketCap = () => {
    const [marketCap, setMarketCap] = useState(null);
    const [error, setError] = useState('');

    useEffect(() => {
        axios.get('/marketCap')
            .then(response => {
                setMarketCap(response.data);
            })
            .catch(error => {
                setError('Error fetching market cap');
            });
    }, []);

    return (
        <div>
            <h2>Market Cap</h2>
            {marketCap ? <p>{JSON.stringify(marketCap)}</p> : <p>{error}</p>}
        </div>
    );
};

export default MarketCap;
