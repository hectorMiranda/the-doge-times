
import React, { useState, useEffect } from 'react';
import axios from 'axios';

const CurrentPrice = () => {
    const [currentPrice, setCurrentPrice] = useState(null);
    const [error, setError] = useState('');

    useEffect(() => {
        axios.get('/currentPrice')
            .then(response => {
                setCurrentPrice(response.data);
            })
            .catch(error => {
                setError('Error fetching current price');
            });
    }, []);

    return (
        <div>
            <h2>Current Price</h2>
            {currentPrice ? <p>{JSON.stringify(currentPrice)}</p> : <p>{error}</p>}
        </div>
    );
};

export default CurrentPrice;
