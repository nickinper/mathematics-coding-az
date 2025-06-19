import React from 'react';
import { Container, Box, Typography, Button, Paper } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import ErrorOutlineIcon from '@mui/icons-material/ErrorOutline';

const NotFound = () => {
  return (
    <Container maxWidth="md">
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          minHeight: '100vh',
          textAlign: 'center',
          py: 4
        }}
      >
        <Paper elevation={3} sx={{ p: 5, borderRadius: 2, width: '100%' }}>
          <ErrorOutlineIcon sx={{ fontSize: 80, color: 'error.main', mb: 2 }} />
          
          <Typography variant="h2" component="h1" gutterBottom>
            404
          </Typography>
          
          <Typography variant="h4" component="h2" gutterBottom>
            Page Not Found
          </Typography>
          
          <Typography variant="body1" paragraph sx={{ mb: 4 }}>
            The page you are looking for might have been removed, had its name changed,
            or is temporarily unavailable.
          </Typography>
          
          <Box sx={{ display: 'flex', justifyContent: 'center', gap: 2 }}>
            <Button 
              variant="contained" 
              color="primary" 
              component={RouterLink} 
              to="/dashboard"
              size="large"
            >
              Go to Dashboard
            </Button>
            
            <Button 
              variant="outlined" 
              component={RouterLink} 
              to="/challenges"
              size="large"
            >
              Explore Challenges
            </Button>
          </Box>
        </Paper>
      </Box>
    </Container>
  );
};

export default NotFound;