# Time-Series Anomaly Detection Methods

This reference provides detailed implementation guidance for time-series specific anomaly detection.

## When to Use Time-Series Methods

Use time-series methods when:
- Data has a date/time component
- You need to detect temporal patterns (trends, seasonality)
- Anomalies depend on historical context
- Looking for sudden changes or breaks in patterns

## Core Techniques

### 1. Moving Average Deviation

Detect values that deviate significantly from their moving average:

```python
def moving_average_anomaly(series, window=7, threshold=2.5):
    """Detect anomalies using moving average deviation"""
    ma = series.rolling(window=window, center=True).mean()
    std = series.rolling(window=window, center=True).std()
    
    z_scores = np.abs((series - ma) / std)
    anomalies = z_scores > threshold
    
    return anomalies
```

**Best for:** Detecting sudden spikes or drops in relatively stable data
**Window size:** 7 days for daily data, 12 months for monthly data

### 2. Seasonal Decomposition

Separate trend, seasonal, and residual components:

```python
from statsmodels.tsa.seasonal import seasonal_decompose

def seasonal_anomaly_detection(series, freq):
    """Decompose and detect anomalies in residuals"""
    decomposition = seasonal_decompose(series, model='additive', period=freq)
    
    residuals = decomposition.resid.dropna()
    threshold = 3 * residuals.std()
    
    anomalies = np.abs(residuals) > threshold
    return anomalies
```

**Best for:** Data with clear seasonal patterns (monthly sales, yearly trends)
**Frequency:** 7 for weekly patterns, 30 for monthly, 365 for yearly

### 3. Change Point Detection

Identify where the data distribution fundamentally changes:

```python
def detect_change_points(series, window=10):
    """Detect significant changes in mean/variance"""
    changes = []
    
    for i in range(window, len(series) - window):
        before = series[i-window:i]
        after = series[i:i+window]
        
        # T-test for mean change
        t_stat, p_value = stats.ttest_ind(before, after)
        
        if p_value < 0.01:  # Significant change
            changes.append(i)
    
    return changes
```

**Best for:** Identifying structural breaks, regime changes
**Use cases:** Policy changes, market shifts, equipment failures

### 4. Rate of Change Analysis

Detect unusually rapid changes:

```python
def rate_of_change_anomaly(series, threshold=0.5):
    """Detect anomalous rate of change"""
    pct_change = series.pct_change()
    
    # Flag changes > threshold % (e.g., 50% increase/decrease)
    anomalies = np.abs(pct_change) > threshold
    
    return anomalies
```

**Best for:** Financial data, sensor readings, traffic analysis
**Threshold:** 0.2 (20%) for sensitive, 0.5 (50%) for moderate, 1.0 (100%) for extreme

## Pattern-Specific Detection

### Spike Detection

Identify sudden short-term increases:

```python
def detect_spikes(series, baseline_window=7, spike_threshold=3):
    """Detect short-term spikes"""
    baseline = series.rolling(window=baseline_window).median()
    baseline_std = series.rolling(window=baseline_window).std()
    
    z_scores = (series - baseline) / baseline_std
    spikes = z_scores > spike_threshold
    
    return spikes
```

### Dip Detection

Identify sudden short-term decreases:

```python
def detect_dips(series, baseline_window=7, dip_threshold=-3):
    """Detect short-term dips"""
    baseline = series.rolling(window=baseline_window).median()
    baseline_std = series.rolling(window=baseline_window).std()
    
    z_scores = (series - baseline) / baseline_std
    dips = z_scores < dip_threshold
    
    return dips
```

## Advanced: Multi-variate Time-Series

For datasets with multiple related time-series:

```python
def multivariate_ts_anomaly(df, date_col, value_cols):
    """Detect anomalies across multiple correlated series"""
    from sklearn.ensemble import IsolationForest
    
    # Prepare data
    features = df[value_cols].values
    
    # Isolation Forest for multivariate detection
    clf = IsolationForest(contamination=0.05, random_state=42)
    predictions = clf.fit_predict(features)
    
    # -1 indicates anomaly
    anomaly_mask = predictions == -1
    
    return anomaly_mask
```

## Practical Guidelines

### Choosing Window Sizes

- **Short window (3-7):** Captures recent trends, sensitive to short-term changes
- **Medium window (7-14):** Balanced, good for weekly patterns
- **Long window (30+):** Smooths out noise, captures long-term trends

### Handling Seasonality

1. **Remove seasonality first** if it's strong and predictable
2. **Apply anomaly detection to residuals** after decomposition
3. **Use seasonal-aware methods** for data with multiple seasonal patterns

### Missing Data

- **Forward fill:** For sparse data with stable values
- **Interpolation:** For smooth continuous data
- **Seasonal average:** For data with seasonal patterns
- **Remove:** If too many gaps (>20% missing)

## Performance Tips

1. **Downsample** large datasets before analysis (hourly to daily)
2. **Batch process** by time chunks for memory efficiency
3. **Cache rolling statistics** for repeated queries
4. **Use vectorized operations** instead of loops
