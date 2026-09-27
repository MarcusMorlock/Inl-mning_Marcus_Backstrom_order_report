from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

@dataclass(frozen=True)
class ReportConfig:
    input_path: Path = PROJECT_ROOT / "data" / "orders.csv"
    output_dir: Path = PROJECT_ROOT / "data_output"
    log_path: Path = PROJECT_ROOT / "logs" / "order_report.log"

    def ensure_directories(self) -> None:

        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)