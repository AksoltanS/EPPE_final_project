"""All the general configuration of the project."""

from pathlib import Path

SRC: Path = Path(__file__).parent.resolve()
ROOT: Path = SRC.joinpath("..", "..").resolve()

BLD: Path = ROOT.joinpath("bld").resolve()

DOCUMENTS: Path = ROOT.joinpath("documents").resolve()

TEMPLATE_GROUPS: tuple[str, ...] = ("marital_status", "highest_qualification")

DATA = SRC / "data"
DATA_RAW = DATA / "raw"

FOLLOW_BACKS_RAW = DATA_RAW / "follow_backs.csv"

BLD_DATA = BLD / "data"
BLD_FIGURES = BLD / "figures"

FOLLOW_BACKS_ANALYSIS = BLD_DATA / "follow_backs_analysis.parquet"
FIG1_DATA = BLD_FIGURES / "fig1_data.csv"
FIG1_PNG = BLD_FIGURES / "fig1_followbacks_type.png"
