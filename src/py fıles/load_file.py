import pandas as pd
from sklearn.model_selection import train_test_split
from datasets import load_dataset

def load_file(file_name, files_exists = False):
   main_df = pd.read_csv(file_name)

   datasets = {} # dict of datasets to be returned {category_name: dataset}

   dfs = [main_df[["raw_text",col]] for col in main_df][1:] # creates a dataframe for each label

   for df in dfs:
      train, test = train_test_split(df, test_size=0.15, random_state=42)
      train, validation = train_test_split(train, test_size=0.20, random_state=42)


      train_data_name =  df.columns[1] + '_train_data.csv'
      validation_data_name =  df.columns[1] + '_validation_data.csv'
      test_data_name =  df.columns[1] + '_test_data.csv'

      if not files_exists:
         train.to_csv(train_data_name, index=False)
         validation.to_csv(validation_data_name, index=False)
         test.to_csv(test_data_name, index=False)

      dataset = load_dataset('csv', data_files={'train': [train_data_name], 'test': test_data_name, 'validation' : validation_data_name})

      datasets[df.columns[1]] = dataset

   return datasets