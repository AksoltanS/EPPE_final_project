"""All the general configuration of the project."""

from pathlib import Path

SRC: Path = Path(__file__).parent.resolve()
ROOT: Path = SRC.joinpath("..", "..").resolve()
BLD: Path = ROOT.joinpath("bld").resolve()

DATA_RAW = SRC / "data" / "raw"

FOLLOW_BACKS_RAW = DATA_RAW / "follow_backs.csv"
SUBJECT_POOL_RAW = DATA_RAW / "subject_pool.csv"
SUBJECT_POOL_SCRAMBLED_RAW = DATA_RAW / "subject_pool_scrambled.csv"


BLD_DATA = BLD / "data"
BLD_FIGURES = BLD / "figures"
BLD_TABLES = BLD / "tables"

FOLLOW_BACKS_ANALYSIS = BLD_DATA / "follow_backs_analysis.parquet"
SUBJECT_POOL_ANALYSIS = BLD_DATA / "subject_pool_analysis.parquet"


FIG1_DATA = BLD_FIGURES / "fig1_data.csv"
FIG1_PNG = BLD_FIGURES / "fig1_followbacks_type.png"

FIG2_GENDER_DATA = BLD_FIGURES / "fig2_gender_data.csv"
FIG2_RACE_DATA = BLD_FIGURES / "fig2_race_data.csv"
FIG2_UNI_DATA = BLD_FIGURES / "fig2_uni_data.csv"
FIG2_CONTROLS_DATA = BLD_FIGURES / "fig2_controls_data.csv"
FIG2_PNG = BLD_FIGURES / "fig2_main_results_marginal.png"

FIG3A_DATA = BLD_FIGURES / "fig3a_data.csv"
FIG3A_PNG = BLD_FIGURES / "fig3a_main_results_interactions.png"

FIG3B_DATA = BLD_FIGURES / "fig3b_data.csv"
FIG3B_PNG = BLD_FIGURES / "fig3b_interactions_coefficients.png"

TABLE1A_TEX = BLD_TABLES / "Table1a_Descriptives_Qualitative.tex"
TABLE1B_TEX = BLD_TABLES / "Table1b_Descriptives_Quantitative.tex"

BOT_VARS = ["bot_gender", "bot_race", "bot_uni"]

CONTROLS_CATEGORICAL = ["continent", "profession", "female"]

CONTROLS_CONTINUOUS = [
    "above_median_year_created",
    "follow_diversity",
    "background_pic",
    "above_median_followers_count",
    "above_median_friends_count",
]

FE_VARS = ["wave", "strata", "missfit"]

PVAL_DISPLAY_THRESHOLD = 0.001

TABLE1_QUAL_VARS = [
    "gender",
    "continent",
    "profession",
    "race",
    "follow_diversity",
    "background_pic",
]

TABLE1_QUAL_VARS_SCRAMBLED = [
    "TopUni_10",
    "verified",
]

TABLE1_QUANT_VARS = [
    "followers_count",
    "friends_count",
    "statuses_count",
    "favourites_count",
    "listed_count",
    "share_mobile",
]
