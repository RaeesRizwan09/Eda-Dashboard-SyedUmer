# filters.py
"""filters.py — High-Performance Filter Pipeline for Onyx Coffee Lab"""
import pandas as pd

def apply_filters(
    df: pd.DataFrame,
    countries: list,
    species: list,
    processing: list,
    score_range: tuple,
    altitude_range: tuple,
) -> pd.DataFrame:
    out = df.copy()

    if countries:
        out = out[out["country_of_origin"].isin(countries)]
    if species:
        out = out[out["species"].isin(species)]
    if processing:
        out = out[out["processing_method"].isin(processing)]
    if score_range:
        out = out[(out["total_cup_points"] >= score_range[0]) &
                  (out["total_cup_points"] <= score_range[1])]
    if altitude_range and "altitude_mean_meters" in out.columns:
        # Filter missing altitudes only if a strict range subset is selected
        out = out[out["altitude_mean_meters"].isna() | 
                  ((out["altitude_mean_meters"] >= altitude_range[0]) & 
                   (out["altitude_mean_meters"] <= altitude_range[1]))]
    return out