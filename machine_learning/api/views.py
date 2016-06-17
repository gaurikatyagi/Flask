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
from sklearn.cross_validation import train_test_split
import sklearn.linear_model as linear_model
import sklearn.metrics as metric

def get_abs_path():
    return os.path.abspath(os.path.dirname(__file__))

def get_data():
    f_name = os.path.join(get_abs_path(), "data", "breast-cancer-wisconsin.csv")
    columns = ["code", "clump_thickness", "size_uniformity", "shape_uniformity", "adhesion", "cell_size", "bare_nuclei",
               "bland_chromatin", "normal_nuclei", "mitosis", "class"]
    df = pd.read_csv(f_name, sep=",", header=None, names=columns, na_values="?")
    return df.dropna()

def benign_malignant():
    data = get_data()
    data_x = data.ix[:, (data.columns != "class") & (data.columns != "code")].as_matrix()
    # print data_x.shape
    y = (data.ix[:, data.columns == "class"].as_matrix()).ravel()
    data_y = [0 if x == 2 else 1 for x in y] #considering 2 is benign and 4 is malignant
    # print np.unique(data_y)
    # print np.unique(y)
    # print data_y.shape
    #remvoing code because it is just an identifier and might be coded according to
    train_x, test_x, train_y, test_y = train_test_split(data_x, data_y, test_size = 0.4, random_state = 9)
    # print train_x.shape, train_y.shape
    # print test_x.shape, type(test_x), test_y.shape
    lrc = linear_model.LogisticRegression()
    lrc = lrc.fit(train_x, train_y)
    return lrc, train_x, train_y, test_x, test_y

def model_evaluation():
    model, train_x, train_y, test_x, test_y = benign_malignant()
    predicted = model.predict(test_x)
    false_positive_rate, true_positive_rate, thresholds = metric.roc_curve(test_y, predicted)
    roc_auc = metric.auc(false_positive_rate, true_positive_rate)
    plt.figure()
    plt.plot(false_positive_rate, true_positive_rate, label = "ROC curve (area = %0.2f)" %roc_auc,
                lw=2, color ="red", marker ='s', markerfacecolor ="blue")
    plt.plot([0,1],[0,1], "k--")
    #setting xlimit and ylimit to a value lesser than 0 to show the beginning of the line and the end of the curve resp
    plt.xlim([-0.005, 1.0])
    plt.ylim([0.0, 1.005])
    plt.title("Receiver Operating Characteristics for Testing Data- Logistic Regression")
    plt.legend(loc = "lower right")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    filepath = os.path.join(get_abs_path(), "static", "tmp", "roc.png")
    plt.savefig(filepath)

    confusion_matrix = metric.confusion_matrix(test_y, predicted)

    sensitivity = float(confusion_matrix[1][1]) / (float(confusion_matrix[1][1]) + float(confusion_matrix[1][0]))
    specificity = float(confusion_matrix[0, 0]) / float(confusion_matrix[0, 0] + confusion_matrix[0, 1])
    accuracy = metric.accuracy_score(test_y, predicted)
    f1_score = metric.f1_score(test_y, predicted)
    evaluation_dictionary = {"sensitivity": sensitivity, "specificity": specificity, "accuracy": accuracy,
                             "f1_score": f1_score, "roc_auc": roc_auc}
    return confusion_matrix, evaluation_dictionary

@app.route("/")
def index():
    df = get_data()
    X = df.ix[:, (df.columns != "class") & (df.columns != "code")].as_matrix()
    y = df.ix[:, df.columns == "class"].as_matrix()

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

@app.route("/d3")
def d3():
    df = get_data()
    X = df.ix[:, (df.columns != "class") & (df.columns != "code")].as_matrix()
    y = df.ix[:, df.columns == "class"].as_matrix()

    # scale data
    scaler = preprocessing.StandardScaler().fit(X)
    scaled = scaler.transform(X)

    # PCA
    pcomp = decomposition.PCA(n_components=2)
    pcomp.fit(scaled)
    components = pcomp.transform(scaled)
    var = pcomp.explained_variance_ratio_.sum()

    # Kmeans
    model = KMeans(init="k-means++", n_clusters=2)  # K-means++ ensures that the initial centroids which are chosen
    # are spaced out far apart
    model.fit(components)

    #Generate csv
    cluster_data = pd.DataFrame(
        {
            "pc1": components[:, 0],
            "pc2": components[:, 1],
            "labels": model.labels_
        }
    )
    csv_path = os.path.join(get_abs_path(), "static", "tmp", "kmeans.csv")
    cluster_data.to_csv(csv_path)
    return render_template("d3.html", data_file = url_for("static", filename = "tmp/kmeans.csv"))

@app.route("/prediction")
def prediction():
    conf_dict, eval_dict = model_evaluation()
    return render_template("prediction.html", fig = url_for("static", filename = "tmp/roc.png"),
                           model_type = "Logistic Regression")

@app.route("/api/v1/prediction_confusion_matrix")
def prediction_confusion_matrix():
    conf_dict, eval_dict = model_evaluation()
    tn = conf_dict[0][0]
    tp = conf_dict[1][1]
    fp = conf_dict[0][1]
    fn = conf_dict[1][0]
    c_dict = pd.DataFrame({"logistic regression": {"fp":fp, "tp":tp, "fn":fn, "tn":tn}})
    # c_dict = pd.DataFrame(data = conf_dict,
    #                       index = ("0", "1"),
    #                       columns = ("0", "1"))
    data = json.loads((c_dict.to_json()))
    return jsonify(data)