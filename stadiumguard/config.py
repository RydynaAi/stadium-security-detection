from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Config:
    source: str = "0"
    model_path: str = "yolov8n.pt"
    person_confidence: float = 0.25
    motion_threshold: int = 25
    motion_min_area: int = 1500
    blur_kernel: int = 0
    morph_kernel: int = 0
    track_min_frames: int = 0
    track_min_speed: float = 500.0
    track_max_distance: float = 150.0
    track_max_gap: int = 2
    alert_cooldown_seconds: float = 3.0
    output_dir: Path = Path("outputs")
    show_window: bool = True
