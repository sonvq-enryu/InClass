import numpy as np
import os
import pandas as pd    

def iou(box, clusters):
    """
    Calculate intersection over union between point with center of cluster
    Parameters:
        box: a box with width and height
        clusters: center of clusters with shape (k, 2) with k is number of cluster
    Return:
        intersection over union of box with center of clusters
    """

    x = np.minimum(clusters[:, 0], box[0])
    y = np.minimum(clusters[:, 1], box[1])

    inter = x * y
    box_area = box[0] * box[1]
    clusters_area = clusters[:, 0] * clusters[:, 1]

    return inter / (box_area + clusters_area - inter)

def iou_kmeans(boxes, k, dist=np.mean):
    """
    K-mean clustering with Intersection over Union (IoU) metric.
    Parameters:
        bboxes: numpy array has shape (n, 2) with n is number of bounding box, 2 is width and height.
        k     : integer, number of clusters.
        dist  : function using calculate new center of clusters
    Return:
        numpy array has shape (k, 2) => priors box
    """
    n = boxes.shape[0]

    distances = np.empty((n, k)) # distance between one box to center of clusters.
    
    last_clusters = np.zeros((n, ))
    
    # random initialization k center of clusters
    np.random.seed()
    clusters = boxes[np.random.choice(n, k, replace=False)] # replace = False aka permutation

    while True:
        for i in range(n):
            distances[i] = 1 - iou(boxes[i], clusters)
        
        nearest_cluster = np.argmin(distances, axis=1)
        
        # if converge
        if (last_clusters == nearest_cluster).all():
            break
        
        # if not converge set last to new cluster
        last_clusters = nearest_cluster

        for i in range(k):
            clusters[i] = dist(boxes[nearest_cluster == i], axis=0)

    return clusters