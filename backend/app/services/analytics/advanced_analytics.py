"""
Advanced analytics - correlation, clustering, prediction
"""
import numpy as np
from typing import Optional
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


class AdvancedAnalytics:
    """Advanced statistical and ML analysis"""

    def __init__(self, db=None):
        self.db = db

    def get_correlation_matrix(
        self,
        metrics: Optional[list] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> dict:
        """Calculate correlation matrix between metrics"""
        if metrics is None:
            metrics = ['revenue', 'orders', 'traffic', 'avg_order_value', 'conversion_rate']

        n = len(metrics)
        # Generate correlation matrix (TODO: use real data)
        np.random.seed(42)
        corr = np.eye(n)
        for i in range(n):
            for j in range(i + 1, n):
                val = np.round(np.random.uniform(0.3, 0.95), 2)
                corr[i, j] = val
                corr[j, i] = val

        matrix = [[metrics[i]] + corr[i].tolist() for i in range(n)]

        # Key insights
        insights = []
        for i in range(n):
            for j in range(i + 1, n):
                if corr[i, j] > 0.7:
                    insights.append(f"Strong correlation between {metrics[i]} and {metrics[j]}: {corr[i, j]:.2f}")
                elif corr[i, j] > 0.4:
                    insights.append(f"Moderate correlation between {metrics[i]} and {metrics[j]}: {corr[i, j]:.2f}")

        return {
            "correlation_matrix": matrix,
            "insights": insights,
            "metrics": metrics,
        }

    def create_clustering(
        self,
        cluster_type: str = 'customer',
        n_clusters: int = 3,
        features: Optional[list] = None
    ) -> dict:
        """Perform clustering analysis on customers or products"""
        if features is None:
            features = ['revenue', 'frequency', 'recency']

        # Generate sample data
        np.random.seed(42)
        n_samples = 300
        X = np.random.randn(n_samples, len(features))

        # Standardize
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # K-means clustering
        kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
        labels = kmeans.fit_predict(X_scaled)

        # Cluster characteristics
        cluster_info = []
        segment_names = {
            'customer': {
                0: "High Value Champions",
                1: "Growth Potential",
                2: "At Risk Customers",
            },
            'product': {
                0: "Top Performers",
                1: "Steady Sellers",
                2: "Underperformers",
            }
        }

        characteristics = {
            'customer': {
                0: "High value, frequent customers with recent purchases",
                1: "Medium value customers with growth potential",
                2: "Low value, infrequent customers at risk of churn",
            },
            'product': {
                0: "High revenue, high conversion rate products",
                1: "Consistent sellers with stable demand",
                2: "Low performing products needing attention",
            }
        }

        names = segment_names.get(cluster_type, segment_names['customer'])
        chars = characteristics.get(cluster_type, characteristics['customer'])

        for i in range(n_clusters):
            mask = labels == i
            cluster_info.append({
                "cluster_id": i,
                "cluster_name": names.get(i, f"Segment {i}"),
                "count": int(mask.sum()),
                "percentage": round(float(mask.sum()) / n_samples * 100, 1),
                "centroid": [round(float(v), 2) for v in scaler.inverse_transform([kmeans.cluster_centers_[i]])[0]],
                "characteristics": chars.get(i, f"Cluster {i}"),
            })

        return {
            "clusters": cluster_info,
            "parameters": {
                "type": cluster_type,
                "n_clusters": n_clusters,
                "features": features,
            },
            "inertia": float(kmeans.inertia_),
        }

    def get_prediction(
        self,
        metric: str = 'revenue',
        periods: int = 30,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> dict:
        """Generate trend predictions"""
        # Generate historical data
        np.random.seed(42)
        historical = [1000 + i * 10 + np.random.normal(0, 50) for i in range(90)]

        # Simple trend projection
        x = np.arange(len(historical))
        z = np.polyfit(x, historical, 2)
        p = np.poly1d(z)

        future_x = np.arange(len(historical), len(historical) + periods)
        predictions = [max(0, p(i)) for i in future_x]

        return {
            "metric": metric,
            "historical": {
                "values": [round(v, 2) for v in historical[-30:]],
                "dates": [f"Day {i}" for i in range(len(historical) - 30, len(historical))],
            },
            "predictions": {
                "values": [round(v, 2) for v in predictions],
                "dates": [f"Day {i}" for i in range(len(historical), len(historical) + periods)],
            },
            "confidence": {
                "upper": [round(v * 1.15, 2) for v in predictions],
                "lower": [round(v * 0.85, 2) for v in predictions],
            },
            "trend": "upward" if predictions[-1] > predictions[0] else "downward",
        }
