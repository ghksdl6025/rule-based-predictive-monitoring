import pandas as pd
import json
import numpy as np
from collections import Counter
import ast
from sklearn.cluster import KMeans
import math
from playsound import playsound
from tqdm import tqdm

def ersecommonrule(both_label):
    label0df = both_label[0]
    label1df = both_label[1]
    label0rule = []
    label1rule = []

    for x in label0df['antecedents']:
        x = sorted(ast.literal_eval(x))
        label0rule.append(str(x))

    for x in label1df['antecedents']:
        x = sorted(ast.literal_eval(x))
        label1rule.append(str(x))
    label0rules = frozenset(label0rule)
    label1rules = frozenset(label1rule)
    commonrule = label0rules.intersection(label1rules)
    print(len(commonrule))
    unqiuelabel0 = [pos for pos,x in tqdm(enumerate(label0rule)) if x not in commonrule]
    unqiuelabel1 = [pos for pos,x in tqdm(enumerate(label1rule)) if x not in commonrule]
    
    return label0df.iloc[unqiuelabel0,:], label1df.iloc[unqiuelabel1,:]

def summarizerule(ndf):
    if len(ndf) ==0:
        return {}
    # ndf['conviction dist'] =abs(ndf['conviction'] - 1)
    groups = ndf.groupby('antecedents')
    rulebeforeclustering=[]
    for case, group in groups:
        group = group.sort_values(by='conviction',ascending=False)
        group = group.reset_index(drop=True)
        rulebeforeclustering.append(group.iloc[0,:])
        
    ndf = pd.DataFrame(rulebeforeclustering).reset_index(drop=True)
    allelement = set()
    for x in list(ndf['antecedents']):
        x = ast.literal_eval(x)
        for k in x:
            allelement.add(k)
    
    for pos,x in enumerate(list(ndf['antecedents'])):
        x = ast.literal_eval(x)
        for k in allelement:
            if k in x:
                ndf.loc[pos,k] =1
            else:
                ndf.loc[pos,k] =0

    try:
        model = KMeans(n_clusters=20)
        model.fit(ndf.loc[:,allelement])

        y_predict = model.fit_predict(ndf.loc[:,allelement])

        ndf['cluster'] = y_predict
        groups = ndf.groupby('cluster')
        topsupport = []
        for case, group in groups:
            group = group.sort_values(by='support',ascending=False)
            group = group.reset_index(drop=True)
            topsupport.append(group.iloc[0,:])
        ndf = pd.DataFrame(topsupport)
    except:
        pass
    ndf = ndf.reset_index(drop=True)
    supportlist= []
    for x in ndf['support']:
        supportlist.append(int(x*10)/10)
    ndf['support'] =supportlist
    data ={}
    for pos,x in enumerate(list(ndf['antecedents'])):
        x = ast.literal_eval(x)
        rule = '/'.join(x)
        supp = ndf.loc[pos,'support']
        if supp not in list(data.keys()):
            data[ndf.loc[pos,'support']] = [rule]
        else:
            data[ndf.loc[pos,'support']].append(rule)
    return data
    


if __name__ =="__main__":
    for prefix in range(2,11):
        for rndst in range(0,5):
            label_ruledf = []
            print('Prefix ', prefix, "Rnd", rndst)
            for label in [0,1]:
                data=[]
                for supp in [0.9]:
                    df =  pd.read_csv('./sepsis/rule1/indexbase/prefix'+str(prefix)+'/simple_timediscretize/threshold0.9/support_'+str(supp)+'/label'+str(label)+'result_rndst'+str(rndst)+'.csv')                    
                    # if len(df) !=0:
                    data.append(df)

                ndf = pd.concat(data)
                label_ruledf.append(ndf)
            data={}
            label0df, label1df = ersecommonrule(label_ruledf)
            data['Label_0'] = summarizerule(label0df)
            data['Label_1'] = summarizerule(label1df)
            rulefilename = './sepsis/rule1//ruleresult/way3/threshold0.9/Summarized_Rule_prefix'+str(prefix)+'_rnd'+str(rndst)+'.json'
            with open(rulefilename,'w') as f:
                json.dump(data,f)
    playsound('../Yattong+edited+version.mp3')
