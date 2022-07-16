from pomegranate import *

# Weather node has no parent
weather = Node(DiscreteDistribution({
    "Hot": 0.7,
    "Warm": 0.1,
    "Chill": 0.2
}), name="weather")

# Track Ice_cream node is conditional on weather
Ice_cream = Node(ConditionalProbabilityTable([
    ["Hot", "burning desired", 0.25],
    ["Hot", "likely", 0.5],
    ["Hot", "not likely", 0.25],
    ["Warm", "burning desired", 0.05],
    ["Warm", "likely", 0.45],
    ["Warm", "not likely", 0.5],
    ["Chill", "burning desired", 0.15],
    ["Chill", "likely", 0.5],
    ["Chill", "not likely", 0.35],
    ], [weather.distribution]), name="Ice_cream")

# Track Delivery_fee node is conditional on weather
Delivery_fee = Node(ConditionalProbabilityTable([
    ["Hot", "high", 0.7],
    ["Hot", "fair", 0.2],
    ["Hot", "low", 0.1],
    ["Warm", "high", 0.3],
    ["Warm", "fair", 0.6],
    ["Warm", "low", 0.1],
    ["Chill", "high", 0.5],
    ["Chill", "fair", 0.3],
    ["Chill", "low", 0.2],
    ], [weather.distribution]), name="Delivery_fee")

# Track buy node is conditional on both Ice_cream and Delivery_fee
Buy = Node(ConditionalProbabilityTable([
    ["burning desired", "high", "yes", 0.5],
    ["burning desired", "high", "no", 0.5],
    ["burning desired", "fair", "yes", 0.8],
    ["burning desired", "fair", "no", 0.2],
    ["burning desired", "low", "yes", 0.95],
    ["burning desired", "low", "no", 0.05],
    ["likely", "high", "yes", 0.1],
    ["likely", "high", "no", 0.9],
    ["likely", "fair", "yes", 0.5],
    ["likely", "low", "yes", 0.6],
    ["likely", "fair", "no", 0.5],
    ["likely", "low", "no", 0.4],
    ["not likely", "high", "yes", 0.05],
    ["not likely", "high", "no", 0.95],
    ["not likely", "fair", "yes", 0.1],
    ["not likely", "fair", "no", 0.9],
    ["not likely", "low", "yes", 0.15],
    ["not likely", "low", "no", 0.85],
    ], [Ice_cream.distribution, Delivery_fee.distribution]), name="buy")

# Track Mood node is conditional on Delivery_fee
mood = Node(ConditionalProbabilityTable([
    ["high", "happy", 0.05],
    ["high", "sad", 0.4],
    ["high", "ok", 0.55],
    ["fair", "happy", 0.1],
    ["fair", "ok", 0.6],
    ["fair", "sad", 0.3],
    ["low", "happy", 0.3],
    ["low", "ok", 0.5],
    ["low", "sad", 0.2]
    ], [Delivery_fee.distribution]), name="mood")
# Track Argument node is conditional on both Buy and Mood
Argument = Node(ConditionalProbabilityTable([
    ["yes", "happy", "y", 0.08],
    ["yes", "happy", "n", 0.92],
    ["yes", "ok", "y", 0.1],
    ["yes", "ok", "n", 0.9],
    ["yes", "sad", "y", 0.4],
    ["yes", "sad", "n", 0.6],
    ["no", "happy", "y", 0.04],
    ["no", "happy", "n", 0.96],
    ["no", "ok", "y", 0.08],
    ["no", "ok", "n", 0.92],
    ["no", "sad", "y", 0.35],
    ["no", "sad", "n", 0.65],
    ], [Buy.distribution, mood.distribution]), name="Argument")

# Create a Bayesian Network and add states
model2 = BayesianNetwork()
model2.add_states(weather, Ice_cream, Delivery_fee, Buy, mood, Argument)
# Add edges connecting nodes
model2.add_edge(weather, Ice_cream)
model2.add_edge(weather, Delivery_fee)
model2.add_edge(Ice_cream, Buy)
model2.add_edge(Delivery_fee, Buy)
model2.add_edge(Delivery_fee, mood)
model2.add_edge(Buy, Argument)
model2.add_edge(mood, Argument)

# Finalize model
model2.bake()
