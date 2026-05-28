# CineSynopsis - 开发任务分解与优先级列表

## [ ] Task 1: 项目基础架构搭建
- **Priority**: P0
- **Depends On**: None
- **Description**: 
  - 创建项目目录结构
  - 配置后端 Python 虚拟环境和依赖
  - 配置前端 React + TypeScript 项目
  - 设置 Docker Compose 开发环境
- **Acceptance Criteria Addressed**: 无（基础设施任务）
- **Test Requirements**:
  - `programmatic` TR-1.1: 后端服务启动成功，访问 `/docs` 返回 API 文档
  - `programmatic` TR-1.2: 前端项目构建成功，无错误
  - `programmatic` TR-1.3: Docker Compose 启动所有服务正常

## [ ] Task 2: 数据库模型设计与实现
- **Priority**: P0
- **Depends On**: Task 1
- **Description**: 
  - 使用 SQLAlchemy 定义 Video、Scene、Task 模型
  - 创建数据库迁移脚本
  - 实现 CRUD 操作封装
- **Acceptance Criteria Addressed**: AC-1, AC-7, AC-8
- **Test Requirements**:
  - `programmatic` TR-2.1: 视频记录成功插入数据库
  - `programmatic` TR-2.2: 场景列表关联查询正确
  - `programmatic` TR-2.3: 任务状态更新正常

## [ ] Task 3: 视频上传与预处理模块
- **Priority**: P0
- **Depends On**: Task 2
- **Description**: 
  - 实现视频文件上传接口
  - 使用 FFmpeg 提取视频元信息（时长、帧率、分辨率）
  - 视频文件存储管理
  - 格式校验和大小限制
- **Acceptance Criteria Addressed**: AC-1
- **Test Requirements**:
  - `programmatic` TR-3.1: 支持 MP4/MOV/MKV/AVI 格式上传
  - `programmatic` TR-3.2: 视频元信息正确提取
  - `programmatic` TR-3.3: 超过大小限制的文件被拒绝

## [ ] Task 4: 场景分割模块（基于 PySceneDetect）
- **Priority**: P0
- **Depends On**: Task 3
- **Description**: 
  - 集成 PySceneDetect 场景检测库
  - 实现基于内容的场景分割算法
  - 提取场景关键帧
  - 存储场景列表到数据库
- **Acceptance Criteria Addressed**: AC-2
- **Test Requirements**:
  - `programmatic` TR-4.1: 场景分割结果正确存储
  - `human-judgment` TR-4.2: 分割结果符合人工预期（场景边界合理）

## [ ] Task 5: 语音识别模块（Whisper）
- **Priority**: P0
- **Depends On**: Task 3
- **Description**: 
  - 集成 OpenAI Whisper 进行语音转文字
  - 提取视频中的对话内容
  - 时间戳对齐
- **Acceptance Criteria Addressed**: AC-2, AC-4
- **Test Requirements**:
  - `programmatic` TR-5.1: 语音识别结果包含时间戳
  - `human-judgment` TR-5.2: 识别准确率 > 90%

## [ ] Task 6: LLM 场景分析与评分模块
- **Priority**: P0
- **Depends On**: Task 4, Task 5
- **Description**: 
  - 调用 LLM 分析场景内容
  - 实现场景重要性评分算法
  - 识别关键事件、高潮、结局等场景类型
  - 追踪人物关系与因果链
- **Acceptance Criteria Addressed**: AC-2
- **Test Requirements**:
  - `programmatic` TR-6.1: 每个场景都有评分和类型标签
  - `human-judgment` TR-6.2: 关键场景（高潮/结局）被正确识别

## [ ] Task 7: 动态规划剪辑优化模块
- **Priority**: P0
- **Depends On**: Task 6
- **Description**: 
  - 实现动态规划算法选择最优场景序列
  - 满足目标时长约束
  - 保持场景顺序和故事连贯性
- **Acceptance Criteria Addressed**: AC-3
- **Test Requirements**:
  - `programmatic` TR-7.1: 输出时长在目标时长的 ±10% 范围内
  - `programmatic` TR-7.2: 关键场景（评分=1.0）全部被选中

## [ ] Task 8: 旁白脚本生成模块
- **Priority**: P0
- **Depends On**: Task 7
- **Description**: 
  - 根据选中场景生成连贯的叙述文本
  - 适配目标时长调整详略
  - 保持故事逻辑完整性
- **Acceptance Criteria Addressed**: AC-4
- **Test Requirements**:
  - `human-judgment` TR-8.1: 旁白文本连贯，覆盖主要剧情
  - `human-judgment` TR-8.2: 旁白时长与目标时长匹配

## [ ] Task 9: TTS 语音合成模块
- **Priority**: P0
- **Depends On**: Task 8
- **Description**: 
  - 集成 TTS 引擎（如 OpenAI TTS）
  - 支持多语言、多音色选择
  - 语速动态调整适配目标时长
- **Acceptance Criteria Addressed**: AC-4
- **Test Requirements**:
  - `programmatic` TR-9.1: 生成的语音文件格式正确（MP3/WAV）
  - `human-judgment` TR-9.2: 语音自然度评分 > 4.5/5

## [ ] Task 10: 音画合成与转场模块
- **Priority**: P0
- **Depends On**: Task 7, Task 9
- **Description**: 
  - 使用 FFmpeg 进行视频剪辑
  - 添加场景间平滑转场（淡入淡出、硬切）
  - 旁白音频与画面同步
  - 删除原音频轨道
