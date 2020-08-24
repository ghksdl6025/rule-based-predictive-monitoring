import pandas as pd
from xgboost import XGBClassifier,plot_importance
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt
from playsound import playsound
import numpy as np
import json
import os
# dataset = pd.read_csv('./bpic2015/ltl1/bpic2015_1/indexbase/prefix5/simple_timediscretize/ARMinput_preprocessed.csv')
# label = []
# for k in list(dataset['Label_1']):
#     if k==1:
#         label.append(1)
#     else:
#         label.append(0)
# y = label
# dataset = dataset.drop(['Label_1','Label_0','Case ID'],axis=1)

# x_train,x_test,y_train,y_test = train_test_split(dataset,y,test_size=0.3,random_state = 0)


# xgb = XGBClassifier(n_estimators = 500,learning_rate=0.1,max_depth=4)
# xgb.fit(x_train,y_train)
# xgb_pred = xgb.predict(x_test)
# print(classification_report(y_test,xgb_pred))

# fig,ax = plt.subplots()
# plot_importance(xgb,ax=ax)
# plt.show()

def cuttinginput(df,alpha):
    try:
        df = df.rename(columns={'Label_1.0':'Label_1','Label_0.0':'Label_0'})
    except:
        pass

    df_cols =df.columns.values
    df_collist=['Case ID','Label_1','Label_0']
    for k in df_cols:
        if round(len(df[df[k]==1])/len(df),2) >alpha:
            if k not in df_collist:
                df_collist.append(k)

    df = df.loc[:,df_collist]
    return df, df_collist



def xgboosting():
    for prefixlength in range(2,11):
        resultdict={}
        resultdict['Label 0'] ={'precision':[],'recall':[],'f1-score':[],'support':[]}
        resultdict['Label 1'] ={'precision':[],'recall':[],'f1-score':[],'support':[]}
        for rndst in range(0,5):
            print('Prefix :%s Rndst :%s'%(prefixlength,rndst))
            alpha = 0
            wholefile = './sepsis/rule1/indexbase/prefix'+str(prefixlength)+'/simple_timediscretize/ARMinput_preprocessed.csv'
            wholefile = pd.read_csv(wholefile)

            wholefile,wh_collist = cuttinginput(wholefile,alpha)
           
            train ,test = train_test_split(wholefile,test_size=0.3)
            label = []
            try:
                train = train.rename(columns={'Label_1.0':'Label_1','Label_0.0':'Label_0'})
            except:
                pass

            try:
                test = test.rename(columns={'Label_1.0':'Label_1','Label_0.0':'Label_0'})
            except:
                pass

            for k in list(train['Label_1']):
                if k==1:
                    label.append(1)
                else:
                    label.append(0)
            y_train = label
            train = train.drop(['Label_1','Label_0','Case ID'],axis=1)
            try:
                test = test.drop(['Unnamed: 0'],axis=1)
            except:
                pass
            x_train = train

            label = []
            for k in list(test['Label_1']):
                if k==1:
                    label.append(1)
                else:
                    label.append(0)

            y_test = label
            test = test.drop(['Label_1','Label_0','Case ID'],axis=1)
            x_test = test

            xgb = XGBClassifier(n_estimators = 500,learning_rate=0.1,max_depth=4)
            xgb.fit(x_train,y_train)
            xgb_pred = xgb.predict(x_test)
            result =classification_report(y_test,xgb_pred,target_names=['Label 0','Label 1'],output_dict=True)
            resultdict['Label 0']['precision'].append(result['Label 0']['precision'])
            resultdict['Label 0']['recall'].append(result['Label 0']['recall'])
            resultdict['Label 0']['f1-score'].append(result['Label 0']['f1-score'])
            resultdict['Label 0']['support'].append(result['Label 0']['support'])
            resultdict['Label 1']['precision'].append(result['Label 1']['precision'])
            resultdict['Label 1']['recall'].append(result['Label 1']['recall'])
            resultdict['Label 1']['f1-score'].append(result['Label 1']['f1-score'])
            resultdict['Label 1']['support'].append(result['Label 1']['support'])

        for pre in resultdict.keys():
            for col in resultdict[pre].keys():
                resultdict[pre][col] = [np.mean(resultdict[pre][col]),np.std(resultdict[pre][col])]
                
        resultdir = './sepsis/rule1/ruleresult/xgboost/'
        try:
            os.makedirs(resultdir)
        except:
            pass
        jsonname = resultdir+'/prefix'+str(prefixlength)+'result.json'
        with open(jsonname ,'w') as f:
            json.dump(resultdict,f)

'''
for prefixlength in range(2,10):
    resultdict={}
    resultdict['Label 0'] ={'precision':[],'recall':[],'f1-score':[],'support':[]}
    resultdict['Label 1'] ={'precision':[],'recall':[],'f1-score':[],'support':[]}

    alpha = 0.2
    wholefile = './road traffic/rule1/indexbase/prefix'+str(prefixlength)+'/simple_timediscretize/ARMinput_preprocessed.csv'
    wholefile = pd.read_csv(wholefile)

    wholefile,wh_collist = cuttinginput(wholefile,alpha)
    print('Prefix :%s '%(prefixlength), len(wh_collist))
'''
xgboosting()


playsound('../Yattong+edited+version.mp3')

