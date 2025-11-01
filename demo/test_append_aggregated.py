from synthcast.simulation import results

sample = [
    {"id": 1, "response": "Yes"},
    {"id": 2, "response": "No"},
    {"id": 3, "response": "Yes"},
]

path = results.save_simulation_results(sample, question="Do you like X?", country_code="TST")
print("saved:", path)
print("aggregated datapoints count:")
print(len(results.load_aggregated_datapoints()))
print("last datapoint:")
print(results.load_aggregated_datapoints()[-1])