- **Acceptance Criteria Addressed**: AC-3, AC-5
- **Test Requirements**:
  - `programmatic` TR-10.1: 输出视频无原音频
  - `human-judgment` TR-10.2: 转场效果平滑无跳动
  - `human-judgment` TR-10.3: 旁白与画面节奏对齐

## [ ] Task 11: 字幕生成与嵌入模块
- **Priority**: P1
- **Depends On**: Task 9
- **Description**: 
  - 支持保留原字幕或生成新字幕
  - 旁白文字同步显示
  - 字幕样式配置（字体、颜色、位置）
- **Acceptance Criteria Addressed**: AC-1, AC-5
- **Test Requirements**:
  - `programmatic` TR-11.1: 字幕正确嵌入视频
  - `human-judgment` TR-11.2: 字幕与旁白同步

## [ ] Task 12: 背景音乐添加模块
- **Priority**: P1
- **Depends On**: Task 10
- **Description**: 
  - 集成无版权背景音乐库
  - 背景音乐音量控制
  - 自动适配视频时长
- **Acceptance Criteria Addressed**: AC-5
- **Test Requirements**:
  - `programmatic` TR-12.1: 背景音乐正确混合
  - `human-judgment` TR-12.2: 背景音乐音量不盖过旁白

## [ ] Task 13: 视频导出模块
- **Priority**: P0
- **Depends On**: Task 10
- **Description**: 
  - 支持 MP4 (H.264/H.265) 格式导出
  - 可调节分辨率与码率
  - 提供下载链接
- **Acceptance Criteria Addressed**: AC-6
- **Test Requirements**:
  - `programmatic` TR-13.1: 导出视频格式正确
  - `programmatic` TR-13.2: 分辨率和码率符合设置

## [ ] Task 14: 项目文件保存模块
- **Priority**: P1
- **Depends On**: Task 7, Task 8
- **Description**: 
  - 保存剪辑序列信息
  - 保存旁白脚本
  - 支持项目文件导入和微调
- **Acceptance Criteria Addressed**: AC-7
- **Test Requirements**:
  - `programmatic` TR-14.1: 项目文件正确保存（JSON格式）
  - `programmatic` TR-14.2: 项目文件可正确导入

## [ ] Task 15: 异步任务管理模块
- **Priority**: P0
- **Depends On**: Task 3
- **Description**: 
  - 使用 Celery + Redis 实现异步任务队列
  - 任务状态追踪和进度更新
  - 任务取消功能
- **Acceptance Criteria Addressed**: AC-1, AC-8
- **Test Requirements**:
  - `programmatic` TR-15.1: 任务状态正确更新（pending→processing→completed）
  - `programmatic` TR-15.2: 任务取消功能正常工作

## [ ] Task 16: 批量处理模块
- **Priority**: P1
- **Depends On**: Task 15
- **Description**: 
  - 支持队列输入多部影片
  - 批量任务状态汇总
  - 批量导出功能
- **Acceptance Criteria Addressed**: AC-8
- **Test Requirements**:
  - `programmatic` TR-16.1: 批量任务创建成功
  - `programmatic` TR-16.2: 批量进度统计正确

## [ ] Task 17: 前端基础组件开发
- **Priority**: P0
- **Depends On**: Task 1
- **Description**: 
  - 视频上传组件（VideoUploader）
  - 任务列表组件（TaskList）
  - 进度显示组件（ProgressBar）
  - 导出配置组件（ExportPanel）
- **Acceptance Criteria Addressed**: AC-1, AC-6, AC-8
- **Test Requirements**:
  - `human-judgment` TR-17.1: UI 布局美观合理
  - `programmatic` TR-17.2: 上传功能正常工作

## [ ] Task 18: 前端场景预览组件
- **Priority**: P1
- **Depends On**: Task 4
- **Description**: 
  - 场景列表展示
  - 场景时间线预览
  - 场景选择和排序调整
- **Acceptance Criteria Addressed**: AC-2
- **Test Requirements**:
  - `human-judgment` TR-18.1: 场景预览界面直观易用

## [ ] Task 19: API 集成与状态管理
- **Priority**: P0
- **Depends On**: Task 3, Task 15, Task 17
- **Description**: 
  - 配置 API 客户端
  - Redux 状态管理
  - 异步任务状态订阅
- **Acceptance Criteria Addressed**: 所有 AC
- **Test Requirements**:
  - `programmatic` TR-19.1: API 请求正确处理
  - `programmatic` TR-19.2: 状态更新实时反映到 UI

## [ ] Task 20: 错误处理与用户反馈
- **Priority**: P1
- **Depends On**: 所有模块
- **Description**: 
  - 全局错误捕获
  - 用户友好的错误提示
  - 处理进度实时反馈
- **Acceptance Criteria Addressed**: NFR-6
- **Test Requirements**:
  - `human-judgment` TR-20.1: 错误提示清晰易懂
  - `programmatic` TR-20.2: 进度条正确更新

## [ ] Task 21: 测试与验证
- **Priority**: P0
- **Depends On**: 所有模块
- **Description**: 
  - 编写单元测试
  - 编写集成测试
  - 手动验证各功能模块
- **Acceptance Criteria Addressed**: 所有 AC
- **Test Requirements**:
  - `programmatic` TR-21.1: 单元测试覆盖率 > 70%
  - `human-judgment` TR-21.2: 完整流程测试通过

## [ ] Task 22: 部署文档与配置
- **Priority**: P1
- **Depends On**: 所有模块
- **Description**: 
  - 编写部署指南
  - 配置生产环境 Docker Compose
  - 设置 Nginx 反向代理
- **Acceptance Criteria Addressed**: 无（文档任务）
- **Test Requirements**:
  - `programmatic` TR-22.1: Docker Compose 生产环境启动正常
