import turicreate as tc

# Load the data
data = tc.SFrame('qrs.sframe')

# Make a train-test split
train_data, test_data = data.random_split(0.8)

# Create a model
model = tc.object_detector.create(train_data)

# Save predictions to an SArray
predictions = model.predict(test_data)

# Evaluate the model and save the results into a dictionary
metrics = model.evaluate(test_data)
print(metrics)

# Save the model for later use in Turi Create
model.save('qrs.model')

# Export for use in Core ML
model.export_coreml('QRsObjectDetector.mlmodel')