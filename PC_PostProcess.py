# -*- coding: utf-8 -*-
"""
@author: Miguel Mendez
Affiliation: Department of Measurement and Control
Mechanical Engineering Faculty - Universty of Kassel
email: miguel.mendez@mrt.uni-kassel.de
"""
import numba as nb
import numpy as np
import pandas as pd
from pyntcloud import PyntCloud
from sklearn import linear_model

class PC_postProcessed: 
    def __init__(self, objPath):
        self.objPath= objPath
        print("Begin loading point cloud")
        self.cloud = PyntCloud.from_file(self.objPath)
        print("Begin geometry feature extraction.")
        k_neighbors = self.cloud.get_neighbors(k=10)
        self.radius = self.cloud.points["radius"][:]*1000
        self.ev = self.cloud.add_scalar_field("eigen_values", k_neighbors=k_neighbors)        
        self.get_feature_vector("curvature")        
        self.getStdNgbh()
    def get_feature_vector(self,indc):        
            self.cloud.add_scalar_field(indc, ev=self.ev)
    def getFeaturevalue(self,FeaturePoints):
        return self.cloud.points[FeaturePoints].to_numpy()    
    def getStdNgbh(self):
        @nb.jit(nopython=True)
        def assign_values(case, cloud_points, p,col):
            for j in range(len(case)):
                case [j] = cloud_points [p[j]][col]    
            return case         
        keysSigma = ['sigma_x','sigma_y','sigma_z']
        self.sampledData = pd.DataFrame(columns = keysSigma)
        self.sampledData['orgIndex']=0
        x,y,z=np.zeros(10),np.zeros(10),np.zeros(10)
        index_Proc = np.random.randint(0,len(self.cloud.points), 100)
        cloud_point_list = self.cloud.points.values
        for j,indData in enumerate(index_Proc):
            p = self.cloud.get_neighbors(k=10)[indData]
            for i,case in enumerate([x,y,z]):                    
                case[:]=assign_values(case, cloud_point_list, p,i)
                self.sampledData.loc[j,[keysSigma[i]]] = np.std(case,ddof=1)
                self.sampledData.loc[j,['orgIndex']] = indData
    def getVecs(self,point):
        dfPoints=self.cloud.points
        p=self.cloud.get_neighbors(k=10)[point]
        x,y,z=np.zeros(10),np.zeros(10),np.zeros(10)
        for i in range(10):
            x[i]=dfPoints["x"][p[i]]
            y[i]=dfPoints["y"][p[i]]
            z[i]=dfPoints["z"][p[i]]
        return x,y,z
    def rescale_vecs(self,arr):
        return (arr-np.mean(arr))/(np.max(arr)-np.min(arr))
    def buildRegPlane(self,point):
        x,y,z = self.getVecs(point)        
        x=self.rescale_vecs(x)
        y=self.rescale_vecs(y)
        z=self.rescale_vecs(z)                    
        x_cent=np.mean(x)
        y_cent=np.mean(y)
        z_cent=np.mean(z)
        X=np.vstack((x,y))
        X=X.T
        Y= z
        x_pred,y_pred=np.linspace(min(x),max(x)),np.linspace(min(y),max(y))
        xx_pred, yy_pred = np.meshgrid(x_pred, y_pred)
        model_viz = np.array([xx_pred.flatten(), yy_pred.flatten()]).T
        ols = linear_model.LinearRegression()
        model = ols.fit(X, Y)
        predicted = model.predict(model_viz)              
        vec_cent=[x_cent,y_cent,z_cent]
        return [x,y,z,xx_pred,yy_pred,predicted,vec_cent]            

