from model_02 import model2

# Calculate predictions
predictions = model2.predict_proba({
    "Delivery_fee": "fair"
})

# Print predictions for each node
for node, prediction in zip(model2.states, predictions):
    if isinstance(prediction, str):
        print(f"{node.name}: {prediction}")
    else:
        print(f"{node.name}")
        for value, probability in prediction.parameters[0].items():
            print(f"    {value}: {probability:.4f}")
