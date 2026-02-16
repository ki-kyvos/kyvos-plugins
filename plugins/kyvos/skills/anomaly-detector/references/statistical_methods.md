# Statistical Anomaly Detection Methods

Comprehensive reference for statistical approaches to anomaly detection in tabular data.

## Method Selection Guide

| Method | Data Type | Distribution | Best For | Speed |
|--------|-----------|--------------|----------|-------|
| Z-Score | Numerical | Normal | Quick detection, symmetric data | Very Fast |
| Modified Z-Score | Numerical | Any | Robust to outliers | Fast |
| IQR | Numerical | Any | Skewed distributions | Very Fast |
| Isolation Forest | Numerical | Any | High-dimensional data | Medium |
| Local Outlier Factor | Numerical | Any | Density-based clusters | Slow |
| DBSCAN | Numerical | Any | Spatial clusters | Medium |
| Grubbs' Test | Numerical | Normal | Single outlier detection | Fast |

## Core Statistical Methods

### 1. Z-Score Method

**Formula:** `z = (x - μ) / σ`

**Implementation:**
```python
from scipy import stats
import numpy as np

def zscore_anomaly(data, threshold=3.0):
    """Standard Z-score anomaly detection"""
    z_scores = np.abs(stats.zscore(data))
    anomalies = z_scores > threshold
    return anomalies, z_scores
```

**Thresholds:**
- 2.0: Very sensitive (≈5% false positives)
- 2.5: Balanced (≈1% false positives)
- 3.0: Conservative (≈0.3% false positives)
- 4.0: Very conservative (≈0.006% false positives)

**Assumptions:**
- Data is normally distributed
- Mean and std are not influenced by outliers
- Works best with 30+ samples

**Limitations:**
- Sensitive to extreme outliers
- Assumes Gaussian distribution
- Not suitable for multimodal data

### 2. Modified Z-Score (Median Absolute Deviation)

**Formula:** `modified_z = 0.6745 * (x - median) / MAD`

**Implementation:**
```python
def modified_zscore_anomaly(data, threshold=3.5):
    """Robust Z-score using MAD"""
    median = np.median(data)
    mad = np.median(np.abs(data - median))
    
    if mad == 0:
        return np.zeros(len(data), dtype=bool)
    
    modified_z = 0.6745 * (data - median) / mad
    anomalies = np.abs(modified_z) > threshold
    
    return anomalies
```

**Advantages:**
- Robust to extreme outliers
- Doesn't assume normal distribution
- Better for skewed data

**Threshold:** 3.5 is standard (equivalent to 3.0 in regular Z-score)

### 3. IQR (Interquartile Range) Method

**Formula:** Outliers outside `[Q1 - 1.5*IQR, Q3 + 1.5*IQR]`

**Implementation:**
```python
def iqr_anomaly(data):
    """IQR-based outlier detection"""
    Q1 = np.percentile(data, 25)
    Q3 = np.percentile(data, 75)
    IQR = Q3 - Q1
    
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    anomalies = (data < lower_bound) | (data > upper_bound)
    return anomalies, (lower_bound, upper_bound)
```

**Multiplier Variations:**
- 1.5: Standard (moderate outliers)
- 3.0: Extreme outliers only
- 1.0: More sensitive

**Advantages:**
- No distribution assumptions
- Easy to interpret
- Works well with skewed data

**Use Cases:**
- Sales data (often right-skewed)
- Response times
- Financial transactions

### 4. Grubbs' Test

Single outlier detection for normally distributed data:

```python
from scipy.stats import t

def grubbs_test(data, alpha=0.05):
    """Grubbs test for single outlier"""
    n = len(data)
    mean = np.mean(data)
    std = np.std(data, ddof=1)
    
    # Calculate G statistic
    abs_diff = np.abs(data - mean)
    max_idx = np.argmax(abs_diff)
    G = abs_diff[max_idx] / std
    
    # Critical value
    t_dist = t.ppf(1 - alpha / (2 * n), n - 2)
    G_critical = ((n - 1) * np.sqrt(np.square(t_dist))) / (np.sqrt(n) * np.sqrt(n - 2 + np.square(t_dist)))
    
    is_outlier = G > G_critical
    
    return is_outlier, max_idx if is_outlier else None
```

**Use Case:** When you suspect exactly one outlier in normally distributed data

### 5. Percentile-Based Detection

Simple threshold using percentiles:

```python
def percentile_anomaly(data, lower=1, upper=99):
    """Flag values outside percentile range"""
    lower_bound = np.percentile(data, lower)
    upper_bound = np.percentile(data, upper)
    
    anomalies = (data < lower_bound) | (data > upper_bound)
    return anomalies
```

**Recommended Percentiles:**
- 1st and 99th: Top/bottom 1% (conservative)
- 5th and 95th: Top/bottom 5% (moderate)
- 10th and 90th: Top/bottom 10% (sensitive)

## Machine Learning Methods

### Isolation Forest

