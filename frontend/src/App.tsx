import React from 'react';
import { Provider } from 'react-redux';
import { store } from './store';
import Header from './components/Header';
import VideoUploader from './components/VideoUploader';
import TaskList from './components/TaskList';
import { Container, Box, Stack } from '@mui/material';

const App: React.FC = () => {
  return (
    <Provider store={store}>
      <Box sx={{ minHeight: '100vh', backgroundColor: 'background.default' }}>
        <Header />
        <Container maxWidth="lg" sx={{ mt: 8 }}>
          <Stack spacing={8}>
            <VideoUploader />
            <TaskList />
          </Stack>
        </Container>
      </Box>
    </Provider>
  );
};

export default App;
