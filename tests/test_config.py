from pathlib import Path
import sys

# ensure project root on path
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.main import load_config


def test_load_config_has_placeholders():
    cfg_path = ROOT / 'configs' / 'pipeline.yml'
    cfg = load_config(cfg_path)
    assert cfg['source']['uri'] == 'rtsp://your_rtsp_url_here'
    assert cfg['infer']['config'] == '/app/models/your_model.engine'
    assert cfg['tracker']['config'] == '/app/configs/tracker_config.yml'
