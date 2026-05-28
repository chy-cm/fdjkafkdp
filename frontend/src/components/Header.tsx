import React from 'react';
import { AppBar, Toolbar, Typography, Box } from '@mui/material';
import { Film } from '@mui/icons-material';

const Header: React.FC = () => {
  return (
    <AppBar position="static">
      <Toolbar>
        <Film sx={{ mr: 2 }} />
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
