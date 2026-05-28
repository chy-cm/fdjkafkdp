import axios from 'axios';
import { VideoInfo, Scene, Task, UploadResponse } from '../types';

const API_BASE_URL = process.env.REACT_APP_API_URL || '/api';

const api = axios.create({
  baseURL: API_BASE_URL,
});

export const videoApi = {
  upload: async (
    file: File,
    targetDuration: number,
    subtitleOption: string
  ): Promise<UploadResponse> => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('target_duration', targetDuration.toString());
    formData.append('subtitle_option', subtitleOption);
    
    const response = await api.post('/videos/', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    
    return response.data;
  },
  
  getInfo: async (videoId: number): Promise<VideoInfo> => {
    const response = await api.get(`/videos/${videoId}/info`);
    return response.data;
  },
  
  getScenes: async (videoId: number): Promise<{ scenes: Scene[] }> => {
    const response = await api.get(`/videos/${videoId}/scenes`);
    return response.data;
  },
};

export const taskApi = {
  getAll: async (status?: string): Promise<{ tasks: Task[] }> => {
    const params = status ? { status } : {};
    const response = await api.get('/tasks/', { params });
    return response.data;
  },
  
  getById: async (taskId: string): Promise<Task> => {
    const response = await api.get(`/tasks/${taskId}`);
    return response.data;
  },
  
  cancel: async (taskId: string): Promise<{ success: boolean; message: string }> => {
    const response = await api.delete(`/tasks/${taskId}`);
    return response.data;
  },
  
  createBatch: async (videos: any[]): Promise<{ task_ids: string[] }> => {
    const response = await api.post('/tasks/batch', { videos });
    return response.data;
  },
};

export const exportApi = {
  exportVideo: async (
    taskId: string,
    format: string = 'mp4',
    resolution: string = '1080p',
    bitrate: string = '5000k'
  ): Promise<{ download_url: string }> => {
    const response = await api.post(`/export/${taskId}`, {
      format,
      resolution,
      bitrate,
    });
    return response.data;
  },
  
  downloadVideo: async (taskId: string): Promise<Blob> => {
    const response = await api.get(`/export/${taskId}/download`, {
      responseType: 'blob',
    });
    return response.data;
  },
  
  downloadProject: async (taskId: string): Promise<Blob> => {
    const response = await api.get(`/export/${taskId}/project`, {
      responseType: 'blob',
    });
    return response.data;
  },
};

export default api;
