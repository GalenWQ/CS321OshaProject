"""
k_means.py
"""
import math


def decide_k():
    return 3


def centroid(cluster):
    distances = 0
    speeds = 0
    for instance in cluster:
        distances += float(instance[0])
        speeds += float(instance[1])

    avgDistance = distances / len(cluster)
    avgSpeed = speeds / len(cluster)

    return (avgDistance, avgSpeed)


def euclidean_distance(p, q):
    return math.sqrt((q[0] - p[0])**2 + (q[1] - p[1])**2)


def build_clusters(data):
    k = decide_k()
    clusters = []

    for cluster in range(0, k):
        initial_item = [data.pop(0)]
        clusters.append(initial_item)

    for item in data:
        distance = float(item[1])
        speed = float(item[2])

        closest_cluster = 0
        smallest_distance = 1000
        for cluster in clusters:
            centroid_distance = euclidean_distance(centroid(cluster), (distance, speed))
            if centroid_distance < smallest_distance:
                smallest_distance = centroid_distance
                closest_cluster = clusters.index(cluster)

        clusters[closest_cluster].append(item)

    return clusters

