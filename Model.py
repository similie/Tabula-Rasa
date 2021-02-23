import numpy as np

# DEEP LEARNING MODEL
from keras.models import Sequential, load_model
from keras.layers import Dense, LSTM

from sklearn.metrics import mean_squared_error

if __name__ == "__model_training__":
    model_training ()

def model_training (full_training,
                    X_data_shape_0, 
                    X_data_shape_1,
                    y_data_shape_1,
                    X_data_reshaped,
                    y_data_scaled,
                    epochs,
                    batch_size,
                    X_shift_reshaped,
                    model_path,
                    model_weights_path,
                    y_scaler):

    if full_training is True:

        print ("EXECUTE FULL TRAINING")

        #CREATE LONG SHORT TERM MEMORY RECURRENT NEURAL NETWORK
        model = Sequential()
        #Adding the first LSTM layer 
        model.add(LSTM(units = 50, return_sequences = True, input_shape = (X_data_shape_0, X_data_shape_1)))
        #model.add(Dropout(0.2))  # model seems to work best without dropout layers
        # Second LSTM layer 
        model.add(LSTM(units = 50, return_sequences = True))
        # Third LSTM layer 
        model.add(LSTM(units = 50, return_sequences = True))
        # Adding a fourth LSTM layer 
        model.add(LSTM(units = 50))
        # Adding the output layer
        model.add(Dense(units = y_data_shape_1, activation = 'relu'))  # relu function keeps the model from giving negative outputs
        # Compiling the RNN
        model.compile(optimizer = 'adam', loss = 'mean_squared_error', metrics=['accuracy'])

        # Fitting the RNN to the Training set
        model.fit(X_data_reshaped, y_data_scaled, epochs = epochs, batch_size = batch_size)
        model.summary()

        # Save Model
        model.save(model_path)
        model.save_weights(model_weights_path)
        
        predictions = model.predict(X_shift_reshaped)
        predictions = np.squeeze(predictions)
        predictions = y_scaler.inverse_transform(predictions)
    
    elif full_training is False:

        print ("EXECUTE RE-TRAINING")
        
        #Loads previously saved model
        model = load_model(model_path)
        model.summary()

        #RE-FITS NEW DATA
        model.fit(X_data_reshaped, y_data_scaled, epochs = epochs, batch_size = batch_size)
        predictions = model.predict(X_shift_reshaped)
        predictions = np.squeeze(predictions)
        predictions = y_scaler.inverse_transform(predictions)

    else:
        print("Error: Full Training variable is invalid")
        quit()
    
    return predictions