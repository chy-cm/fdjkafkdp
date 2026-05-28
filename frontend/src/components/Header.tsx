import React from 'react';
import { AppBar, Toolbar, Typography, Box } from '@mui/material';
import { Movie } from '@mui/icons-material';

const Header: React.FC = () => {
  return (
    <AppBar position="static">
      <Toolbar>
        <Movie sx={{ mr: 2 }} />
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          CineSynopsis
        </Typography>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Typography variant="body1">AI 视频剪辑工具</Typography>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Header;
