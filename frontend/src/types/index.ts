export interface VideoInfo {
  id: number;
  filename: string;
  duration: number;
  fps?: number;
  width?: number;
  height?: number;
  format?: string;
}

export interface Scene {
  id: number;
  video_id: number;
  start_time: number;
  end_time: number;
  score: number;
  scene_type: string;
  description?: string;
}

export interface Task {
  id: string;
  video_id: number;
  status: TaskStatus;
  progress: number;
  target_duration: number;
  subtitle_option: string;
  result_path?: string;
  error_message?: string;
  created_at: string;
  updated_at: string;
}

export type TaskStatus = 'pending' | 'processing' | 'completed' | 'failed';

export interface UploadResponse {
  task_id: string;
  video_id: number;
  video_info: VideoInfo;
  message: string;
}
