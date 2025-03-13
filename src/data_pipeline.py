import pandas as pd
from typing import List
from .data_models import DataPoint

def process_data(data: List[DataPoint]):
    if not data:
        return []
    
    # Convert to DataFrame
    df = pd.DataFrame([d.dict() for d in data])
    
    # Group by category
    grouped = df.groupby('category').agg({
        'value': ['mean', 'count'],
        'timestamp': 'max'
    })
    
    # Format results
    results = []
    for category in grouped.index:
        results.append({
            'category': category,
            'avg_value': grouped.loc[category, ('value', 'mean')],
            'count': int(grouped.loc[category, ('value', 'count')]),
            'last_timestamp': grouped.loc[category, ('timestamp', 'max')]
        })
    
    return results
