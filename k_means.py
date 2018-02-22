"""
k_means.py
"""
import math


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


def build_clusters(data, k):
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

        if loops > 50:
            done = True

    return clusters


def eval_clusters(clusters):
    total_length = 0
    for cluster in clusters:
        safe = 0
        compliant = 0
        noncompliant = 0

        for item in cluster:
            if item[4] == 'Safe':
                safe += 1
            elif item[4] == 'Compliant':
                compliant += 1
            elif item[4] == 'NonCompliant':
                noncompliant += 1

        total = safe + compliant + noncompliant

        print('-----------------------')
        print("\nCLUSTER", clusters.index(cluster) + 1)
        print("Safe:", safe / total)
        print("Compliant:", compliant / total)
        print("NonCompliant:", noncompliant / total)
        total_length += len(cluster)
    print("\nTotal length:", total_length)


def calculate_error(cluster):
    total = 0
    cur_centroid = centroid(cluster)
    for instance in cluster:
        point = (float(instance[1]), float(instance[2]))
        deviation = euclidean_distance(cur_centroid, point)
        total += deviation**2

    return total


def find_elbow(data):
    results = []
    for k in range(2, 20):
        clusters = build_clusters(data, k)

        ase = 0
        for cluster in clusters:
            ase += calculate_error(cluster)

        ase /= len(clusters)
        results.append(ase)

    return results