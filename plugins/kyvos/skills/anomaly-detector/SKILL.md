---
name: anomaly-detector
description: Identify statistical anomalies, outliers, and unusual patterns in datasets. Use when users ask to find anomalies, detect outliers, identify unusual patterns, spot irregularities, or analyze data for unexpected behavior. Supports time-series analysis, distribution-based detection, and pattern recognition for numerical and categorical data.
---

# Anomaly Detector

This skill identifies anomalies in data using multiple statistical methods. It can detect unusual values in numerical data, unexpected shifts in time-series data, and rare occurrences in categorical data.

## Numerical Anomaly Detection

For numeric columns, anomalies are typically values that fall far from the central tendency of the data.

### Z-Score Method

This method is best for data that is approximately normally distributed. It measures how many standard deviations a data point is from the mean.

- A Z-score > 3 is generally considered an outlier.

```python
# Assumes data is in a pandas DataFrame 'df' and we're checking 'value' column
z_scores = (df['value'] - df['value'].mean()) / df['value'].std()
anomalies = df[abs(z_scores) > 3]
```

### IQR (Interquartile Range) Method

This method is robust to outliers and does not assume a normal distribution, making it suitable for skewed data. An anomaly is a value that falls outside the range defined by Q1 - 1.5*IQR and Q3 + 1.5*IQR.

```python
# Assumes data is in a pandas DataFrame 'df' and we're checking 'value' column
Q1 = df['value'].quantile(0.25)
Q3 = df['value'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
anomalies = df[(df['value'] < lower_bound) | (df['value'] > upper_bound)]
```

### Percentile Method

A simple method to identify extreme values by defining anomalies as values that fall in the top or bottom X% of the data.

```python
# Identify values in the bottom 1% or top 1%
anomalies = df[(df['value'] < df['value'].quantile(0.01)) |
              (df['value'] > df['value'].quantile(0.99))]
```

## Time-Series Anomaly Detection

For time-series data, anomalies can be sudden spikes/dips or deviations from a recurring pattern (seasonality).

### Moving Average Deviation

This method identifies values that deviate significantly from a rolling average, which helps smooth out short-term noise.

```python
# Assumes 'df' has a datetime index and a 'value' column
# Calculate 7-period moving average
df['moving_average'] = df['value'].rolling(window=7).mean()
# Calculate deviation from moving average
df['deviation'] = df['value'] - df['moving_average']
# Identify points with a large deviation (e.g., > 3 standard deviations of the deviation)
anomaly_threshold = df['deviation'].std() * 3
anomalies = df[abs(df['deviation']) > anomaly_threshold]
```

### Other Time-Series Methods

- **Seasonal Decomposition**: Separates a time series into trend, seasonal, and residual components. Anomalies are often found in the residual component.
- **Change Point Detection**: Identifies points in time where the statistical properties of the data (e.g., mean, variance) change significantly.

## Categorical Anomaly Detection

For categorical data, anomalies are often categories that appear with unusually low frequency.

### Frequency Analysis

Identify categories that are rare compared to others.

```python
# Assumes 'df' has a 'category' column
frequency = df['category'].value_counts(normalize=True)
# Identify categories that make up less than 1% of the data
rare_categories = frequency[frequency < 0.01].index.tolist()
anomalies = df[df['category'].isin(rare_categories)]
```

## Handling Anomalies

Do NOT automatically remove anomalies. Instead:

1.  **Investigate**: Is this a data entry error, a genuine but extreme value, or a sign of a different underlying process?
2.  **Data errors**: Fix or remove if they are clearly incorrect (e.g., negative age, future dates).
3.  **Genuine extremes**: Keep them, but consider using robust statistics (e.g., median instead of mean) for analysis. Report their existence and potential impact.
4.  **Segment**: If anomalies represent a distinct group (e.g., enterprise customers vs. individual users), analyze them as a separate segment.

Always report how anomalies were identified and handled.

## Common Use Cases

1.  **Quality control**: Detect manufacturing defects or measurement errors.
2.  **Sales analysis**: Identify unusual sales patterns or inventory issues.
3.  **Fraud detection**: Flag suspicious transactions or user behavior.
4.  **Sensor data**: Detect equipment failures or sensor malfunctions.
5.  **Business metrics**: Spot unexpected changes in KPIs or performance metrics.
