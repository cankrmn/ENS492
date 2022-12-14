import pandas as pd

df = pd.read_csv("./reduced_dataset.csv")

reduced_df = df[:1000]

reduced_df.to_csv("./reduced_dataset[0,1000].csv")