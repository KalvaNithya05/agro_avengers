import statistics

def aggregate_data(readings):
    """
    Aggregates a list of sensor reading dictionaries.
    Calculates Mean for Temp, Humidity, pH, NPK.
    Calculates Sum for Rainfall (if present).
    
    :param readings: List of dicts, e.g. [{'temperature': 25.0, ...}, ...]
    :return: Dict with aggregated values.
    """
    if not readings:
        return None

    # Fields to average
    mean_keys = ['temperature', 'humidity', 'ph', 'nitrogen', 'phosphorus', 'potassium']
    # Fields to sum
    sum_keys = ['rainfall']
    
    agg = {}
    
    # Calculate Means
    for key in mean_keys:
        values = [r.get(key) for r in readings if r.get(key) is not None]
        if values:
            agg[key] = round(statistics.mean(values), 2)
        else:
            agg[key] = None
            
    # Calculate Sums
    for key in sum_keys:
        values = [r.get(key) for r in readings if r.get(key) is not None]
        if values:
            agg[key] = round(sum(values), 2)
        else:
            agg[key] = 0.0

    return agg

if __name__ == "__main__":
    # Test with stub data
    data = [
        {'temperature': 25, 'humidity': 60, 'ph': 6.5, 'nitrogen': 50, 'phosphorus': 20, 'potassium': 100, 'rainfall': 0},
        {'temperature': 27, 'humidity': 55, 'ph': 6.6, 'nitrogen': 52, 'phosphorus': 22, 'potassium': 105, 'rainfall': 5}
    ]
    print(f"Aggregated: {aggregate_data(data)}")
