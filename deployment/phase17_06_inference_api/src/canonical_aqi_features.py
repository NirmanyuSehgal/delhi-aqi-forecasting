"""Canonical Delhi AQI feature builder extracted from the parity notebook."""

import numpy as np
import pandas as pd

RAW_FEATURES = ['AQI', 'PM2.5', 'PM10', 'NO', 'NO2', 'NOx', 'NH3', 'CO', 'SO2', 'O3', 'Benzene', 'Toluene']
BASE_COLUMNS = ['StationId', 'StationName', 'Datetime'] + RAW_FEATURES
TARGET = 'AQI_t_plus_1'
DIWALI_DATES = pd.to_datetime(['2015-11-11', '2016-10-30', '2017-10-19', '2018-11-07', '2019-10-27', '2020-11-14'])

def is_diwali_window(timestamp, days_before=2, days_after=2):
    timestamp = pd.Timestamp(timestamp)
    return int(any((timestamp >= date - pd.Timedelta(days=days_before) and timestamp <= date + pd.Timedelta(days=days_after) for date in DIWALI_DATES)))

def build_canonical_features(history_df):
    """
    Canonical t -> t+1 feature builder.

    The same function is intended for:
      1. historical model training
      2. historical live-style testing
      3. future CPCB/OGD inference

    All predictors for timestamp t use information
    available at or before t.
    """
    df = history_df[BASE_COLUMNS].copy()
    df['Datetime'] = pd.to_datetime(df['Datetime'])
    df['StationId'] = df['StationId'].astype(str)
    df = df.sort_values(['StationId', 'Datetime']).drop_duplicates(['StationId', 'Datetime'], keep='first').reset_index(drop=True)
    output_parts = []
    for station_id, station_group in df.groupby('StationId', sort=False):
        station = station_group.sort_values('Datetime').copy().reset_index(drop=True)
        station['Hour'] = station['Datetime'].dt.hour
        station['Day'] = station['Datetime'].dt.day
        station['Month'] = station['Datetime'].dt.month
        station['Year'] = station['Datetime'].dt.year
        station['DayOfWeek'] = station['Datetime'].dt.dayofweek
        station['IsWeekend'] = (station['DayOfWeek'] >= 5).astype('int8')
        station['IsStubbleSeason'] = station['Month'].isin([10, 11]).astype('int8')
        station['IsDiwaliWindow'] = station['Datetime'].apply(is_diwali_window).astype('int8')
        for lag in [1, 2, 12]:
            lag_source = station[['Datetime'] + RAW_FEATURES].copy()
            lag_source['Datetime'] = lag_source['Datetime'] + pd.Timedelta(hours=lag)
            lag_source = lag_source.rename(columns={column: f'{column}_lag_{lag}h' for column in RAW_FEATURES})
            station = station.merge(lag_source[['Datetime'] + [f'{column}_lag_{lag}h' for column in RAW_FEATURES]], on='Datetime', how='left', validate='one_to_one')
        rolling_source = station[['Datetime', 'AQI', 'PM2.5', 'PM10', 'NO2']].drop_duplicates('Datetime').set_index('Datetime').sort_index()
        for column in ['AQI', 'PM2.5', 'PM10', 'NO2']:
            station[f'{column}_rolling_mean_3h'] = rolling_source[column].rolling('3h', min_periods=1).mean().to_numpy()
            station[f'{column}_rolling_std_3h'] = rolling_source[column].rolling('3h', min_periods=2).std().to_numpy()
            station[f'{column}_rolling_mean_12h'] = rolling_source[column].rolling('12h', min_periods=1).mean().to_numpy()
            station[f'{column}_rolling_std_12h'] = rolling_source[column].rolling('12h', min_periods=2).std().to_numpy()
        future_aqi = station[['Datetime', 'AQI']].copy()
        future_aqi['Datetime'] = future_aqi['Datetime'] - pd.Timedelta(hours=1)
        future_aqi = future_aqi.rename(columns={'AQI': TARGET})
        future_aqi = future_aqi[['Datetime', TARGET]]
        station = station.merge(future_aqi, on='Datetime', how='left', validate='one_to_one')
        output_parts.append(station)
    result = pd.concat(output_parts, ignore_index=True)
    if result.columns.duplicated().any():
        duplicated_columns = result.columns[result.columns.duplicated()].tolist()
        raise ValueError(f'Duplicate columns remain: {duplicated_columns}')
    return result.sort_values(['StationId', 'Datetime']).reset_index(drop=True)
