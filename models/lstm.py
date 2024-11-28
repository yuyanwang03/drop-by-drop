from sklearn.preprocessing import MinMaxScaler
import torch
import torch.nn as nn
import numpy as np
import pandas as pd
import pickle
from datetime import timedelta


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
    

def inference(data_x, predicted_days, model_path):
    with open(model_path, 'rb') as model_file:
        compact_model = pickle.load(model_file)

    scaler_x = compact_model[1][0]
    scaler_y = compact_model[1][1]
    model = compact_model[0]


    scaled_x = scaler_x.transform(data_x)
    scaled_df_x = pd.DataFrame(scaled_x, columns=data_x.columns)

    # Convert to NumPy array
    X = scaled_df_x.to_numpy()  # Shape: (n_rows, n_columns)
    # Reshape to (1, n_rows, n_columns)
    X = X[np.newaxis, :, :]

    # Convert to PyTorch tensors
    X_tensor = torch.tensor(X, dtype=torch.float32)

    # Evaluate the model on test data
    model.eval()
    with torch.no_grad():
        predictions = model(X_tensor, predicted_days).squeeze() 
        predictions_rescaled = scaler_y.inverse_transform(predictions.detach().numpy().reshape(-1, 1))

    return predictions_rescaled

def inference_per_district(df, predicted_days, models_path="./"):

    consumption = {}
    df_grouped = df.groupby(['Date', 'District']).agg(
        n_meters=('Number of Meters', 'sum'),
        accumulated_consumption=('Accumulated Consumption', 'sum'),
        max_temperature=('temp_max', 'first'), 
        min_temperature=('temp_min', 'first'), 
        precipitation=('precipitacion', 'first'),
        pernoctacion=('pernoctacions', 'first'),
        population=('Population', 'first')
    ).reset_index()

    for idx in range(1,11):
        model_path = f"{models_path}model_{idx}.pkl"
        df_district = df_grouped[df_grouped["District"] == idx]
        df_district_x = df_district[["n_meters", "max_temperature", "min_temperature", "precipitation", "pernoctacion", "population"]]

        consumption[idx] = inference(df_district_x, predicted_days, model_path)

    df['Date'] = pd.to_datetime(df['Date'])

    # Find the latest date
    latest_date = df['Date'].max()
    start_prediction_date = latest_date - timedelta(days=predicted_days-1)

    rows = []

    # Iterate through the dictionary and create the rows
    for district_id, consumption_values in consumption.items():
        # Create a DataFrame for the current district's consumption values
        district_df = pd.DataFrame(consumption_values, columns=['Consumption'])
        district_df['District'] = district_id
        # Generate Date column starting from new_date, incremented by one day per entry
        district_df['Date'] = [start_prediction_date + pd.Timedelta(days=i) for i in range(len(district_df))]

        rows.append(district_df)

    final_df = pd.concat(rows, ignore_index=True)


    return final_df