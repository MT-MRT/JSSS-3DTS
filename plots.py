import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns


def plotHistogram(vec1,vec2,limx,limy,bw,mjLcx,mjLcy,labelX,dimY,color,fileName):
    figSizeXmm = 80
    figSizeYmm = dimY
    fontSize = 10    
    lineWidth = 1.0    
    figSizeXinches = figSizeXmm/25.4
    figSizeYinches = figSizeYmm/25.4    
    borderPad = 0.7
        
    plt.rcParams['axes.linewidth'] = lineWidth
    plt.rcParams["figure.figsize"] = (figSizeXinches, figSizeYinches)    

    fig, axs = plt.subplots(nrows=1,ncols=2)
    sns.histplot(vec1,stat='density', kde=True,ax=axs[0], color=color,binwidth=bw)
    sns.histplot(vec2,stat='density', kde=True,ax=axs[1], color=color,binwidth=bw)

    title = ["Existing","New"]
    for i,ax in enumerate(axs):
        ax.set(xlim=(0,limx),ylim=(0,limy))    
        ax.xaxis.set_major_locator(ticker.MultipleLocator(mjLcx))
        ax.xaxis.set_major_formatter(ticker.ScalarFormatter())
        ax.yaxis.set_major_locator(ticker.MultipleLocator(mjLcy))
        ax.yaxis.set_major_formatter(ticker.ScalarFormatter())        
        ax.set_xlabel(labelX, fontsize=fontSize)        
        ax.set_ylabel(r'PDF', fontsize=fontSize)        
        ax.set_title(title[i], fontsize=fontSize) 
    fig.tight_layout(pad=borderPad)
    plt.savefig(fileName)
def plotPlanes(Model,point,axisToPlot,proyecs,fileName):
    x,y,z,xx_pred,yy_pred,predicted,vec_cent=Model.buildRegPlane(point)    
    figSizeXcm = 5
    figSizeYcm = 5
    figSizeXinches = figSizeXcm/2.54
    figSizeYinches = figSizeYcm/2.54    
    fontSize = 10    
    lineWidth = 1.0         
    ##    
    fig, axes = plt.subplots(nrows=1, ncols=1, subplot_kw=dict(projection="3d"))    
    plt.rcParams["figure.figsize"] = (figSizeXinches, figSizeYinches)            
    plt.rcParams['axes.linewidth'] = lineWidth 
            
    axes.plot(x, y, z, color='k', zorder=15, linestyle='none', marker='o', markersize=1,alpha=1)
    axes.scatter(xx_pred.flatten(), yy_pred.flatten(), predicted, facecolor=(0,0,0,0), s=0.5, edgecolor='#70b3f0')
    axes.plot(vec_cent[0], vec_cent[1], vec_cent[2], color='r', zorder=15, linestyle='none', marker='o', markersize=1,alpha=1)        
    axes.set_zlabel(r'$z^{\prime}$',fontsize=fontSize)
    if axisToPlot == 'x':
        axes.set_xlabel(r'$x^{\prime}$',fontsize=fontSize)
        axes.yaxis.set_ticklabels([])        
    elif axisToPlot == 'y':
        axes.set_ylabel(r'$y^{\prime}$',fontsize=fontSize)
        axes.xaxis.set_ticklabels([])        
    axes.set_xlim(-0.8,0.8)
    axes.set_ylim(-0.8,0.8)
    axes.set_zlim(-0.8,0.8)
    axes.set_xticks([-0.5,0,0.5])
    axes.set_yticks([-0.5,0,0.5])
    axes.set_zticks([-0.5,0,0.5])
    axes.grid()
    axes.set_proj_type('ortho')
    axes.view_init(elev=1, azim=proyecs[0])                        
    plt.savefig(fileName)