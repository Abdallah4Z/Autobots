const sendRouteRequest = async () => {
    const response = await fetch('http://localhost:5000/api/routes', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        from: '21',
        to: 'F4',
        type: 'public', // or 'private'
      }),
    });
  
    const data = await response.json();
    console.log('Received nodes:', data.nodes);
  };
  