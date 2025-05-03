import React, { useState } from 'react';
import { Box, Button, TextField, Typography, Paper, Select, MenuItem, FormControl, InputLabel } from '@mui/material';
import { testRouteApi } from '../services/debugApi';

/**
 * A simple component to test and debug API endpoints
 */
const ApiDebugger: React.FC = () => {
  const [origin, setOrigin] = useState('1');
  const [destination, setDestination] = useState('2');
  const [results, setResults] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const handleTest = async () => {
    setLoading(true);
    try {
      const apiResults = await testRouteApi(origin, destination);
      setResults(apiResults);
      console.log('API test results:', apiResults);
    } catch (error) {
      console.error('Error testing API:', error);
      setResults({ error: String(error) });
    } finally {
      setLoading(false);
    }
  };

  const extractJsonFromResponse = () => {
    try {
      // Try to get any JSON-like content from the response
      if (results?.jsonFetch?.text) {
        const text = results.jsonFetch.text;
        
        // Look for anything that looks like JSON
        const jsonMatch = text.match(/\{.*\}/s);
        if (jsonMatch && jsonMatch[0]) {
          const jsonContent = jsonMatch[0];
          console.log('Extracted JSON content:', jsonContent);
          
          try {
            const parsedJson = JSON.parse(jsonContent);
            console.log('Successfully parsed extracted JSON:', parsedJson);
            setResults({
              ...results,
              extractedJson: {
                raw: jsonContent,
                parsed: parsedJson
              }
            });
            return;
          } catch (e) {
            console.error('Failed to parse extracted content as JSON:', e);
          }
        }
      }
      
      alert('Could not extract valid JSON from the response.');
    } catch (error) {
      console.error('Error extracting JSON:', error);
      alert(`Error extracting JSON: ${error}`);
    }
  };

  return (
    <Paper sx={{ p: 3, m: 2, maxWidth: '800px', mx: 'auto' }}>
      <Typography variant="h5" gutterBottom>API Debugger</Typography>
      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
        Use this tool to test the route API and see the raw response
      </Typography>

      <Box sx={{ mb: 2 }}>
        <FormControl fullWidth sx={{ mb: 2 }}>
          <InputLabel>Origin</InputLabel>
          <Select
            value={origin}
            label="Origin"
            onChange={(e) => setOrigin(e.target.value)}
          >
            {Array.from({ length: 15 }, (_, i) => i + 1).map(num => (
              <MenuItem key={num} value={String(num)}>{num} (District)</MenuItem>
            ))}
            {Array.from({ length: 10 }, (_, i) => i + 1).map(num => (
              <MenuItem key={`F${num}`} value={`F${num}`}>F{num} (Facility)</MenuItem>
            ))}
          </Select>
        </FormControl>

        <FormControl fullWidth sx={{ mb: 2 }}>
          <InputLabel>Destination</InputLabel>
          <Select
            value={destination}
            label="Destination"
            onChange={(e) => setDestination(e.target.value)}
          >
            {Array.from({ length: 15 }, (_, i) => i + 1).map(num => (
              <MenuItem key={num} value={String(num)}>{num} (District)</MenuItem>
            ))}
            {Array.from({ length: 10 }, (_, i) => i + 1).map(num => (
              <MenuItem key={`F${num}`} value={`F${num}`}>F{num} (Facility)</MenuItem>
            ))}
          </Select>
        </FormControl>
      </Box>

      <Box sx={{ display: 'flex', gap: 2, mb: 3 }}>
        <Button 
          variant="contained" 
          onClick={handleTest}
          disabled={loading}
        >
          {loading ? 'Testing...' : 'Test API'}
        </Button>
        
        <Button 
          variant="outlined"
          onClick={extractJsonFromResponse}
          disabled={!results || loading}
        >
          Extract JSON
        </Button>
      </Box>

      {results && (
        <Box sx={{ mt: 3 }}>
          <Typography variant="h6">Test Results:</Typography>
          
          {results.extractedJson && (
            <Box sx={{ mb: 2, p: 2, bgcolor: '#f5f5f5', borderRadius: 1 }}>
              <Typography variant="subtitle1" color="primary">Extracted JSON:</Typography>
              <pre style={{ whiteSpace: 'pre-wrap', wordBreak: 'break-word' }}>
                {JSON.stringify(results.extractedJson.parsed, null, 2)}
              </pre>
            </Box>
          )}

          <Typography variant="subtitle2">Response Headers:</Typography>
          <Box sx={{ mb: 2, p: 1, bgcolor: '#f5f5f5', borderRadius: 1, maxHeight: '200px', overflow: 'auto' }}>
            <pre style={{ fontSize: '0.8rem' }}>
              {JSON.stringify(results.jsonFetch?.headers || {}, null, 2)}
            </pre>
          </Box>

          <Typography variant="subtitle2">Response Preview:</Typography>
          <Box sx={{ mb: 2, p: 1, bgcolor: '#f5f5f5', borderRadius: 1, maxHeight: '200px', overflow: 'auto' }}>
            <pre style={{ fontSize: '0.8rem' }}>
              {results.jsonFetch?.preview || 'No preview available'}
            </pre>
          </Box>

          <Typography variant="subtitle2" color={results.jsonFetch?.isHtml ? 'error' : 'success'}>
            Content Type: {results.jsonFetch?.contentType || 'unknown'} 
            {results.jsonFetch?.isHtml ? ' (HTML detected)' : ''}
          </Typography>
        </Box>
      )}
    </Paper>
  );
};

export default ApiDebugger;