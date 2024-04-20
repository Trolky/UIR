import math
import numpy as np
from matplotlib import pyplot as plt

class Points():
    def __init__(self, x:float, y:float):
        self.x: float = float(x)
        self.y: float = float(y)

    def toString(self):
        print(f"x = {self.x}, y = {self.y}")

class DataLoader():
    @staticmethod
    def loadData(file_name):
        cluster: list[Points] = []
        centroids: list[Points] = []

        with open(file_name, 'r') as f:
            f.readline()

            line = f.readline().strip()
            while line != "init.x;init.y":
                x, y = line.strip().split(";")
                cluster.append(Points(x, y))
                line = f.readline().strip()

            line = f.readline().strip()
            while line:
                x, y = line.strip().split(";")
                centroids.append(Points(x,y))
                line = f.readline().strip()
        return cluster, centroids
class Clusters():
    def __init__(self, points, centroids):
        self.points = points
        self.centroids = centroids

    def show_plot(self, title):
        x_points = [point.x for point in self.points]
        y_points = [point.y for point in self.points]

        # Extract x and y coordinates for centroids
        x_centroids = [centroid.x for centroid in self.centroids]
        y_centroids = [centroid.y for centroid in self.centroids]

        # Plot points
        plt.scatter(x_points, y_points, color='blue', label='Points')

        # Plot centroids
        plt.scatter(x_centroids, y_centroids, color='red', label='Centroids', marker='x')

        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title(title)
        plt.legend()
        plt.show()

    def calculate_distace(self, point1: Points, point2: Points):
        distance_squared = math.fsum(
            (float(x1) - float(x2)) ** 2.0 for x1, x2 in zip((point1.x, point1.y), (point2.x, point2.y)))
        return math.sqrt(distance_squared)

    def k_means(self):
        converged = False
        iteration = 1
        while not converged:
            clusters = [[] for _ in range(len(self.centroids))]
            for point in self.points:
                distances_to_centroids = [self.calculate_distace(point, centroid) for centroid in self.centroids]
                get_minimal_distance = min(distances_to_centroids)
                assigned_centroid = distances_to_centroids.index(get_minimal_distance)
                clusters[assigned_centroid].append(point)

            new_centroids = [self.calculate_centroid_k_means(cluster) for cluster in clusters]
            converged = all(abs(new_centroid.x - old_centroid.x) < 1e-5 and
                            abs(new_centroid.y - old_centroid.y) < 1e-5
                            for new_centroid, old_centroid in zip(new_centroids, self.centroids))

            self.centroids = new_centroids
            if converged:
                return self.centroids, iteration
            iteration += 1

    def k_medoid(self):
        converged = False
        iteration = 1
        while not converged:
            clusters = [[] for _ in range(len(self.centroids))]
            for point in self.points:
                distances_to_centroids = [self.calculate_distace(point, centroid) for centroid in self.centroids]
                get_minimal_distance = min(distances_to_centroids)
                assigned_centroid = distances_to_centroids.index(get_minimal_distance)
                clusters[assigned_centroid].append(point)

            new_centroids = [self.calculate_centroid_k_medoid(cluster) for cluster in clusters]

            converged = all(abs(new_centroid.x - old_centroid.x) < 1e-5 and
                            abs(new_centroid.y - old_centroid.y) < 1e-5
                            for new_centroid, old_centroid in zip(new_centroids, self.centroids))

            self.centroids = new_centroids
            if converged:
                return self.centroids, iteration
            iteration += 1



    def calculate_centroid_k_means(self, cluster):
        if not cluster:
            return None

        sum_x = sum(point.x for point in cluster)
        sum_y = sum(point.y for point in cluster)

        centroid_x = sum_x / len(cluster)
        centroid_y = sum_y / len(cluster)

        return Points(centroid_x, centroid_y)

    def calculate_centroid_k_medoid(self, cluster):
        if not cluster:
            return None

        cluster_points = list(cluster)
        min_total_dissimilarity = float('inf')
        new_medoid = None

        for point in cluster_points:
            total_dissimilarity = sum(self.calculate_distace(point, other_point) for other_point in cluster_points)

            if total_dissimilarity < min_total_dissimilarity:
                min_total_dissimilarity = total_dissimilarity
                new_medoid = point

        return new_medoid


if __name__ == "__main__":
    points, centroids = DataLoader.loadData("cv7_vstup.txt")

    cluster = Clusters(points, centroids)

    centroids, iteration = cluster.k_means()
    print(f"K-means ended in {iteration} iterations: ")
    for i in centroids:
        print(f"x = {i.x}, y = {i.y}")
    cluster.show_plot("K-Means Clustering")

    cluster = Clusters(points, centroids)
    centroids, iteration = cluster.k_medoid()
    print(f"K-Medoid ended in {iteration} iterations: ")
    for i in centroids:
        print(f"x = {i.x}, y = {i.y}")
    cluster.show_plot("K-Medoid Clustering")
