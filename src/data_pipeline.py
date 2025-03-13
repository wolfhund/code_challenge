"""
Contains the data processing pipeline using pandas.
Demonstrates .merge, .pivot_table, .melt, and .groupby.
"""

import pandas as pd
from typing import List
from src.data_models import DataItem, ProcessedItem

def process_data(raw_data: List[DataItem]) -> List[ProcessedItem]:
    """
    Processes the raw data using pandas transformations:
      1. Convert list of DataItem to a pandas DataFrame.
      2. Merge with a small static DataFrame that maps `id` to a `name`.
      3. Use pivot_table to get mean values by 'id' and 'metric' over time.
      4. Melt the pivoted data back to long format.
      5. Groupby to confirm aggregated results (demonstration).
    Returns a list of ProcessedItem for the final data.
    """
    if not raw_data:
        return []

    # Convert raw data to DataFrame
    df = pd.DataFrame([item.dict() for item in raw_data])

    # Create a static DataFrame to demonstrate merging
    # This simulates some reference data that might exist elsewhere
    reference_data = {
        "id": list(range(10)),  # Suppose we have 10 known IDs
        "name": [f"Item-{i}" for i in range(10)]
    }
    df_ref = pd.DataFrame(reference_data)

    # Merge the raw data with reference data on 'id'
    merged_df = df.merge(df_ref, on="id", how="left")

    # For demonstration, pivot the data to get mean of 'value_a' and 'value_b'
    # by timestamp and id, then re-melt
    pivot_df = merged_df.pivot_table(
        index=["timestamp", "id", "name"],
        values=["value_a", "value_b"],
        aggfunc="mean"  # average by default
    )

    # Reset index so we can melt properly
    pivot_df.reset_index(inplace=True)

    # Melt pivot_df so we have a 'metric' column for either 'value_a' or 'value_b'
    melted_df = pd.melt(
        pivot_df,
        id_vars=["timestamp", "id", "name"],
        value_vars=["value_a", "value_b"],
        var_name="metric",
        value_name="mean_value"
    )

    # Example groupby (not strictly necessary, but demonstrates usage)
    # We'll group by 'id', 'name', 'metric' to get an overall mean
    grouped = melted_df.groupby(["id", "name", "metric"], as_index=False)["mean_value"].mean()

    # Convert to list of ProcessedItem
    processed_items = [
        ProcessedItem(
            id=int(row["id"]),
            name=str(row["name"]) if row["name"] else "Unknown",
            metric=str(row["metric"]),
            mean_value=float(row["mean_value"])
        )
        for _, row in grouped.iterrows()
    ]

    return processed_items
