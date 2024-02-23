import pandas as pd
import ast

INJECTION_DATA_PATH = "prompt_injections.csv"
GISKARD_META_PATH = "giskard_meta_data.csv"

def check_matching_dfs_len(df1, df2):
    if len(df1) != len(df2):
        raise ValueError(
            f"{__name__}: {INJECTION_DATA_PATH} and {GISKARD_META_PATH} should "
            "have the same length and should be a one-to-one mapping of each other."
        )

def check_meta_df_requirements(df):
    if "expected_strings" not in df.columns:
        raise ValueError(f"{__name__}: expected_strings are needed for the evaluation.")

    if df.expected_strings.isnull().values.any():
        raise ValueError(f"{__name__}: expected_strings column cannot have any NaN values.")
    df.expected_strings = df.expected_strings.apply(ast.literal_eval)

def check_group_description(df, group):
    group_description = df.loc[df["group_mapping"] == group].description.to_list()
    if len(set(group_description)) != 1:
        raise ValueError("There must be only one group description per group.")
    return group_description[0]

def check_group_deviation_description(df, group):
    group_deviation_description = df.loc[df["group_mapping"] == group].deviation_description.to_list()
    if len(set(group_deviation_description)) != 1:
        raise ValueError(
            "There must be only one group description deviation per group."
        )
    return group_deviation_description[0]

def check_uniqueness(df):
    if df.prompt.nunique() != len(df):
        dup = df[df.prompt.duplicated(keep=False)]
        indices = dup.groupby(list(dup)).apply(lambda x: tuple(x.index)).tolist()
        raise ValueError(
            f"{len(df) - df.prompt.nunique()} of the prompts are duplicated! These are the rows: {indices}"
        )
    
if __name__ == "__main__":
    prompt_injections_df = pd.read_csv(INJECTION_DATA_PATH, index_col=["index"])
    meta_df = pd.read_csv(GISKARD_META_PATH, index_col=["index"])
    check_uniqueness(prompt_injections_df)
    check_matching_dfs_len(meta_df, prompt_injections_df)
    check_meta_df_requirements(meta_df)
    for group in meta_df.group_mapping.unique().tolist():
        check_group_description(meta_df, group)
        check_group_deviation_description(meta_df, group)
        
        
    print("Validation passed succesfully!")