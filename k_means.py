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
        distances += float(instance[1])
        speeds += float(instance[2])

    avgDistance = distances / len(cluster)
    avgSpeed = speeds / len(cluster)

    return (avgDistance, avgSpeed)


def euclidean_distance(p, q):
    return math.sqrt((q[0] - p[0])**2 + (q[1] - p[1])**2)


def build_clusters(data):
    k = decide_k()
    clusters = []
    centroids = []

    for cluster in range(0, k):
        initial_item = [data.pop(0)]
        clusters.append(initial_item)
        centroids.append(centroid(clusters[cluster]))

    for item in data:
        distance = float(item[1])
        speed = float(item[2])

        closest_cluster = 0
        smallest_distance = 1000

        for cluster in clusters:
            centroid_distance = euclidean_distance(centroids[clusters.index(cluster)], (distance, speed))
            if centroid_distance < smallest_distance:
                smallest_distance = centroid_distance
                closest_cluster = clusters.index(cluster)

        clusters[closest_cluster].append(item)
        centroids[closest_cluster] = centroid(clusters[closest_cluster])

    done = False
    loops = 0

    while not done:
        done = True
        loops += 1
        for cluster in clusters:
            for item in cluster:
                distance = float(item[1])
                speed = float(item[2])

                cur_centroid_distance = euclidean_distance(centroids[clusters.index(cluster)], (distance, speed))
                cur_cluster = cluster

                for comp_cluster in clusters:
                    centroid_distance = euclidean_distance(centroids[clusters.index(comp_cluster)], (distance, speed))
                    if centroid_distance < cur_centroid_distance:
                        cur_centroid_distance = centroid_distance
                        cur_cluster = comp_cluster

                if cur_cluster != cluster:
                    updated_clusters = [clusters.index(cluster), clusters.index(cur_cluster)]
                    cluster.remove(item)
                    cur_cluster.append(item)
                    for updated_cluster in updated_clusters:
                        centroids[updated_cluster] = centroid(clusters[updated_cluster])
                    done = False

        if loops > 20:
            done = True

    return clusters

