def image_heatmap_2D_x_y(filepath,qual_angle):
    #Average of the voxels normal to the plane plotted
    if qual_angle == True:
        angle = "qualfactorangle"
    
    else:
        angle= "angle"
        
    df = pd.read_csv(filepath)
    print(df)
    df['X'] = df['X'].str.strip('(]')
    df['Y'] = df['Y'].str.strip('(]')
    df[angle] = df[angle].astype(float)
    df[angle] = df[angle].fillna(0)
    for index, row in df.iterrows():

        df.loc[index,"X"] = math.ceil(np.average(np.fromstring(df.loc[index,"X"],sep=",")))
        df.loc[index,"Y"] = math.ceil(np.average(np.fromstring(df.loc[index,"Y"],sep=",")))

    x_val = df.loc[:,"X"]
    y_val = df.loc[:,"Y"]
    angles = df.loc[:,angle]
    
    pivot = df.pivot(values = angle,columns='X',index='Y')
    sns.heatmap(pivot,cmap = 'Spectral_r').axis('equal')
    
    plt.savefig(filepath[:-4]+"xy.png")
    plt.show()
    return(None)
def image_heatmap_2D_x_z(filepath, detector_corners,qual_angle):
    #Average of the voxels normal to the plane plotted
    if qual_angle == True:
        angle = "qualfactorangle"
    
    else:
        angle= "angle"
        
    xticksww = np.linspace(-detector_corners[0][0],detector_corners[0][0],29)
    xticksww = np.around(xticksww,-1)
    
    zticks = np.linspace(-detector_corners[0][2],detector_corners[0][2],19)
    zticks = np.around(zticks,-1)
    
    
    
    df = pd.read_csv(filepath)
    
    #df.rename(columns={0: 'X',  1: 'Z', 2: 'angle'}, inplace=True)
    print(df)
    df['X'] = df['X'].str.strip('(]')
    df['Z'] = df['Z'].str.strip('(]')
    df[angle] = df[angle].astype(float)
    df[angle] = df[angle].fillna(0)
    for index, row in df.iterrows():

        df.loc[index,"X"] = math.ceil(np.average(np.fromstring(df.loc[index,"X"],sep=",")))
        df.loc[index,"Z"] = math.ceil(np.average(np.fromstring(df.loc[index,"Z"],sep=",")))

    x_val = df.loc[:,"X"]
    y_val = df.loc[:,"Z"]
    angles = df.loc[:,angle]
    
    #object_outline
    #outline_x = [1000,1000,-1000,-1000]
    #outline_z = [-75,75,75,-75]
    
    
    pivot = df.pivot(values = angle,columns='X',index='Z')
    #plt.plot(outline_x, outline_z, linestyle='dashed', color='black')
    #sns.heatmap(pivot,cmap = 'Spectral_r',yticklabels = zticks, xticklabels=xticksww).axis('equal')
    sns.heatmap(pivot,cmap = 'Spectral_r').axis('equal')
    #, yticklabels = zticks,
    
    plt.savefig(filepath[:-4]+"xz.png")
    plt.show()
    return(None)
def image_heatmap_2D_y_z(filepath,qual_angle):
    #Average of the voxels normal to the plane plotted
    if qual_angle == True:
        angle = "qualfactorangle"
    
    else:
        angle= "angle"
    
    df = pd.read_csv(filepath)
    

    df['Y'] = df['Y'].str.strip('(]')
    df['Z'] = df['Z'].str.strip('(]')
    df[angle] = df[angle].astype(float)
    df[angle] = df[angle].fillna(0)
    for index, row in df.iterrows():

        df.loc[index,"Y"] = math.ceil(np.average(np.fromstring(df.loc[index,"Y"],sep=",")))
        df.loc[index,"Z"] = math.ceil(np.average(np.fromstring(df.loc[index,"Z"],sep=",")))

    x_val = df.loc[:,"Y"]
    y_val = df.loc[:,"Z"]
    angles = df.loc[:,angle]
    
    pivot = df.pivot(values = angle,columns='Y',index='Z')
    sns.heatmap(pivot,cmap = 'Spectral_r').axis('equal')
    
    plt.savefig(filepath[:-4]+"yz.png")
    plt.show()
    return(None)