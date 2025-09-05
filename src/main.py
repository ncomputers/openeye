import sys
import yaml


def load_config(path):
    """Load pipeline configuration from YAML file."""
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def build_pipeline(cfg):
    """Build a DeepStream GStreamer pipeline from configuration."""
    import gi
    gi.require_version('Gst', '1.0')
    from gi.repository import Gst

    Gst.init(None)

    pipeline = Gst.Pipeline()

    source = Gst.ElementFactory.make('rtspsrc', 'source')
    streammux = Gst.ElementFactory.make('nvstreammux', 'stream-muxer')
    pgie = Gst.ElementFactory.make('nvinfer', 'primary-inference')
    tracker = Gst.ElementFactory.make('nvtracker', 'tracker')
    nvdsosd = Gst.ElementFactory.make('nvdsosd', 'onscreendisplay')
    sink = Gst.ElementFactory.make('appsink', 'app-sink')

    if not all([source, streammux, pgie, tracker, nvdsosd, sink]):
        raise RuntimeError('Failed to create one or more GStreamer elements')

    source.set_property('location', cfg['source']['uri'])
    pgie.set_property('config-file-path', cfg['infer']['config'])
    tracker.set_property('ll-config-file', cfg['tracker']['config'])

    pipeline.add(source)
    pipeline.add(streammux)
    pipeline.add(pgie)
    pipeline.add(tracker)
    pipeline.add(nvdsosd)
    pipeline.add(sink)

    source.link(streammux)
    streammux.link(pgie)
    pgie.link(tracker)
    tracker.link(nvdsosd)
    nvdsosd.link(sink)

    return pipeline


def main(config_path):
    cfg = load_config(config_path)
    pipeline = build_pipeline(cfg)

    from gi.repository import Gst

    pipeline.set_state(Gst.State.PLAYING)
    bus = pipeline.get_bus()
    bus.timed_pop_filtered(Gst.CLOCK_TIME_NONE, Gst.MessageType.EOS)
    pipeline.set_state(Gst.State.NULL)


if __name__ == '__main__':
    config = sys.argv[1] if len(sys.argv) > 1 else '/app/configs/pipeline.yml'
    main(config)
