#!/usr/bin/env python3
"""
Anomaly Detection Script for CSV Data
Detects anomalies using multiple statistical methods
"""

import pandas as pd
import numpy as np
from scipy import stats
from datetime import datetime
import argparse
import json
import warnings
warnings.filterwarnings('ignore')


class AnomalyDetector:
    """Multi-method anomaly detection for CSV data"""
    
    def __init__(self, threshold=3.0):
        self.threshold = threshold
        self.results = {
            'summary': {},
            'anomalies': [],
            'statistics': {}
        }
    
    def detect_zscore_anomalies(self, df, column):
        """Detect anomalies using Z-score method"""
        if not pd.api.types.is_numeric_dtype(df[column]):
            return []
        
        # Remove NaN values
        data = df[column].dropna()
        if len(data) < 3:
            return []
        
        # Calculate Z-scores
        z_scores = np.abs(stats.zscore(data))
        anomaly_indices = np.where(z_scores > self.threshold)[0]
        
        anomalies = []
        for idx in anomaly_indices:
            original_idx = data.index[idx]
            anomalies.append({
                'row': int(original_idx),
                'column': column,
                'value': float(data.iloc[idx]),
                'z_score': float(z_scores[idx]),
                'method': 'z-score',
                'severity': 'high' if z_scores[idx] > 4 else 'medium'
            })
        
        return anomalies
    
    def detect_iqr_anomalies(self, df, column):
        """Detect anomalies using IQR method"""
        if not pd.api.types.is_numeric_dtype(df[column]):
            return []
        
        data = df[column].dropna()
        if len(data) < 4:
            return []
        
        Q1 = data.quantile(0.25)
        Q3 = data.quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        anomaly_mask = (data < lower_bound) | (data > upper_bound)
        anomaly_indices = data[anomaly_mask].index
        
        anomalies = []
        for idx in anomaly_indices:
            value = data.loc[idx]
            distance = min(abs(value - lower_bound), abs(value - upper_bound))
            severity = 'high' if distance > 2 * IQR else 'medium'
            
            anomalies.append({
                'row': int(idx),
                'column': column,
                'value': float(value),
                'bounds': f'[{lower_bound:.2f}, {upper_bound:.2f}]',
                'method': 'IQR',
                'severity': severity
            })
        
        return anomalies
    
    def detect_timeseries_anomalies(self, df, date_column, value_column):
        """Detect time-series anomalies"""
        if date_column not in df.columns or value_column not in df.columns:
            return []
        
        # Try to parse date column
        try:
            df_sorted = df.copy()
            df_sorted[date_column] = pd.to_datetime(df_sorted[date_column])
            df_sorted = df_sorted.sort_values(date_column)
        except:
            return []
        
        # Group by date and aggregate
        daily_data = df_sorted.groupby(date_column)[value_column].sum().reset_index()
        
        if len(daily_data) < 7:
            return []
        
        # Calculate rolling statistics (7-day window)
        window_size = min(7, len(daily_data) // 3)
        rolling_mean = daily_data[value_column].rolling(window=window_size, center=True).mean()
        rolling_std = daily_data[value_column].rolling(window=window_size, center=True).std()
        
        anomalies = []
        for idx in range(len(daily_data)):
            if pd.isna(rolling_mean.iloc[idx]) or pd.isna(rolling_std.iloc[idx]):
                continue
            
            value = daily_data[value_column].iloc[idx]
            mean = rolling_mean.iloc[idx]
            std = rolling_std.iloc[idx]
            
            if std > 0:
                z_score = abs(value - mean) / std
                if z_score > self.threshold:
                    anomalies.append({
                        'date': str(daily_data[date_column].iloc[idx]),
                        'column': value_column,
                        'value': float(value),
                        'expected_range': f'{mean-2*std:.2f} to {mean+2*std:.2f}',
                        'z_score': float(z_score),
                        'method': 'time-series',
                        'severity': 'high' if z_score > 4 else 'medium'
                    })
        
        return anomalies
    
    def detect_frequency_anomalies(self, df, column):
        """Detect categorical anomalies based on frequency"""
        if pd.api.types.is_numeric_dtype(df[column]):
            return []
        
        value_counts = df[column].value_counts()
        total = len(df)
        
        anomalies = []
        for value, count in value_counts.items():
            frequency = count / total
            
            # Flag rare categories (< 1% of data)
            if frequency < 0.01 and count < 10:
                anomalies.append({
                    'column': column,
                    'value': str(value),
                    'count': int(count),
                    'frequency': float(frequency),
                    'method': 'frequency',
                    'severity': 'low'
                })
        
        return anomalies
    
    def analyze(self, csv_path, methods=['zscore', 'iqr'], date_column=None):
        """Run anomaly detection on CSV file"""
        print(f"Loading data from {csv_path}...")
        df = pd.read_csv(csv_path)
        
        print(f"Dataset shape: {df.shape}")
        print(f"Columns: {list(df.columns)}\n")
        
        all_anomalies = []
        
        # Detect numeric column anomalies
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        for col in numeric_cols:
            if 'zscore' in methods:
                anomalies = self.detect_zscore_anomalies(df, col)
                all_anomalies.extend(anomalies)
                if anomalies:
                    print(f"Z-score: Found {len(anomalies)} anomalies in '{col}'")
            
            if 'iqr' in methods:
                anomalies = self.detect_iqr_anomalies(df, col)
                all_anomalies.extend(anomalies)
                if anomalies:
                    print(f"IQR: Found {len(anomalies)} anomalies in '{col}'")
        
        # Time series analysis if date column specified
        if 'timeseries' in methods and date_column:
            for value_col in numeric_cols:
                anomalies = self.detect_timeseries_anomalies(df, date_column, value_col)
                all_anomalies.extend(anomalies)
                if anomalies:
                    print(f"Time-series: Found {len(anomalies)} anomalies in '{value_col}'")
        
        # Frequency analysis for categorical columns
        if 'frequency' in methods:
            categorical_cols = df.select_dtypes(include=['object']).columns
            for col in categorical_cols:
                anomalies = self.detect_frequency_anomalies(df, col)
                all_anomalies.extend(anomalies)
                if anomalies:
                    print(f"Frequency: Found {len(anomalies)} rare categories in '{col}'")
        
        # Compile results
        self.results['anomalies'] = all_anomalies
        self.results['summary'] = {
            'total_anomalies': len(all_anomalies),
            'high_severity': sum(1 for a in all_anomalies if a.get('severity') == 'high'),
            'medium_severity': sum(1 for a in all_anomalies if a.get('severity') == 'medium'),
            'low_severity': sum(1 for a in all_anomalies if a.get('severity') == 'low'),
            'methods_used': methods
        }
        
        # Statistics
        self.results['statistics'] = {
            'dataset_rows': len(df),
            'dataset_columns': len(df.columns),
            'numeric_columns': len(numeric_cols),
            'anomaly_percentage': (len(all_anomalies) / len(df)) * 100 if len(df) > 0 else 0
        }
        
        return self.results
    
    def save_results(self, output_path):
        """Save results to JSON file"""
        with open(output_path, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"\nResults saved to {output_path}")
    
    def print_summary(self):
        """Print summary of findings"""
        print("\n" + "="*60)
        print("ANOMALY DETECTION SUMMARY")
        print("="*60)
        
        summary = self.results['summary']
        stats = self.results['statistics']
        
        print(f"\nDataset Statistics:")
        print(f"  Total rows: {stats['dataset_rows']}")
        print(f"  Total columns: {stats['dataset_columns']}")
        print(f"  Numeric columns: {stats['numeric_columns']}")
        
        print(f"\nAnomaly Summary:")
        print(f"  Total anomalies: {summary['total_anomalies']}")
        print(f"  High severity: {summary['high_severity']}")
        print(f"  Medium severity: {summary['medium_severity']}")
        print(f"  Low severity: {summary['low_severity']}")
        print(f"  Anomaly rate: {stats['anomaly_percentage']:.2f}%")
        
        # Show top anomalies by severity
        if self.results['anomalies']:
            high_severity = [a for a in self.results['anomalies'] if a.get('severity') == 'high']
            if high_severity:
                print(f"\nTop High Severity Anomalies (showing up to 5):")
                for i, anomaly in enumerate(high_severity[:5], 1):
                    print(f"\n  {i}. {anomaly.get('method', 'unknown').upper()} method")
                    for key, value in anomaly.items():
                        if key not in ['method', 'severity']:
                            print(f"     {key}: {value}")


def main():
    parser = argparse.ArgumentParser(
        description='Detect anomalies in CSV data using multiple statistical methods'
    )
    parser.add_argument('input_csv', help='Path to input CSV file')
    parser.add_argument(
        '--methods',
        default='zscore,iqr',
        help='Comma-separated detection methods: zscore, iqr, timeseries, frequency (default: zscore,iqr)'
    )
    parser.add_argument(
        '--threshold',
        type=float,
        default=3.0,
        help='Z-score threshold for anomaly detection (default: 3.0)'
    )
    parser.add_argument(
        '--date-column',
        help='Date column name for time-series analysis'
    )
    parser.add_argument(
        '--output',
        help='Output JSON file path for detailed results'
    )
    
    args = parser.parse_args()
    
    # Parse methods
    methods = [m.strip() for m in args.methods.split(',')]
    
    # Run detection
    detector = AnomalyDetector(threshold=args.threshold)
    results = detector.analyze(args.input_csv, methods=methods, date_column=args.date_column)
    
    # Print summary
    detector.print_summary()
    
    # Save results if output specified
    if args.output:
        detector.save_results(args.output)
    
    return 0


if __name__ == '__main__':
    exit(main())
