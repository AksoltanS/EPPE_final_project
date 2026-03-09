"""All the general configuration of the project."""

from pathlib import Path

SRC: Path = Path(__file__).parent.resolve()
ROOT: Path = SRC.joinpath("..", "..").resolve()
BLD: Path = ROOT.joinpath("bld").resolve()

TEMPLATE_GROUPS: tuple[str, ...] = ("marital_status", "highest_qualification")

DATA = SRC / "data"
DATA_RAW = DATA / "raw"
BLD_DATA = BLD / "data"
BLD_FIGURES = BLD / "figures"

FOLLOW_BACKS_RAW = DATA_RAW / "follow_backs.csv"
SUBJECT_POOL_RAW = DATA_RAW / "subject_pool.csv"
SUBJECT_POOL_SCRAMBLED_RAW = DATA_RAW / "subject_pool_scrambled.csv"

FOLLOW_BACKS_ANALYSIS = BLD_DATA / "follow_backs_analysis.parquet"
SUBJECT_POOL_ANALYSIS = BLD_DATA / "subject_pool_analysis.parquet"

BOT_VARS: list[str] = ["bot_gender", "bot_race", "bot_uni"]
CONTROLS_CATEGORICAL: list[str] = ["continent", "profession", "female"]
CONTROLS_CONTINUOUS: list[str] = [
    "above_median_year_created",
    "follow_diversity",
    "background_pic",
    "above_median_followers_count",
    "above_median_friends_count",
]
FE_GROUPS: list[str] = ["wave", "strata", "missfit"]
PVAL_DISPLAY_THRESHOLD: float = 0.001


FIG1_DATA = BLD_FIGURES / "fig1_data.csv"
FIG1_PNG = BLD_FIGURES / "fig1_followbacks_type.png"
FIG2_GENDER_DATA = BLD_FIGURES / "fig2_gender.csv"
FIG2_RACE_DATA = BLD_FIGURES / "fig2_race.csv"
FIG2_UNI_DATA = BLD_FIGURES / "fig2_uni.csv"
FIG2_PNG = BLD_FIGURES / "fig2_marginals.png"
FIG2_CONTROLS_DATA = BLD_FIGURES / "fig2_controls.csv"

FIG3A_DATA = BLD_FIGURES / "fig3a_data.csv"
FIG3A_PNG = BLD_FIGURES / "fig3a_interaction.png"

FIG3B_DATA = BLD_FIGURES / "fig3b_data.csv"
FIG3B_PNG = BLD_FIGURES / "fig3b_interactions.png"

TABLE1A_TEX: Path = BLD_FIGURES / "table1a.tex"
TABLE1B_TEX: Path = BLD_FIGURES / "table1b.tex"
