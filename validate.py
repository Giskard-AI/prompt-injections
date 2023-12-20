import pandas as pd
import ast

INJECTION_DATA_PATH = "prompt_injections.csv"
GISKARD_META_PATH = "giskard_meta_data.csv"

def _check_matching_dfs_len(df1, df2):
    if len(df1) != len(df2):
        raise ValueError(
            f"{__name__}: {INJECTION_DATA_PATH} and {GISKARD_META_PATH} should "
            "have the same length and should be a one-to-one mapping of each other."
        )

def _check_meta_df_requirements(df):
    if "expected_strings" not in df.columns:
        raise ValueError(f"{__name__}: expected_strings are needed for the evaluation.")

    if df.expected_strings.isnull().values.any():
        raise ValueError(f"{__name__}: expected_strings column cannot have any NaN values.")
    df.expected_strings = df.expected_strings.apply(ast.literal_eval)
    
    
if __name__ == "__main__":
    prompt_injections_df = pd.read_csv(INJECTION_DATA_PATH, index_col=["index"])
    meta_df = pd.read_csv(GISKARD_META_PATH, index_col=["index"])
    _check_matching_dfs_len(meta_df, prompt_injections_df)
    _check_meta_df_requirements(meta_df)
    print("Validation passed succesfully!")