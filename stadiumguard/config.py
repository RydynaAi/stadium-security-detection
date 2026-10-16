from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Config:
    source: str = "0"
    model_path: str = "yolov8n.pt"
    person_confidence: float = 0.25
    motion_threshold: int = 25
    motion_min_area: int = 1500
    blur_kernel: int = 5
    morph_kernel: int = 5
    alert_cooldown_seconds: float = 3.0
    output_dir: Path = Path("outputs")
    show_window: bool = True
