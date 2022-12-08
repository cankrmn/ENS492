import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
# Text pre-processing
import tensorflow as tf
from keras.preprocessing.text import Tokenizer
from keras.utils import pad_sequences
from keras.callbacks import EarlyStopping
# Modeling
from keras.models import Sequential
from keras.layers import LSTM, Dense, Embedding, Dropout,SpatialDropout1D
from keras.models import load_model



main_df = pd.read_csv('Src/reduced_dataset[0,1000].csv')


dfs = [main_df[["raw_text",col]] for col in main_df][2:3] # creates a dataframe for each label

def train(df, label_name):
    #df = pd.read_csv("./corporation_train_data.csv")
    df['text_length'] = df['raw_text'].apply(len)

    msg_label = df[label_name].values
    x_train, x_test, y_train, y_test = train_test_split(df['raw_text'], msg_label, test_size=0.2, random_state=434)

    max_len = 1000 
    trunc_type = 'post'
    padding_type = 'post'
    oov_tok = '<OOV>' # out of vocabulary token
    vocab_size = 500

    tokenizer = Tokenizer(num_words = vocab_size, 
                        char_level = False,
                        oov_token = oov_tok)
    tokenizer.fit_on_texts(x_train)
    word_index = tokenizer.word_index
    total_words = len(word_index)

    training_sequences = tokenizer.texts_to_sequences(x_train)
    training_padded = pad_sequences(training_sequences,
                                    maxlen = max_len,
                                    padding = padding_type,
                                    truncating = trunc_type)


    testing_sequences = tokenizer.texts_to_sequences(x_test)
    testing_padded = pad_sequences(testing_sequences,
                                maxlen = max_len,
                                padding = padding_type,
                                truncating = trunc_type)

    # Define parameter
    vocab_size = 500 
    embedding_dim = 16
    drop_value = 0.2
    n_dense = 24

    # Define parameter
    n_lstm = 128
    drop_lstm = 0.2
    # Define LSTM Model 
    model = Sequential()
    model.add(Embedding(vocab_size, embedding_dim, input_length=max_len))
    model.add(SpatialDropout1D(drop_lstm))
    model.add(LSTM(n_lstm, return_sequences=False))
    model.add(Dropout(drop_lstm))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(loss = 'binary_crossentropy',
                optimizer = 'adam',
                metrics = ['accuracy'])

    num_epochs = 30
    early_stop = EarlyStopping(monitor='val_loss', patience=2)
    history = model.fit(training_padded,
                        y_train,
                        epochs=num_epochs, 
                        validation_data=(testing_padded, y_test),
                        callbacks =[early_stop],
                        verbose=2)
    train_dense_results = model.evaluate(training_padded, np.asarray(y_train), verbose=2, batch_size=256)
    valid_dense_results = model.evaluate(testing_padded, np.asarray(y_test), verbose=2, batch_size=256)
    print("This results are for " + label_name)
    print(f'Train accuracy: {train_dense_results[1]*100:0.2f}')
    print(f'Valid accuracy: {valid_dense_results[1]*100:0.2f}')
    
    model.save(label_name+"model")

def predict(input_text, model):
    max_len=1000
    # Tokenize the input text
    tokenizer = Tokenizer()
    tokenizer.fit_on_texts(input_text)
    encoded_text = tokenizer.texts_to_sequences(input_text)

    # Pad the input text to the correct length
    padded_text = pad_sequences(encoded_text, maxlen=max_len)

    # Use the model to make predictions on the input text
    predictions = model.predict(padded_text)
    print(predictions)


input_text = ["hey hello how are you","FRAUD fraud Fraud detected in a system"]

for df in dfs:
    #train(df,df.columns[1])
    get_model = load_model('./fraudmodel')
    predict(input_text, get_model)

