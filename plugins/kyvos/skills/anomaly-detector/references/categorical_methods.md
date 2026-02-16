# Categorical Anomaly Detection Methods

Reference for detecting anomalies in non-numerical (categorical) data.

## When to Use
- Data contains string labels, IDs, status codes, or categories
- You need to find rare events or unusual combinations
- Detecting shifts in category distribution (e.g., "Error" status frequency increasing)

## Core Techniques

### 1. Rare Category Detection (Frequency Analysis)

Identify categories that appear too infrequently to be considered normal.

```python
def detect_rare_categories(series, min_count=None, min_freq=0.01):
    """
    Flag values that appear less than a specific count or frequency.
    
    Args:
        series: Pandas Series of categorical data
        min_count: Minimum absolute count required
        min_freq: Minimum percentage (0.0-1.0) required
    """
    value_counts = series.value_counts()
    total_count = len(series)
    
    if min_count is None:
        min_count = total_count * min_freq
        
    rare_values = value_counts[value_counts < min_count].index.tolist()
    
    # Boolean mask: True if value is rare
    anomalies = series.isin(rare_values)
    return anomalies, rare_values
```

**Use Case:** Finding rare error codes, unusual user agents, or uncommon product categories.

### 2. High Cardinality Anomaly

Detect when a column has an unexpectedly high number of unique values (e.g., free text in a field expected to be a dropdown).

```python
def check_cardinality(series, threshold_ratio=0.9):
    """
    Check if a categorical column has too many unique values.
    
    Args:
        series: Pandas Series
        threshold_ratio: Ratio of unique values to total rows (0.0-1.0)
    """
    n_unique = series.nunique()
    n_total = len(series)
    ratio = n_unique / n_total
    
    is_anomalous = ratio > threshold_ratio
    return is_anomalous, ratio
```

**Use Case:** Identifying data quality issues where IDs are put in Name fields, or dirty data with many typos.

### 3. Entropy Analysis

Measure the "randomness" of a categorical variable. Low entropy means predictable; high entropy means random. Anomalies occur when entropy deviates from the norm.

```python
from scipy.stats import entropy

def calculate_entropy(series):
    """Calculate Shannon entropy of a series."""
    value_counts = series.value_counts()
    probs = value_counts / len(series)
    return entropy(probs)
```

**Application:**
- **Unexpected Uniformity:** If a "Status" field usually has 90% "OK", entropy is low. If it suddenly becomes 50% "OK" and 50% "Error", entropy spikes.
- **Unexpected Spikes:** If a "User ID" field is usually random (high entropy) but suddenly one user dominates, entropy drops.

### 4. Chi-Square Goodness of Fit

Compare the current distribution of categories against a reference (expected) distribution.

```python
from scipy.stats import chisquare

def detect_distribution_shift(current_counts, expected_probs):
    """
    Compare current value counts against expected probabilities.
    
    Args:
        current_counts: Dict or Series of counts {category: count}
        expected_probs: Dict of expected probabilities {category: prob}
    """
    # Align observed and expected
    observed = []
    expected = []
    total_samples = sum(current_counts.values())
    
    for cat, prob in expected_probs.items():
        obs = current_counts.get(cat, 0)
        exp = prob * total_samples
        
        # Chi-square requires expected freq >= 5
        if exp >= 5:
            observed.append(obs)
            expected.append(exp)
            
    if not observed:
        return False, 1.0
        
    chi2_stat, p_value = chisquare(f_obs=observed, f_exp=expected)
    
    # p_value < 0.05 implies significant difference (anomaly)
    is_anomalous = p_value < 0.05
    return is_anomalous, p_value
```

**Use Case:** Monitoring if the mix of "Gold", "Silver", "Bronze" customers has changed significantly.

## Advanced: Rare Combination Detection

Detect unusual combinations of two categorical variables (e.g., "Region=US" usually goes with "Currency=USD").

```python
def detect_rare_combinations(df, col1, col2, threshold=0.01):
    """
    Find rows where the combination of col1 and col2 is rare.
    """
    # Create a combined key
    df['combined'] = df[col1].astype(str) + "|" + df[col2].astype(str)
    
    # Use frequency analysis on the combination
    anomalies, rare_vals = detect_rare_categories(df['combined'], min_freq=threshold)
    
    return anomalies
```

**Use Case:** "Shipping Country" vs "Billing Country" mismatches, or "Department" vs "Job Title" inconsistencies.
