import torch
from transformers import BertTokenizer, BertForSequenceClassification

# Set the device (CPU or GPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Set the BERT tokenizer and model
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertForSequenceClassification.from_pretrained('bert-base-uncased')
model.to(device)

# Set the input text and labels
input_text = ["This is a positive example.", "This is a negative example."]
labels = [1, 0]

# Tokenize the input text
input_ids = [tokenizer.encode(sent, add_special_tokens=True) for sent in input_text]

# Set the attention masks
attention_masks = [[int(i>0) for i in seq] for seq in input_ids]

# Convert the inputs to PyTorch tensors
input_ids = torch.tensor(input_ids)
attention_masks = torch.tensor(attention_masks)
labels = torch.tensor(labels)

# Set the batch size
batch_size = 32

# Create the DataLoader
prediction_data = TensorDataset(input_ids, attention_masks, labels)
prediction_sampler = SequentialSampler(prediction_data)
prediction_dataloader = DataLoader(prediction_data, sampler=prediction_sampler, batch_size=batch_size)

# Set the optimizer and learning rate
optimizer = AdamW(model.parameters(), lr=2e-5, correct_bias=False)

# Train the model
for epoch in range(1, epochs+1):
  # Set the model to training mode
  model.train()
  
  # Track the training progress
  train_loss = 0
  
  # Train the model for each batch
  for step, batch in enumerate(prediction_dataloader):
    # Unpack the inputs from the DataLoader
    b_input_ids = batch[0].to(device)
    b_input_mask = batch[1].to(device)
    b_labels = batch[2].to(device)

    # Clear any previous gradients
    optimizer.zero_grad()        

    # Forward pass
    loss = model(b_input_ids, token_type_ids=None, attention_mask=b_input_mask, labels=b_labels)

    # Backward pass
    loss.backward()

    # Update the weights
    optimizer.step()

    # Update the training loss
    train_loss += loss.item()
  
  # Print the training loss
  print('Epoch: {}, Training Loss: {}'.format(epoch, train_loss/len(prediction_dataloader)))

# Save the trained model
model.save_pretrained('/path/to/save/directory')
