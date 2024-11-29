import torch
import torch.nn as nn


class LSTMRegressor(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(LSTMRegressor, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)  # LSTM layer
        self.fc = nn.Linear(hidden_size, output_size)  # Fully connected layer to output regression

    def forward(self, x, predicted_days=90):
        # x is of shape (batch_size, sequence_length, input_size)
        x, _ = self.lstm(x)  # Get the last hidden state
        out = self.fc(x[:,-predicted_days:,:])  # Use the last hidden state to predict
        return out