import pickle
import pandas as pd

# Load the pickled model
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

new_data = pd.DataFrame({
    'CROP TYPE': [3],
    'SOIL TYPE': [2],
    'REGION': [2],
    'TEMPERATURE GROUP': [3],
    'WEATHER CONDITION': [4]
})


prediction = model.predict(new_data)

print(prediction[0])