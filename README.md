# DeepStream Python App

This project demonstrates a minimal DeepStream pipeline built with Python and packaged for the official NVIDIA DeepStream container.

## Build the container

```bash
docker build -t ds-app -f docker/Dockerfile .
```

## Run with GPU and mount /work

```bash
docker run --rm --gpus all -v $(pwd):/work ds-app
```

The container executes `src/main.py`, which reads `/app/configs/pipeline.yml` to construct a pipeline consisting of `rtspsrc → nvstreammux → nvinfer → nvtracker → nvdsosd → appsink`. Edit `configs/pipeline.yml` to set your RTSP URL, model path, and tracker configuration before building.
