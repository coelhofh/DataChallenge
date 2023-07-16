import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import seaborn as sns; sns.set()
from tabulate import tabulate

#Elbow curves - not used in normal loading operation, just for debugging purposes
def plotElbowCurve(XOri, XDes):
    # Elbow curve - for given data only 3 clusters is necessary
    K_clusters = range(1,10)
    kmeans = [KMeans(n_clusters=i) for i in K_clusters]
    Y_axis = XOri[['oriCordLati']]
    X_axis = XOri[['oriCordLong']]
    score = [kmeans[i].fit(Y_axis).score(Y_axis) for i in range(len(kmeans))]

    # Visualize
    plt.plot(K_clusters, score)
    plt.xlabel('Number of Clusters')
    plt.ylabel('Score')
    plt.title('Elbow Curve Origin')
    plt.show()

    # Elbow curve - for given data only 3 clusters is necessary
    K_clusters = range(1,10)
    kmeans = [KMeans(n_clusters=i) for i in K_clusters]
    Y_axis = XDes[['desCordLati']]
    X_axis = XDes[['desCordLong']]
    score = [kmeans[i].fit(Y_axis).score(Y_axis) for i in range(len(kmeans))]
    # Visualize
    plt.plot(K_clusters, score)
    plt.xlabel('Number of Clusters')
    plt.ylabel('Score')
    plt.title('Elbow Curve Destination')
    plt.show()


# clustering the data with latitude and longitude for both origin and destination
def RegionCluster(fileRows):
    # create dataframe to make some treatments easier
    df = pd.DataFrame(fileRows, columns = ['idSeqFile','region','oriCordLati','oriCordLong', 'desCordLati','desCordLong', 'dtTime', 'dataSource'])

    # # Variable with the Longitude and Latitude
    XOri=df.loc[:,['idSeqFile','oriCordLati','oriCordLong']]
    XDes=df.loc[:,['idSeqFile','desCordLati','desCordLong']]

    # create clustering Origin
    # kmeans = KMeans(n_clusters = 3, init ='k-means++')
    kmeans = KMeans(n_clusters = 3, init ='k-means++', n_init = 10)
    kmeans.fit(XOri[XOri.columns[1:3]]) # k-means clustering compute
    XOri['cluster_Ori'] = kmeans.fit_predict(XOri[XOri.columns[1:3]])
    centers = kmeans.cluster_centers_ # Coordinates of cluster centers
    labels = kmeans.predict(XOri[XOri.columns[1:3]]) # Labeling
    # print(tabulate(XOri.head(10), headers = 'keys', tablefmt = 'psql'))

    # create clustering Destination
    kmeans = KMeans(n_clusters = 3, init ='k-means++', n_init = 10)
    kmeans.fit(XDes[XDes.columns[1:3]])
    XDes['cluster_Des'] = kmeans.fit_predict(XDes[XDes.columns[1:3]])
    centers = kmeans.cluster_centers_
    labels = kmeans.predict(XDes[XDes.columns[1:3]])
    # print(tabulate(XDes.head(10), headers = 'keys', tablefmt = 'psql'))

    # plot the curve for visualization
    # plotElbowCurve(XOri, XDes)


    #final dataframe
    dfFinal = df.merge(XOri[['idSeqFile','cluster_Ori']], left_on='idSeqFile', right_on='idSeqFile').merge(XDes[['idSeqFile','cluster_Des']], left_on='idSeqFile', right_on='idSeqFile')

    print("Region clusters calculated. {} total rows.".format(len(fileRows)))

    # return as list
    return dfFinal.iloc[: , 1:].values.tolist()
