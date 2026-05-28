import React, { useEffect } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import {
  Card,
  CardContent,
  Container,
  LinearProgress,
  Stack,
  Typography,
  Button,
  Chip,
} from '@mui/material';
import { PlayCircle, Download, XCircle, RefreshCw } from '@mui/icons-material';
import { fetchTasks, cancelTask, fetchTask } from '../store/taskSlice';
import { RootState } from '../store';
import { Task } from '../types';
import { exportApi } from '../api';

const statusConfig = {
  pending: { label: '等待中', color: 'default' },
  processing: { label: '处理中', color: 'primary' },
  completed: { label: '已完成', color: 'success' },
  failed: { label: '失败', color: 'error' },
};

const TaskList: React.FC = () => {
  const { tasks, loading } = useSelector((state: RootState) => state.tasks);
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(fetchTasks());
  }, [dispatch]);

  useEffect(() => {
    const processingTasks = tasks.filter((t) => t.status === 'processing');
    if (processingTasks.length > 0) {
      const interval = setInterval(() => {
        processingTasks.forEach((task) => {
          dispatch(fetchTask(task.id));
        });
      }, 3000);
      return () => clearInterval(interval);
    }
  }, [tasks, dispatch]);

  const handleDownload = async (task: Task) => {
    try {
      const blob = await exportApi.downloadVideo(task.id);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `output_${task.id}.mp4`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      console.error('下载失败:', err);
    }
  };

  const handleCancel = (taskId: string) => {
    dispatch(cancelTask(taskId));
  };

  if (loading) {
    return (
      <Container maxWidth="md">
        <Typography>加载中...</Typography>
      </Container>
    );
  }

  if (tasks.length === 0) {
    return (
      <Container maxWidth="md">
        <Typography variant="body1" color="textSecondary">
          暂无任务，上传视频开始处理
        </Typography>
      </Container>
    );
  }

  return (
    <Container maxWidth="md">
      <Typography variant="h5" component="h2" gutterBottom>
        任务列表
      </Typography>
      <Stack spacing={2}>
        {tasks.map((task) => {
          const status = statusConfig[task.status];
          return (
            <Card key={task.id} variant="outlined">
              <CardContent>
                <Stack direction="row" alignItems="center" spacing={2}>
                  <div style={{ flex: 1 }}>
                    <Typography variant="subtitle1">任务 {task.id.slice(0, 8)}</Typography>
                    <Typography variant="body2" color="textSecondary">
                      目标时长: {Math.floor(task.target_duration / 60)} 分钟
                    </Typography>
                  </div>
                  <Chip
                    label={status.label}
                    color={status.color as any}
                    size="small"
                  />
                </Stack>

                {task.status === 'processing' && (
                  <div style={{ marginTop: 16 }}>
                    <LinearProgress variant="determinate" value={task.progress} />
                    <Typography variant="caption" color="textSecondary" mt={1}>
                      {task.progress}%
                    </Typography>
                  </div>
                )}

                {task.status === 'failed' && (
                  <Typography color="error" variant="body2" mt={2}>
                    {task.error_message || '处理失败'}
                  </Typography>
                )}

                <Stack direction="row" spacing={2} mt={2}>
                  {task.status === 'completed' && (
                    <>
                      <Button
                        variant="contained"
                        size="small"
                        startIcon={<Download />}
                        onClick={() => handleDownload(task)}
                      >
                        下载视频
                      </Button>
                      <Button
                        variant="outlined"
                        size="small"
                        startIcon={<PlayCircle />}
                      >
                        预览
                      </Button>
                    </>
                  )}
                  {task.status === 'pending' && (
                    <Button
                      variant="outlined"
                      size="small"
                      startIcon={<RefreshCw />}
                      onClick={() => dispatch(fetchTask(task.id))}
                    >
                      刷新状态
                    </Button>
                  )}
                  {(task.status === 'pending' || task.status === 'processing') && (
                    <Button
                      variant="outlined"
                      size="small"
                      color="error"
                      startIcon={<XCircle />}
                      onClick={() => handleCancel(task.id)}
                    >
                      取消
                    </Button>
                  )}
                </Stack>
              </CardContent>
            </Card>
          );
        })}
      </Stack>
    </Container>
  );
};

export default TaskList;
