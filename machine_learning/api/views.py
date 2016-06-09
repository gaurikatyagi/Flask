from api import app
import os
import pandas as pd
import json
from flask import jsonify
from flask import render_template, url_for
from sklearn import preprocessing
from sklearn import decomposition
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt


def get_abs_path():
    return os.path.abspath(os.path.dirname(__file__))

def get_data():
    f_name = os.path.join(get_abs_path(), "data", "breast-cancer-wisconsin.csv")
    columns = ["code", "clump_thickness", "size_uniformity", "shape_uniformity", "adhesion", "cell_size", "bare_nuclei",
               "bland_chromatin", "normal_nuclei", "mitosis", "class"]
    df = pd.read_csv(f_name, sep=",", header=None, names=columns, na_values="?")
    return df.dropna()

@app.route("/")
def index():
    df = get_data()
    X = df.ix[:, (df.columns != "class") & (df.columns != "code")].as_matrix()
    y = df.ix[:, df.columns == "clas"].as_matrix()

    #scale data
    scaler = preprocessing.StandardScaler().fit(X)
    scaled = scaler.transform(X)

    #PCA
    pcomp = decomposition.PCA(n_components = 2)
    pcomp.fit(scaled)
    components = pcomp.transform(scaled)
    var = pcomp.explained_variance_ratio_.sum()

    #Kmeans
    model = KMeans(init = "k-means++", n_clusters = 2) #K-means++ ensures that the initial centroids which are chosen
    # are spaced out far apart
    model.fit(components)
    fig = plt.figure()
    plt.scatter(x = components[:, 0], y = components[:, 1], c = model.labels_)
    centers = plt.plot(
        [model.cluster_centers_[0, 0], model.cluster_centers_[1, 0]],
        [model.cluster_centers_[1, 0], model.cluster_centers_[1, 1]],
        "kx", c = "Green"
    )

    #Increase size of center points
    plt.setp(centers, ms = 11.0) #increases size
    plt.setp(centers, mew = 1.8)

    #Plot axes adjustments
    axes = plt.gca()
    axes.set_xlim([-7.5, 3])
    axes.set_ylim([-2, 5])
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.title("Clustering of PCs ({:.2f}% Var. Explained)".format(var*100))

    #Save figure
    fig_path = os.path.join(get_abs_path(), "static", "tmp", "cluster.png")
    fig.savefig(fig_path)
    return render_template("index.html", fig = url_for("static", filename = "tmp/cluster.png"))

@app.route("/head")
def head():
    df = get_data().head()
    data = json.loads((df.to_json()))
    return jsonify(data)