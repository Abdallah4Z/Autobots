/**
 * City data with node IDs and coordinates
 * Used to convert between node IDs in API responses and geographic coordinates for the map
 */

export interface CityLocation {
  id: string;
  name: string;
  type: 'district' | 'facility';
  coordinates: {
    lat: number;
    lng: number;
  };
}

export const cityData: CityLocation[] = [
  // Districts (1-15)
  {
    id: '1',
    name: 'Maadi',
    type: 'district',
    coordinates: { lat: 29.9626, lng: 31.2497 }
  },
  {
    id: '2',
    name: 'Nasr City',
    type: 'district',
    coordinates: { lat: 30.0511, lng: 31.3656 }
  },
  {
    id: '3',
    name: 'Downtown Cairo',
    type: 'district',
    coordinates: { lat: 30.0444, lng: 31.2357 }
  },
  {
    id: '4',
    name: 'New Cairo',
    type: 'district',
    coordinates: { lat: 30.0300, lng: 31.4700 }
  },
  {
    id: '5',
    name: 'Heliopolis',
    type: 'district',
    coordinates: { lat: 30.0911, lng: 31.3425 }
  },
  {
    id: '6',
    name: 'Zamalek',
    type: 'district',
    coordinates: { lat: 30.0705, lng: 31.2183 }
  },
  {
    id: '7',
    name: '6th October City',
    type: 'district',
    coordinates: { lat: 29.9285, lng: 30.9188 }
  },
  {
    id: '8',
    name: 'Giza',
    type: 'district',
    coordinates: { lat: 29.9870, lng: 31.2118 }
  },
  {
    id: '9',
    name: 'Mohandessin',
    type: 'district',
    coordinates: { lat: 30.0576, lng: 31.2073 }
  },
  {
    id: '10',
    name: 'Dokki',
    type: 'district',
    coordinates: { lat: 30.0392, lng: 31.2113 }
  },
  {
    id: '11',
    name: 'Shubra',
    type: 'district',
    coordinates: { lat: 30.1179, lng: 31.2446 }
  },
  {
    id: '12',
    name: 'Helwan',
    type: 'district',
    coordinates: { lat: 29.8500, lng: 31.3333 }
  },
  {
    id: '13',
    name: 'New Administrative Capital',
    type: 'district',
    coordinates: { lat: 30.0075, lng: 31.7467 }
  },
  {
    id: '14',
    name: 'Al Rehab',
    type: 'district',
    coordinates: { lat: 30.0594, lng: 31.4923 }
  },
  {
    id: '15',
    name: 'Sheikh Zayed',
    type: 'district',
    coordinates: { lat: 30.0709, lng: 30.9580 }
  },

  // Facilities (F1-F10)
  {
    id: 'F1',
    name: 'Cairo International Airport',
    type: 'facility',
    coordinates: { lat: 30.1222, lng: 31.4058 }
  },
  {
    id: 'F2',
    name: 'Ramses Railway Station',
    type: 'facility',
    coordinates: { lat: 30.0636, lng: 31.2467 }
  },
  {
    id: 'F3',
    name: 'Cairo University',
    type: 'facility',
    coordinates: { lat: 30.0259, lng: 31.2094 }
  },
  {
    id: 'F4',
    name: 'Al-Azhar University',
    type: 'facility',
    coordinates: { lat: 30.0460, lng: 31.2656 }
  },
  {
    id: 'F5',
    name: 'Egyptian Museum',
    type: 'facility',
    coordinates: { lat: 30.0476, lng: 31.2337 }
  },
  {
    id: 'F6',
    name: 'Cairo International Stadium',
    type: 'facility',
    coordinates: { lat: 30.0728, lng: 31.2981 }
  },
  {
    id: 'F7',
    name: 'Smart Village',
    type: 'facility',
    coordinates: { lat: 30.0726, lng: 31.0183 }
  },
  {
    id: 'F8',
    name: 'Cairo Festival City',
    type: 'facility',
    coordinates: { lat: 30.0280, lng: 31.4069 }
  },
  {
    id: 'F9',
    name: 'Qasr El Aini Hospital',
    type: 'facility',
    coordinates: { lat: 30.0308, lng: 31.2262 }
  },
  {
    id: 'F10',
    name: 'Maadi Military Hospital',
    type: 'facility',
    coordinates: { lat: 29.9612, lng: 31.2520 }
  }
];

export const roadsData = [
  {from: 1, to: 3},
  {from: 1, to: 8},
  {from: 2, to: 3},
  {from: 2, to: 5},
  {from: 3, to: 5},
  {from: 3, to: 6},
  {from: 3, to: 9},
  {from: 3, to: 10},
  {from: 4, to: 2},
  {from: 4, to: 14},
  {from: 5, to: 11},
  {from: 6, to: 9},
  {from: 7, to: 8},
  {from: 7, to: 15},
  {from: 8, to: 10},
  {from: 8, to: 12},
  {from: 9, to: 10},
  {from: 10, to: 11},
  {from: 11, to: 'F2'},
  {from: 12, to: 1},
  {from: 13, to: 4},
  {from: 14, to: 13},
  {from: 15, to: 7},
  {from: 'F1', to: 5},
  {from: 'F1', to: 2},
  {from: 'F2', to: 3},
  {from: 'F7', to: 15},
  {from: 'F8', to: 4},
]

export const busRoutes = [
  {id: 'B1', stops: ['1', '3', '6', '9']},
  {id: 'B2', stops: ['7', '15', '8', '10', '3']},
  {id: 'B3', stops: ['2', '5', 'F1']},
  {id: 'B4', stops: ['4', '14', '2', '3']},
  {id: 'B5', stops: ['8', '12', '1']},
  {id: 'B6', stops: ['11', '5', '2']},
  {id: 'B7', stops: ['13', '4', '14']},
  {id: 'B8', stops: ['F7', '15', '7']},
  {id: 'B9', stops: ['1', '8', '10', '9', '6']},
  {id: 'B10', stops: ['F10', 'F8', '4', '2', '5']},
  {id: 'M11', stops: ['12', '1', '3', 'F2', '11']},
  {id: 'M12', stops: ['11', 'F2', '3', '10', '8']},
  {id: 'M13', stops: ['F1', '5', '2', '3', '9']},
]