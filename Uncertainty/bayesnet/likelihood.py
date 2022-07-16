from model import model

# Calculate probability for a given observation
probability = model.probability([["none", "yes", "on time", "attend"]])

print(probability)
