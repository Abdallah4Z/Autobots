// Types for our map data
export interface CityNode {
    id: number | string;
    name: string;
    population?: number;
    type: string;
    lat: number;
    lng: number;
    description?: string;
  }
  
  export interface Road {
    id: string;
    from: number | string;
    to: number | string;
    type: 'normal' | 'highway' | 'bridge';
    condition?: 'good' | 'fair' | 'poor';
  }
  
  export interface TransportRoute {
    id: string;
    name: string;
    type: 'bus' | 'metro' | 'tram';
    color: string;
    stops: Array<number | string>;
    frequency?: string;
    operatingHours?: string;
  }
  
  // City districts/neighborhoods data
  export const cityData: CityNode[] = [
    { id: 1, name: "Maadi", population: 250000, type: "Residential", lat: 29.96, lng: 31.25, description: "Affluent residential district with many international schools and embassies" },
    { id: 2, name: "Nasr City", population: 500000, type: "Mixed", lat: 30.06, lng: 31.34, description: "Large district with residential areas and commercial centers" },
    { id: 3, name: "Downtown Cairo", population: 100000, type: "Business", lat: 30.04, lng: 31.24, description: "Historic center of Cairo with government buildings and business district" },
    { id: 4, name: "New Cairo", population: 300000, type: "Residential", lat: 30.03, lng: 31.47, description: "Modern suburban area with upscale residential compounds" },
    { id: 5, name: "Heliopolis", population: 200000, type: "Mixed", lat: 30.09, lng: 31.32, description: "Historic district with distinctive architecture and commercial areas" },
    { id: 6, name: "Zamalek", population: 50000, type: "Residential", lat: 30.06, lng: 31.22, description: "Upscale island district with diplomatic missions and cultural centers" },
    { id: 7, name: "6th October City", population: 400000, type: "Mixed", lat: 29.93, lng: 30.98, description: "Satellite city with industrial zones and residential areas" },
    { id: 8, name: "Giza", population: 550000, type: "Mixed", lat: 29.99, lng: 31.21, description: "Major urban area known for the Pyramids and ancient monuments" },
    { id: 9, name: "Mohandessin", population: 180000, type: "Business", lat: 30.05, lng: 31.2, description: "Upscale commercial district with offices and shopping areas" },
    { id: 10, name: "Dokki", population: 220000, type: "Mixed", lat: 30.03, lng: 31.21, description: "Central district with universities and government institutions" },
    { id: 11, name: "Shubra", population: 450000, type: "Residential", lat: 30.11, lng: 31.24, description: "Densely populated residential area with vibrant street life" },
    { id: 12, name: "Helwan", population: 350000, type: "Industrial", lat: 29.85, lng: 31.33, description: "Industrial suburb with factories and working-class neighborhoods" },
    { id: 13, name: "New Administrative Capital", population: 50000, type: "Government", lat: 30.02, lng: 31.8, description: "New planned capital city under development" },
    { id: 14, name: "Al Rehab", population: 120000, type: "Residential", lat: 30.06, lng: 31.49, description: "Planned residential community with green spaces" },
    { id: 15, name: "Sheikh Zayed", population: 150000, type: "Residential", lat: 30.01, lng: 30.94, description: "Modern residential city with upscale compounds" }
  ];
  
  // Important facilities data
  export const facilityData: CityNode[] = [
    { id: "F1", name: "Cairo International Airport", type: "Airport", lat: 30.11, lng: 31.41, description: "Main international airport serving Cairo and Egypt" },
    { id: "F2", name: "Ramses Railway Station", type: "Transit Hub", lat: 30.06, lng: 31.25, description: "Main railway station connecting Cairo to other Egyptian cities" },
    { id: "F3", name: "Cairo University", type: "Education", lat: 30.03, lng: 31.21, description: "One of Egypt's oldest and most prestigious universities" },
    { id: "F4", name: "Al-Azhar University", type: "Education", lat: 30.05, lng: 31.26, description: "Historic Islamic university founded in 970 CE" },
    { id: "F5", name: "Egyptian Museum", type: "Tourism", lat: 30.05, lng: 31.23, description: "Home to an extensive collection of ancient Egyptian artifacts" },
    { id: "F6", name: "Cairo International Stadium", type: "Sports", lat: 30.07, lng: 31.3, description: "Multi-purpose stadium and Egypt's main sporting venue" },
    { id: "F7", name: "Smart Village", type: "Business", lat: 30.07, lng: 30.97, description: "Technology and business park housing multinational companies" },
    { id: "F8", name: "Cairo Festival City", type: "Commercial", lat: 30.03, lng: 31.4, description: "Large shopping mall and mixed-use development" },
    { id: "F9", name: "Qasr El Aini Hospital", type: "Medical", lat: 30.03, lng: 31.23, description: "Major teaching hospital affiliated with Cairo University" },
    { id: "F10", name: "Maadi Military Hospital", type: "Medical", lat: 29.95, lng: 31.25, description: "Specialized military medical facility" },
    { id: "F11", name: "Grand Egyptian Museum", type: "Tourism", lat: 29.99, lng: 31.13, description: "New museum complex near the Giza Pyramids" },
    { id: "F12", name: "Citadel of Saladin", type: "Tourism", lat: 30.03, lng: 31.26, description: "Medieval Islamic fortification and historic site" },
    { id: "F13", name: "Al-Azhar Park", type: "Recreation", lat: 30.04, lng: 31.27, description: "Large urban park with gardens and historic views" },
    { id: "F14", name: "American University in Cairo", type: "Education", lat: 30.02, lng: 31.5, description: "Private English-language university" },
    { id: "F15", name: "Mall of Egypt", type: "Commercial", lat: 29.97, lng: 31.02, description: "Major shopping and entertainment complex" }
  ];
  
  // Road network data
  export const roadsData: Road[] = [
    { id: "R1", from: 1, to: 3, type: "normal", condition: "good" },
    { id: "R2", from: 1, to: 8, type: "normal", condition: "fair" },
    { id: "R3", from: 2, to: 3, type: "normal", condition: "good" },
    { id: "R4", from: 2, to: 5, type: "highway", condition: "good" },
    { id: "R5", from: 3, to: 5, type: "normal", condition: "fair" },
    { id: "R6", from: 3, to: 6, type: "bridge", condition: "good" },
    { id: "R7", from: 3, to: 9, type: "normal", condition: "good" },
    { id: "R8", from: 3, to: 10, type: "normal", condition: "good" },
    { id: "R9", from: 4, to: 2, type: "highway", condition: "good" },
    { id: "R10", from: 4, to: 14, type: "normal", condition: "good" },
    { id: "R11", from: 5, to: 11, type: "normal", condition: "fair" },
    { id: "R12", from: 6, to: 9, type: "bridge", condition: "good" },
    { id: "R13", from: 7, to: 8, type: "highway", condition: "good" },
    { id: "R14", from: 7, to: 15, type: "normal", condition: "good" },
    { id: "R15", from: 8, to: 10, type: "normal", condition: "poor" },
    { id: "R16", from: 8, to: 12, type: "highway", condition: "fair" },
    { id: "R17", from: 9, to: 10, type: "normal", condition: "good" },
    { id: "R18", from: 10, to: 11, type: "normal", condition: "fair" },
    { id: "R19", from: 11, to: "F2", type: "normal", condition: "fair" },
    { id: "R20", from: 12, to: 1, type: "highway", condition: "good" },
    { id: "R21", from: 13, to: 4, type: "highway", condition: "good" },
    { id: "R22", from: 14, to: 13, type: "highway", condition: "good" },
    { id: "R23", from: 15, to: 7, type: "normal", condition: "good" },
    { id: "R24", from: "F1", to: 5, type: "highway", condition: "good" },
    { id: "R25", from: "F1", to: 2, type: "highway", condition: "good" },
    { id: "R26", from: "F2", to: 3, type: "normal", condition: "fair" },
    { id: "R27", from: "F7", to: 15, type: "normal", condition: "good" },
    { id: "R28", from: "F8", to: 4, type: "normal", condition: "good" },
    { id: "R29", from: 8, to: "F11", type: "normal", condition: "good" },
    { id: "R30", from: 3, to: "F12", type: "normal", condition: "fair" },
    { id: "R31", from: 5, to: "F13", type: "normal", condition: "good" },
    { id: "R32", from: 4, to: "F14", type: "normal", condition: "good" },
    { id: "R33", from: 7, to: "F15", type: "highway", condition: "good" }
  ];
  
  // Public transportation routes
  export const transportRoutes: TransportRoute[] = [
    { 
      id: "B1", 
      name: "Central Line", 
      type: "bus", 
      color: "#0288d1", 
      stops: [1, 3, 6, 9],
      frequency: "Every 15 minutes",
      operatingHours: "6:00 AM - 11:00 PM"
    },
    { 
      id: "B2", 
      name: "Western Circuit", 
      type: "bus", 
      color: "#2e7d32", 
      stops: [7, 15, 8, 10, 3],
      frequency: "Every 20 minutes",
      operatingHours: "6:30 AM - 10:30 PM"
    },
    { 
      id: "B3", 
      name: "Airport Express", 
      type: "bus", 
      color: "#1565c0", 
      stops: [2, 5, "F1"],
      frequency: "Every 30 minutes",
      operatingHours: "5:00 AM - 1:00 AM"
    },
    { 
      id: "B4", 
      name: "Eastern Line", 
      type: "bus", 
      color: "#d32f2f", 
      stops: [4, 14, 2, 3],
      frequency: "Every 15 minutes",
      operatingHours: "6:00 AM - 11:00 PM"
    },
    { 
      id: "B5", 
      name: "Southern Route", 
      type: "bus", 
      color: "#f57c00", 
      stops: [8, 12, 1],
      frequency: "Every 25 minutes",
      operatingHours: "6:30 AM - 10:00 PM"
    },
    { 
      id: "B6", 
      name: "Northern Circuit", 
      type: "bus", 
      color: "#7b1fa2", 
      stops: [11, 5, 2],
      frequency: "Every 20 minutes",
      operatingHours: "6:00 AM - 11:30 PM"
    },
    { 
      id: "B7", 
      name: "New Capital Link", 
      type: "bus", 
      color: "#00796b", 
      stops: [13, 4, 14],
      frequency: "Every 40 minutes",
      operatingHours: "7:00 AM - 9:00 PM"
    },
    { 
      id: "B8", 
      name: "Technology Line", 
      type: "bus", 
      color: "#004d40", 
      stops: ["F7", 15, 7],
      frequency: "Every 30 minutes",
      operatingHours: "7:00 AM - 8:00 PM"
    },
    { 
      id: "B9", 
      name: "Central Loop", 
      type: "bus", 
      color: "#880e4f", 
      stops: [1, 8, 10, 9, 6],
      frequency: "Every 15 minutes",
      operatingHours: "6:00 AM - 12:00 AM"
    },
    { 
      id: "B10", 
      name: "Medical Route", 
      type: "bus", 
      color: "#c2185b", 
      stops: ["F10", "F8", 4, 2, 5],
      frequency: "Every 25 minutes",
      operatingHours: "6:30 AM - 10:30 PM"
    },
    { 
      id: "M1", 
      name: "Metro Line 1", 
      type: "metro", 
      color: "#f44336", 
      stops: [12, 1, 3, "F2", 11],
      frequency: "Every 4 minutes",
      operatingHours: "5:30 AM - 1:00 AM"
    },
    { 
      id: "M2", 
      name: "Metro Line 2", 
      type: "metro", 
      color: "#e91e63", 
      stops: [11, "F2", 3, 10, 8],
      frequency: "Every 5 minutes",
      operatingHours: "5:30 AM - 1:00 AM"
    },
    { 
      id: "M3", 
      name: "Metro Line 3", 
      type: "metro", 
      color: "#9c27b0", 
      stops: ["F1", 5, 2, 3, 9],
      frequency: "Every 6 minutes",
      operatingHours: "5:30 AM - 12:30 AM"
    },
    { 
      id: "T1", 
      name: "Tram Line 1", 
      type: "tram", 
      color: "#4caf50", 
      stops: [5, "F13", 3, "F5", 10],
      frequency: "Every 10 minutes",
      operatingHours: "6:00 AM - 11:00 PM"
    },
    { 
      id: "T2", 
      name: "Tram Line 2", 
      type: "tram", 
      color: "#8bc34a", 
      stops: [8, "F11", "F3", 10, 6],
      frequency: "Every 12 minutes",
      operatingHours: "6:30 AM - 10:30 PM"
    }
  ];
  
  // Traffic data (average congestion level from 0-100)
  export const trafficData = [
    { roadId: "R1", level: 75, time: "morning" },
    { roadId: "R1", level: 60, time: "afternoon" },
    { roadId: "R1", level: 85, time: "evening" },
    { roadId: "R4", level: 90, time: "morning" },
    { roadId: "R4", level: 65, time: "afternoon" },
    { roadId: "R4", level: 95, time: "evening" },
    { roadId: "R9", level: 80, time: "morning" },
    { roadId: "R9", level: 55, time: "afternoon" },
    { roadId: "R9", level: 85, time: "evening" },
    { roadId: "R13", level: 70, time: "morning" },
    { roadId: "R13", level: 50, time: "afternoon" },
    { roadId: "R13", level: 75, time: "evening" },
    { roadId: "R20", level: 65, time: "morning" },
    { roadId: "R20", level: 45, time: "afternoon" },
    { roadId: "R20", level: 70, time: "evening" },
    { roadId: "R21", level: 85, time: "morning" },
    { roadId: "R21", level: 60, time: "afternoon" },
    { roadId: "R21", level: 90, time: "evening" },
    { roadId: "R24", level: 95, time: "morning" },
    { roadId: "R24", level: 70, time: "afternoon" },
    { roadId: "R24", level: 80, time: "evening" },
  ];
  
  // Points of interest (POIs)
  export const pointsOfInterest = [
    { id: "POI1", name: "Giza Pyramids", category: "Historical", lat: 29.9773, lng: 31.1325, rating: 4.9, visitors: 14000000 },
    { id: "POI2", name: "Khan el-Khalili", category: "Shopping", lat: 30.0478, lng: 31.2622, rating: 4.6, visitors: 5000000 },
    { id: "POI3", name: "Al-Azhar Mosque", category: "Religious", lat: 30.0444, lng: 31.2625, rating: 4.7, visitors: 3000000 },
    { id: "POI4", name: "Tahrir Square", category: "Landmark", lat: 30.0444, lng: 31.2357, rating: 4.3, visitors: 8000000 },
    { id: "POI5", name: "Coptic Cairo", category: "Historical", lat: 30.0042, lng: 31.2297, rating: 4.5, visitors: 2000000 },
    { id: "POI6", name: "Cairo Tower", category: "Landmark", lat: 30.0458, lng: 31.2241, rating: 4.4, visitors: 1500000 },
    { id: "POI7", name: "Nile Corniche", category: "Recreation", lat: 30.0367, lng: 31.2253, rating: 4.6, visitors: 10000000 },
    { id: "POI8", name: "Salah El Din Citadel", category: "Historical", lat: 30.0286, lng: 31.2598, rating: 4.8, visitors: 4000000 },
    { id: "POI9", name: "Baron Palace", category: "Historical", lat: 30.0878, lng: 31.3281, rating: 4.2, visitors: 500000 },
    { id: "POI10", name: "Hanging Church", category: "Religious", lat: 30.0056, lng: 31.2303, rating: 4.7, visitors: 1200000 },
  ];
  
  // Helper function to find node by ID
  export const getNodeById = (id: number | string): CityNode | undefined => {
    const numericId = typeof id === 'string' ? parseInt(id) : id;
    
    if (isNaN(numericId) || typeof id === 'string') {
      return facilityData.find(f => f.id === id);
    } else {
      return cityData.find(c => c.id === numericId);
    }
  };