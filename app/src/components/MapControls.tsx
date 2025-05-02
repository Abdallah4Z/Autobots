import { Paper, Typography } from '@mui/material';
import { useSelector } from 'react-redux';
import { RootState } from '../redux/store';

const MapControls: React.FC = () => {
  const { lat, lng } = useSelector((state: RootState) => state.map.position);

  return (
    <></>
    // <Paper elevation={3} sx={{ position: 'absolute', top: 16, left: 16, padding: 2 }}>
    //   <Typography variant="h6">Current Position</Typography>
    //   <Typography>Lat: {lat.toFixed(5)}</Typography>
    //   <Typography>Lng: {lng.toFixed(5)}</Typography>
    // </Paper>
  );
};

export default MapControls;
