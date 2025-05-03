/**
 * Debugging utility to test API endpoints directly
 */

/**
 * Tests the route API and returns detailed debugging information
 * @param origin The origin node ID
 * @param destination The destination node ID 
 * @returns A promise with detailed debug info
 */
export const testRouteApi = async (origin: string, destination: string) => {
  try {
    // Check if we're in a browser environment
    if (typeof window === 'undefined') {
      return { error: 'This function must run in browser environment' };
    }
    
    console.log('Testing route API with:', { origin, destination });
    
    // Test URL (adding a timestamp to prevent caching)
    const url = `/api/flow/route/astar?origin=${encodeURIComponent(origin)}&dest=${encodeURIComponent(destination)}&_=${Date.now()}`;
    
    // Test using various approaches
    const results = {
      standardFetch: null as any,
      jsonFetch: null as any,
      xmlHttpRequest: null as any,
      diagnostics: {
        url,
        userAgent: navigator.userAgent,
        date: new Date().toISOString(),
      }
    };
    
    // 1. Standard fetch
    try {
      const response = await fetch(url);
      const contentType = response.headers.get('content-type');
      const responseText = await response.text();
      
      results.standardFetch = {
        status: response.status,
        statusText: response.statusText,
        contentType,
        responseLength: responseText.length,
        isHtml: responseText.includes('<!DOCTYPE') || responseText.includes('<html'),
        isJson: contentType?.includes('application/json'),
        headers: Object.fromEntries([...response.headers]),
        preview: responseText.substring(0, 200) + '...',
        text: responseText,
      };
      
      if (!results.standardFetch.isHtml) {
        try {
          results.standardFetch.parsedJson = JSON.parse(responseText);
        } catch (e) {
          results.standardFetch.jsonParseError = String(e);
        }
      }
    } catch (error) {
      results.standardFetch = { error: String(error) };
    }
    
    // 2. Fetch with explicit JSON headers
    try {
      const response = await fetch(url, {
        method: 'GET',
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json',
        }
      });
      const contentType = response.headers.get('content-type');
      const responseText = await response.text();
      
      results.jsonFetch = {
        status: response.status,
        statusText: response.statusText,
        contentType,
        responseLength: responseText.length,
        isHtml: responseText.includes('<!DOCTYPE') || responseText.includes('<html'),
        isJson: contentType?.includes('application/json'),
        headers: Object.fromEntries([...response.headers]),
        preview: responseText.substring(0, 200) + '...',
        text: responseText,
      };
      
      if (!results.jsonFetch.isHtml) {
        try {
          results.jsonFetch.parsedJson = JSON.parse(responseText);
        } catch (e) {
          results.jsonFetch.jsonParseError = String(e);
        }
      }
    } catch (error) {
      results.jsonFetch = { error: String(error) };
    }
    
    // 3. Using XMLHttpRequest for comparison
    try {
      const xhr = new XMLHttpRequest();
      xhr.open('GET', url, false); // Synchronous for simplicity in this test function
      xhr.setRequestHeader('Accept', 'application/json');
      xhr.send(null);
      
      const responseText = xhr.responseText;
      
      results.xmlHttpRequest = {
        status: xhr.status,
        statusText: xhr.statusText,
        contentType: xhr.getResponseHeader('Content-Type'),
        responseLength: responseText.length,
        isHtml: responseText.includes('<!DOCTYPE') || responseText.includes('<html'),
        isJson: xhr.getResponseHeader('Content-Type')?.includes('application/json'),
        headers: parseXhrHeaders(xhr),
        preview: responseText.substring(0, 200) + '...',
        text: responseText,
      };
      
      if (!results.xmlHttpRequest.isHtml) {
        try {
          results.xmlHttpRequest.parsedJson = JSON.parse(responseText);
        } catch (e) {
          results.xmlHttpRequest.jsonParseError = String(e);
        }
      }
    } catch (error) {
      results.xmlHttpRequest = { error: String(error) };
    }
    
    console.log('API Test Results:', results);
    return results;
  } catch (error) {
    console.error('Error in testRouteApi:', error);
    return { error: String(error) };
  }
};

// Helper function to parse XHR headers
function parseXhrHeaders(xhr: XMLHttpRequest): Record<string, string> {
  const headerString = xhr.getAllResponseHeaders();
  const headerLines = headerString.split('\r\n');
  const headers: Record<string, string> = {};
  
  for (const line of headerLines) {
    if (line) {
      const parts = line.split(': ');
      const key = parts[0];
      const value = parts.slice(1).join(': ');
      headers[key] = value;
    }
  }
  
  return headers;
}