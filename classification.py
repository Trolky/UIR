import math
import numpy as np
from matplotlib import pyplot as plt
import heapq
class Points():
    def __init__(self, x:float, y:float, cluster:str) -> None:
        self.x: float = float(x)
        self.y: float = float(y)
        self.clsuter = cluster
    def setCluster(self, cluster):
        self.clsuter = cluster

class DataLoader():
    @staticmethod
    def loadData(file_name):
        points: list[Points] = []
        newPoints: list[Points] = []

        with open(file_name, 'r') as f:
            f.readline()

            line = f.readline().strip()
            while line != "test.x;test.y":
                x, y, cluster = line.strip().split(";")
                points.append(Points(x, y, cluster))
                line = f.readline().strip()

            line = f.readline().strip()
            while line:
                x, y = line.strip().split(";")
                newPoints.append(Points(x, y, ""))
                line = f.readline().strip()
        return points, newPoints
class Clusters():
    def __init__(self, points, newPoints):
        self.points:list[Points] = points
        self.newPoints:list[Points] = newPoints

    def show_plot(self, title, points, allClasses):
        colors = ["blue", "red", "green", "yellow"]
        i = 0
        for cls in allClasses:
            point_x = []
            point_y = []
            for point in points:
                if cls == point.clsuter:
                    point_x.append(point.x)
                    point_y.append(point.y)

            plt.scatter(point_x,  point_y, color=colors[i], label=cls)
            i += 1


        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title(title)
        plt.legend()
        plt.show()

    def calculate_distace(self, point1: Points, point2: Points):
        distance_squared = math.fsum(
            (float(x1) - float(x2)) ** 2.0 for x1, x2 in zip((point1.x, point1.y), (point2.x, point2.y)))
        return math.sqrt(distance_squared)

    def k_nn(self, k):
        allClasses = set(point.clsuter for point in points)
        for newPoint in self.newPoints:
            distances = []
            clusterCounts = {cluster: 0 for cluster in allClasses}
            for point in self.points:
                distances.append(self.calculate_distace(newPoint, point))
            for distance in heapq.nsmallest(k, distances):
                clusterCounts[self.points[distances.index(distance)].clsuter] += 1

            newPoint.clsuter = max(clusterCounts, key=clusterCounts.get)
        categorizedPoints = self.points
        categorizedPoints.extend(self.newPoints)
        return categorizedPoints, allClasses




    def k_nc(self):
        allClasses = set(point.clsuter for point in points)
        centroids = {}

        for cluster in allClasses:
            clusterPoints = [point for point in self.points if point.clsuter == cluster]
            centroid_x = sum(point.x for point in clusterPoints)/len(clusterPoints)
            centroid_y = sum(point.y for point in clusterPoints)/len(clusterPoints)
            centroids[cluster] = Points(centroid_x, centroid_y, cluster)

        for newPoint in self.newPoints:
            distances = []
            for centroid in centroids.values():
                distances.append(self.calculate_distace(newPoint, centroid))

            newPoint.clsuter = list(centroids.values())[distances.index(min(distances))].clsuter

        categorizedPoints = self.points
        categorizedPoints.extend(self.newPoints)
        return categorizedPoints, allClasses




if __name__ == "__main__":
    points, newPoints = DataLoader.loadData("cv8_vstup.txt")

    cluster = Clusters(points, newPoints)
    allPoints, allClasses = cluster.k_nn(1)
    cluster.show_plot("K-NN", allPoints, allClasses)

    cluster = Clusters(points, newPoints)
    allPoints, allClasses = cluster.k_nc()
    cluster.show_plot("K-NC", allPoints, allClasses)
