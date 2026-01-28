"""
Anomaly Detection using HNSW Graph Properties

Implements multiple anomaly scoring methods:
- kNN Distance Score: Points whose neighbors are far away
- Local Outlier Factor (LOF): Points in sparse regions surrounded by dense regions
- Reverse kNN: Points that aren't claimed as neighbors by others
- Isolation Score: Combined metric for ranking anomalies
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field
from sklearn.neighbors import LocalOutlierFactor
from collections import Counter


@dataclass
class AnomalyScore:
    """Represents anomaly scores for an item."""
    item_id: int
    knn_distance: float  # Average distance to k nearest neighbors
    lof_score: float  # Local Outlier Factor (>1 = outlier)
    reverse_knn_count: int  # How many items have this as a neighbor
    isolation_score: float  # Combined anomaly score (higher = more anomalous)
    neighbors: List[int] = field(default_factory=list)
    rank: int = 0  # Rank among all items (1 = most anomalous)

    def to_dict(self) -> dict:
        return {
            "item_id": self.item_id,
            "knn_distance": round(self.knn_distance, 4),
            "lof_score": round(self.lof_score, 4),
            "reverse_knn_count": self.reverse_knn_count,
            "isolation_score": round(self.isolation_score, 4),
            "rank": self.rank,
            "neighbors": self.neighbors
        }


class AnomalyDetector:
    """
    Detects anomalies in indexed code using HNSW graph properties.

    The detector analyzes the structure of the HNSW graph to identify
    "anomalys" - code that doesn't fit the normal patterns.
    """

    def __init__(self, index, k: int = 10):
        """
        Initialize anomaly detector.

        Args:
            index: HNSWIndex instance
            k: Number of neighbors for kNN-based metrics
        """
        self.index = index
        self.k = k

    def compute_knn_distances(self) -> Dict[int, Tuple[float, List[int]]]:
        """
        Compute average kNN distance for each item.

        Returns:
            Dict mapping item_id -> (avg_distance, neighbor_ids)
        """
        results = {}
        count = self.index.count()

        for item_id in range(count):
            neighbors = self.index.get_neighbors(item_id, k=self.k)
            if neighbors:
                avg_dist = np.mean([dist for _, dist in neighbors])
                neighbor_ids = [idx for idx, _ in neighbors]
            else:
                avg_dist = float('inf')
                neighbor_ids = []

            results[item_id] = (avg_dist, neighbor_ids)

        return results

    def compute_reverse_knn(self) -> Dict[int, int]:
        """
        Compute reverse kNN count for each item.

        Reverse kNN = how many other items have this item as a neighbor.
        Low reverse kNN = "orphan" that nothing considers close.

        Returns:
            Dict mapping item_id -> reverse_knn_count
        """
        reverse_counts = Counter()
        count = self.index.count()

        for item_id in range(count):
            neighbors = self.index.get_neighbors(item_id, k=self.k)
            for neighbor_id, _ in neighbors:
                reverse_counts[neighbor_id] += 1

        # Ensure all items have an entry
        for item_id in range(count):
            if item_id not in reverse_counts:
                reverse_counts[item_id] = 0

        return dict(reverse_counts)

    def compute_lof(self, contamination: float = 0.1) -> Dict[int, float]:
        """
        Compute Local Outlier Factor for each item.

        LOF compares local density of a point to its neighbors.
        LOF > 1 indicates lower density than neighbors (outlier).

        Args:
            contamination: Expected proportion of outliers

        Returns:
            Dict mapping item_id -> LOF score
        """
        embeddings = self.index.get_all_embeddings()

        if len(embeddings) < self.k + 1:
            # Not enough data for LOF
            return {i: 1.0 for i in range(len(embeddings))}

        lof = LocalOutlierFactor(
            n_neighbors=min(self.k, len(embeddings) - 1),
            contamination=contamination,
            novelty=False,
            metric='cosine'
        )

        # LOF returns negative scores; -1 = inlier, more negative = outlier
        # We convert to positive where >1 = outlier
        lof.fit(embeddings)
        scores = -lof.negative_outlier_factor_

        return {i: float(scores[i]) for i in range(len(scores))}

    def compute_isolation_score(
        self,
        knn_distances: Dict[int, Tuple[float, List[int]]],
        lof_scores: Dict[int, float],
        reverse_knn: Dict[int, int],
        weights: Tuple[float, float, float] = (0.4, 0.4, 0.2)
    ) -> Dict[int, float]:
        """
        Compute combined isolation score.

        Combines multiple signals into a single anomaly score.

        Args:
            knn_distances: Output from compute_knn_distances
            lof_scores: Output from compute_lof
            reverse_knn: Output from compute_reverse_knn
            weights: (knn_weight, lof_weight, reverse_knn_weight)

        Returns:
            Dict mapping item_id -> isolation_score
        """
        # Normalize each metric to [0, 1]
        knn_values = [d for d, _ in knn_distances.values()]
        lof_values = list(lof_scores.values())
        rknn_values = list(reverse_knn.values())

        def normalize(values: List[float], inverse: bool = False) -> Dict[int, float]:
            """Normalize values to [0, 1], optionally inverting."""
            arr = np.array(values)
            if arr.max() == arr.min():
                return {i: 0.5 for i in range(len(values))}

            normalized = (arr - arr.min()) / (arr.max() - arr.min())
            if inverse:
                normalized = 1 - normalized
            return {i: float(normalized[i]) for i in range(len(values))}

        # Higher knn distance = more anomalous
        knn_norm = normalize(knn_values)

        # Higher LOF = more anomalous
        lof_norm = normalize(lof_values)

        # Lower reverse kNN = more anomalous (inverse)
        rknn_norm = normalize(rknn_values, inverse=True)

        # Combine with weights
        w_knn, w_lof, w_rknn = weights
        isolation = {}

        for item_id in range(len(knn_distances)):
            score = (
                w_knn * knn_norm[item_id] +
                w_lof * lof_norm[item_id] +
                w_rknn * rknn_norm[item_id]
            )
            isolation[item_id] = score

        return isolation

    def analyze(
        self,
        lof_contamination: float = 0.1,
        weights: Tuple[float, float, float] = (0.4, 0.4, 0.2)
    ) -> List[AnomalyScore]:
        """
        Run full anomaly analysis on the index.

        Args:
            lof_contamination: Expected outlier proportion for LOF
            weights: (knn_weight, lof_weight, reverse_knn_weight)

        Returns:
            List of AnomalyScore objects, sorted by isolation_score (descending)
        """
        if self.index.count() == 0:
            return []

        # Compute all metrics
        knn_distances = self.compute_knn_distances()
        lof_scores = self.compute_lof(contamination=lof_contamination)
        reverse_knn = self.compute_reverse_knn()
        isolation_scores = self.compute_isolation_score(
            knn_distances, lof_scores, reverse_knn, weights
        )

        # Build AnomalyScore objects
        scores = []
        for item_id in range(self.index.count()):
            knn_dist, neighbors = knn_distances[item_id]
            scores.append(AnomalyScore(
                item_id=item_id,
                knn_distance=knn_dist,
                lof_score=lof_scores[item_id],
                reverse_knn_count=reverse_knn[item_id],
                isolation_score=isolation_scores[item_id],
                neighbors=neighbors
            ))

        # Sort by isolation score (most anomalous first)
        scores.sort(key=lambda s: s.isolation_score, reverse=True)

        # Assign ranks
        for rank, score in enumerate(scores, 1):
            score.rank = rank

        return scores

    def get_top_anomalys(
        self,
        n: int = 10,
        lof_contamination: float = 0.1
    ) -> List[AnomalyScore]:
        """
        Get the top N most anomalous items.

        Args:
            n: Number of anomalies to return
            lof_contamination: Expected outlier proportion for LOF

        Returns:
            Top N AnomalyScore objects
        """
        all_scores = self.analyze(lof_contamination=lof_contamination)
        return all_scores[:n]

    def explain_anomaly(self, score: AnomalyScore) -> str:
        """
        Generate a human-readable explanation for why an item is anomalous.

        Args:
            score: AnomalyScore object

        Returns:
            Explanation string
        """
        reasons = []

        # Check kNN distance
        if score.knn_distance > 0.5:
            reasons.append(f"High distance to neighbors ({score.knn_distance:.3f}) - isolated in embedding space")
        elif score.knn_distance > 0.3:
            reasons.append(f"Moderate distance to neighbors ({score.knn_distance:.3f})")

        # Check LOF
        if score.lof_score > 1.5:
            reasons.append(f"High LOF score ({score.lof_score:.2f}) - in a sparse region compared to neighbors")
        elif score.lof_score > 1.2:
            reasons.append(f"Elevated LOF score ({score.lof_score:.2f})")

        # Check reverse kNN
        if score.reverse_knn_count == 0:
            reasons.append("Zero reverse neighbors - nothing considers this code similar")
        elif score.reverse_knn_count < 3:
            reasons.append(f"Low reverse neighbors ({score.reverse_knn_count}) - rarely referenced as similar")

        if not reasons:
            reasons.append("Slightly elevated anomaly metrics")

        return " | ".join(reasons)
