# -*- coding: utf-8 -*-
"""
@author: Miguel Mendez
Affiliation: Department of Measurement and Control
Mechanical Engineering Faculty - Universty of Kassel
email: miguel.mendez@mrt.uni-kassel.de
"""
import os
from PC_PostProcess import PC_postProcessed
from plots import *

def get_sigma(model1,model2,dir_sigma):
    vec1,vec2 = model1.sampledData[dir_sigma].values*1000,model2.sampledData[dir_sigma].values*1000
    return vec1,vec2
def process_3DTS():
    #Define where the data is located.
    pathMC3D="PC_Temp/DF_MC3D_4.ply"
    pathRS="PC_Temp/DF_RS_3.ply"
    
    print("Load data")
    MC3D_model = PC_postProcessed(pathMC3D)
    RS_model = PC_postProcessed(pathRS)
    
    print("Get and plot standard deviations of the sampled neighborhoods")
    for sigma in ["sigma_x","sigma_y","sigma_z"]:
        MC3D_sigma, RS_sigma = get_sigma(MC3D_model,RS_model,sigma)
        plotHistogram(MC3D_sigma,RS_sigma,6,2.6,0.1,1,0.6,r"$\sigma_{x}$ in mm",40,'saddlebrown',sigma+".svg")
    
    print("Get point information and plot its Neighborhood")
    pointMC3D, pointRS = 0,0
    print("Point MC3D: {0} and Point RS: {1}".format(pointMC3D,pointRS))
    print("MC3D-> e1: {0:4e}, e2: {1:4e}, e3: {2:4e}, curvature: {3:4e}, NumPoints: {4:d}".format(MC3D_model.cloud.points["e1(11)"][pointMC3D],
                                                                                                  MC3D_model.cloud.points["e2(11)"][pointMC3D],
                                                                                                  MC3D_model.cloud.points["e3(11)"][pointMC3D],
                                                                                                  MC3D_model.cloud.points["curvature(11)"][pointMC3D],
                                                                                                  len(MC3D_model.cloud.points)))
    print("RS-> e1: {0:4e}, e2: {1:4e}, e3: {2:4e}, curvature: {3:4e}, NumPoints: {4:d}".format(RS_model.cloud.points["e1(11)"][pointRS],
                                                                                                RS_model.cloud.points["e2(11)"][pointRS],
                                                                                                RS_model.cloud.points["e3(11)"][pointRS],
                                                                                                RS_model.cloud.points["curvature(11)"][pointRS],
                                                                                                len(RS_model.cloud.points)))

    plotPlanes(MC3D_model,0,'x',[90],'planeMC3D_x.svg')
    plotPlanes(MC3D_model,0,'y',[0],'planeMC3D_y.svg')       
    plotPlanes(RS_model,0,'x',[90],'planeRS_x.svg')
    plotPlanes(RS_model,0,'y',[0],'planeRS_y.svg')

    print("Get and plot curvature")
    MC3D_curvature, RS_curvature = MC3D_model.cloud.points["curvature(11)"][:],RS_model.cloud.points["curvature(11)"][:]
    plotHistogram(MC3D_curvature,RS_curvature,1,3,0.01,0.3,0.4,r"curvature",50,'green',"curvature.svg")

    print("Get and plot surfel radius")
    MC3D_radius, RS_radius = MC3D_model.cloud.points["radius"][:]*1000,RS_model.cloud.points["radius"][:]*1000
    plotHistogram(MC3D_radius,RS_radius,8,2.5,0.01,1,0.4,r"radius in mm/px",40,'green',"radius.svg")

if __name__=="__main__":
    process_3DTS()