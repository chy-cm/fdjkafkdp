import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { Task } from '../types';
import { taskApi } from '../api';

interface TaskState {
  tasks: Task[];
  loading: boolean;
  error: string | null;
}

const initialState: TaskState = {
  tasks: [],
  loading: false,
  error: null,
};

export const fetchTasks = createAsyncThunk('tasks/fetchTasks', async (status?: string) => {
  const response = await taskApi.getAll(status);
  return response.tasks;
});

export const fetchTask = createAsyncThunk('tasks/fetchTask', async (taskId: string) => {
  const response = await taskApi.getById(taskId);
  return response;
});

export const cancelTask = createAsyncThunk('tasks/cancelTask', async (taskId: string) => {
  await taskApi.cancel(taskId);
  return taskId;
});

const taskSlice = createSlice({
  name: 'tasks',
  initialState,
  reducers: {
    addTask: (state, action: PayloadAction<Task>) => {
      state.tasks.unshift(action.payload);
    },
    updateTask: (state, action: PayloadAction<Task>) => {
      const index = state.tasks.findIndex((t) => t.id === action.payload.id);
      if (index !== -1) {
        state.tasks[index] = action.payload;
      }
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchTasks.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchTasks.fulfilled, (state, action) => {
        state.loading = false;
        state.tasks = action.payload;
      })
      .addCase(fetchTasks.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch tasks';
      })
      .addCase(fetchTask.fulfilled, (state, action) => {
        const index = state.tasks.findIndex((t) => t.id === action.payload.id);
        if (index !== -1) {
          state.tasks[index] = action.payload;
        } else {
          state.tasks.push(action.payload);
        }
      })
      .addCase(cancelTask.fulfilled, (state, action) => {
        const index = state.tasks.findIndex((t) => t.id === action.payload);
        if (index !== -1) {
          state.tasks[index].status = 'failed';
          state.tasks[index].error_message = 'Task cancelled by user';
        }
      });
  },
});

export const { addTask, updateTask } = taskSlice.actions;

export default taskSlice.reducer;
