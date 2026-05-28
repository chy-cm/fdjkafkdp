import React, { useState } from 'react';
import {
  Button,
  Card,
  CardContent,
  Container,
  FormControl,
  InputLabel,
  MenuItem,
  Select,
  Stack,
  Typography,
  Box,
  CircularProgress,
} from '@mui/material';
import { Upload, Movie } from '@mui/icons-material';
import { videoApi } from '../api';
import { useDispatch } from 'react-redux';
import { addTask } from '../store/taskSlice';
import { Task, UploadResponse } from '../types';

const durationOptions = [
  { value: 180, label: '3 分钟' },
  { value: 300, label: '5 分钟' },
  { value: 600, label: '10 分钟' },
];

const subtitleOptions = [
  { value: 'new', label: '生成新字幕' },
  { value: 'keep', label: '保留原字幕' },
];

const VideoUploader: React.FC = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [targetDuration, setTargetDuration] = useState(300);
  const [subtitleOption, setSubtitleOption] = useState('new');
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const dispatch = useDispatch();

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      const allowedExtensions = ['mp4', 'mov', 'mkv', 'avi'];
      const extension = file.name.split('.').pop()?.toLowerCase();
      if (!allowedExtensions.includes(extension || '')) {
        setError('不支持的文件格式，请上传 MP4、MOV、MKV 或 AVI 格式');
        setSelectedFile(null);
        return;
      }
      setSelectedFile(file);
      setError(null);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError('请先选择视频文件');
      return;
    }

    setUploading(true);
    setError(null);

    try {
      const response: UploadResponse = await videoApi.upload(
        selectedFile,
        targetDuration,
        subtitleOption
      );

      const newTask: Task = {
        id: response.task_id,
        video_id: response.video_id,
        status: 'pending',
        progress: 0,
        target_duration: targetDuration,
        subtitle_option: subtitleOption,
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      };

      dispatch(addTask(newTask));
      setSelectedFile(null);
    } catch (err) {
      setError('上传失败，请重试');
    } finally {
      setUploading(false);
    }
  };

  return (
    <Container maxWidth="md">
      <Card variant="outlined">
        <CardContent>
          <Typography variant="h5" component="h2" gutterBottom>
            上传视频
          </Typography>

          <Stack spacing={4}>
            <Box
              sx={{
                border: 2,
                borderStyle: 'dashed',
                borderColor: selectedFile ? 'primary.main' : 'grey.300',
                borderRadius: 2,
                p: 6,
                textAlign: 'center',
                cursor: 'pointer',
              }}
              onClick={() => document.getElementById('file-input')?.click()}
            >
              <input
                id="file-input"
                type="file"
                accept="video/mp4,video/quicktime,video/x-matroska,video/x-msvideo"
                onChange={handleFileChange}
                style={{ display: 'none' }}
              />
              <Movie
                sx={{ fontSize: 48, color: selectedFile ? 'primary.main' : 'grey.400' }}
              />
              <Typography mt={2}>
                {selectedFile ? selectedFile.name : '点击选择视频文件'}
              </Typography>
              <Typography variant="caption" color="textSecondary">
                支持 MP4、MOV、MKV、AVI 格式，最大 5GB
              </Typography>
            </Box>

            {error && (
              <Typography color="error">{error}</Typography>
            )}

            <FormControl fullWidth>
              <InputLabel id="duration-label">目标时长</InputLabel>
              <Select
                labelId="duration-label"
                id="duration-select"
                value={targetDuration}
                label="目标时长"
                onChange={(e) => setTargetDuration(e.target.value as number)}
              >
                {durationOptions.map((option) => (
                  <MenuItem key={option.value} value={option.value}>
                    {option.label}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            <FormControl fullWidth>
              <InputLabel id="subtitle-label">字幕选项</InputLabel>
              <Select
                labelId="subtitle-label"
                id="subtitle-select"
                value={subtitleOption}
                label="字幕选项"
                onChange={(e) => setSubtitleOption(e.target.value as string)}
              >
                {subtitleOptions.map((option) => (
                  <MenuItem key={option.value} value={option.value}>
                    {option.label}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>

            <Button
              variant="contained"
              size="large"
              onClick={handleUpload}
              disabled={!selectedFile || uploading}
              startIcon={uploading ? <CircularProgress size={20} /> : <Upload />}
            >
              {uploading ? '上传中...' : '开始处理'}
            </Button>
          </Stack>
        </CardContent>
      </Card>
    </Container>
  );
};

export default VideoUploader;
