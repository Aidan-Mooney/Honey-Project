from src.extract.extract import extract
import pandas as pd
import os
from scipy.stats import ttest_1samp


def main():
    null_hyp = "Lemon sales ≤ Peppermint sales (mean difference ≤ 0)"
    alt_hyp = "Lemon sales > Peppermint sales (mean difference > 0)"
    extract()
    data_dir = "data/extract"
    folders = [
        f for f in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, f))
    ]
    folder_name = folders[0]
    products_path = os.path.join(data_dir, folder_name, "products.csv")
    purchases_path = os.path.join(data_dir, folder_name, "purchases.csv")
    products_df = pd.read_csv(products_path, header=None)
    purchases_df = pd.read_csv(purchases_path, header=None)
    merged_df = products_df.merge(purchases_df, left_on=2, right_on=0, how="left")[
        ["0_x", "2_y"]
    ]
    merged_df["2_y"] = merged_df["2_y"].str[:10]
    lemon_sales = (
        merged_df[merged_df["0_x"] == "Lemon Lip Balm"]
        .groupby("2_y")
        .size()
        .reset_index(name="lemon_count")
    )
    peppermint_sales = (
        merged_df[merged_df["0_x"] == "Peppermint Lip Balm"]
        .groupby("2_y")
        .size()
        .reset_index(name="peppermint_count")
    )
    sales_by_date = pd.merge(lemon_sales, peppermint_sales, on="2_y", how="outer")
    sales_by_date.columns = ["date", "lemon_count", "peppermint_count"]
    sales_by_date = sales_by_date.fillna(0)
    sales_by_date["lemon_minus_peppermint"] = (
        sales_by_date["lemon_count"] - sales_by_date["peppermint_count"]
    )
    differences = sales_by_date["lemon_minus_peppermint"].tolist()
    t_stat, p_value = ttest_1samp(differences, popmean=0, alternative="greater")
    print(f"t_stat: {t_stat}")
    print(f"p_value: {p_value}")
    if p_value < 0.05:
        print("Null Hypothesis rejected! Alternate Hypothesis Accepted!")
        print(alt_hyp)
    else:
        print("Alternate Hypothesis rejected! Null Hypothesis Accepted!")
        print(null_hyp)
    print(t_stat, p_value)


if __name__ == "__main__":
    main()
