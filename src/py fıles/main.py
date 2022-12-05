from load_file import load_file
from preprocess import preprocess

labels = ['fraud', 'hacker groups', 'government', 'corporation',
       'unrelated', 'darknet', 'cyber defense', 'hacking', 'security concepts',
       'security products', 'network security', 'cyberwar', 'geopolitical',
       'data breach', 'vulnerability', 'platform', 'cyber attack']

# id2label = {idx:label for idx, label in enumerate(labels)}
# label2id = {label:idx for idx, label in enumerate(labels)}

def main():
   datasets = load_file("/Users/cankrmn/Desktop/ENS 492 Bert venv/src/reduced_dataset[0,1000].csv", True)
   print(datasets)
   
   for label in labels:
      dataset = datasets[label]
      # print(dataset['train'].column_names)
      encoded_dataset = dataset.map(lambda x : print("1", x), batched=True, remove_columns=dataset['train'].column_names)
      print("2", encoded_dataset)
      break
      

if __name__ == "__main__":
   main()