Efficient for high-dimensional data:

```python
from sklearn.ensemble import IsolationForest

def isolation_forest_anomaly(data, contamination=0.05):
    """Isolation Forest for complex patterns"""
    clf = IsolationForest(
        contamination=contamination,
        random_state=42,
        n_estimators=100
    )
    
    predictions = clf.fit_predict(data.reshape(-1, 1))
    anomalies = predictions == -1
    scores = clf.score_samples(data.reshape(-1, 1))
    
    return anomalies, scores
```

**Contamination:** Expected proportion of outliers (0.01 to 0.1)

### Local Outlier Factor (LOF)

Density-based anomaly detection:

```python
from sklearn.neighbors import LocalOutlierFactor

def lof_anomaly(data, n_neighbors=20, contamination=0.05):
    """LOF for density-based detection"""
    clf = LocalOutlierFactor(
        n_neighbors=n_neighbors,
        contamination=contamination
    )
    
    predictions = clf.fit_predict(data.reshape(-1, 1))
    anomalies = predictions == -1
    scores = clf.negative_outlier_factor_
    
    return anomalies, scores
```

**Neighbors:** 
- Small (5-10): Detects local anomalies
- Large (20-50): Detects global anomalies

## Multivariate Methods

### Mahalanobis Distance

For correlated features:

```python
from scipy.spatial.distance import mahalanobis

def mahalanobis_anomaly(data, threshold=3):
    """Detect anomalies using Mahalanobis distance"""
    mean = np.mean(data, axis=0)
    cov = np.cov(data.T)
    inv_cov = np.linalg.inv(cov)
    
    distances = []
    for point in data:
        dist = mahalanobis(point, mean, inv_cov)
        distances.append(dist)
    
    distances = np.array(distances)
    anomalies = distances > threshold
    
    return anomalies, distances
```

**Use Case:** Multiple correlated numerical features

## Categorical Data Methods

### Frequency-Based Detection

```python
def frequency_anomaly(data, min_count=5, min_freq=0.01):
    """Detect rare categories"""
    value_counts = pd.Series(data).value_counts()
    total = len(data)
    
    rare_categories = []
    for value, count in value_counts.items():
        freq = count / total
        if count < min_count or freq < min_freq:
            rare_categories.append(value)
    
    anomalies = pd.Series(data).isin(rare_categories)
    return anomalies
```

### Chi-Square Test

For categorical distributions:

```python
from scipy.stats import chi2_contingency

def chi_square_anomaly(observed, expected):
    """Test if distribution is anomalous"""
    chi2, p_value, dof, expected_freq = chi2_contingency([observed, expected])
    
    is_anomalous = p_value < 0.05  # 5% significance
    return is_anomalous, p_value
```

## Combination Strategies

### Ensemble Voting

Combine multiple methods:

```python
def ensemble_anomaly(data, threshold=2):
    """Majority voting across methods"""
    # Run multiple methods
    z_anom, _ = zscore_anomaly(data)
    iqr_anom, _ = iqr_anomaly(data)
    iso_anom, _ = isolation_forest_anomaly(data)
    
    # Stack results
    votes = np.column_stack([z_anom, iqr_anom, iso_anom])
    vote_count = np.sum(votes, axis=1)
    
    # Flag if at least 'threshold' methods agree
    anomalies = vote_count >= threshold
    
    return anomalies, vote_count
```

### Confidence Scoring

Weight methods by confidence:

```python
def weighted_anomaly(data):
    """Weighted combination of scores"""
    z_anom, z_scores = zscore_anomaly(data)
    iqr_anom, _ = iqr_anomaly(data)
    
    # Normalize Z-scores to 0-1
    confidence = (z_scores - z_scores.min()) / (z_scores.max() - z_scores.min())
    
    # Combine with IQR
    final_score = 0.6 * confidence + 0.4 * iqr_anom.astype(float)
    anomalies = final_score > 0.7
    
    return anomalies, final_score
```

## Practical Considerations

### Sample Size Requirements

- **Z-Score/IQR:** Minimum 30 samples
- **Grubbs:** Minimum 7 samples
- **ML Methods:** Minimum 100 samples (1000+ recommended)

### Handling Edge Cases

1. **All values identical:** No anomalies possible
2. **Too few samples:** Use simple percentile method
3. **Heavy skew:** Prefer IQR or Modified Z-Score over Z-Score
4. **Multiple modes:** Use clustering-based methods

### Performance Guidelines

- **< 1K rows:** Any method works, prefer simple statistics
- **1K-100K rows:** Z-Score, IQR, or Isolation Forest
- **100K-1M rows:** Batch processing with Z-Score/IQR
- **> 1M rows:** Sample-based or distributed processing

### False Positive Management

To reduce false positives:
1. Increase threshold (Z > 3.5 instead of 3.0)
2. Require multiple methods to agree
3. Add domain-specific rules
4. Use time-series context for temporal data
5. Manual review of high-confidence anomalies
