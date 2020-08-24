import os
import pandas as pd
import numpy as np
import json
from mlxtend.frequent_patterns import fpgrowth,apriori
from mlxtend.frequent_patterns import association_rules
from playsound import playsound
from tqdm import tqdm

def cuttinginput(df,alpha):
    try:
        df = df.rename(columns={'Label_1.0':'Label_1','Label_0.0':'Label_0'})
    except:
        pass
    print(len(df.columns.values))
    df_cols =df.columns.values
    df_collist=['Case ID','Label_1','Label_0']
    for k in df_cols:
        if round(len(df[df[k]==1])/len(df),2) >alpha:
            if k not in df_collist:
                df_collist.append(k)

    df = df.loc[:,df_collist]
    print(len(df_collist))
    return df, df_collist



def bpic2015():
    for rndst in [0,1,2,3,4]:
        for length in range(2,11):
            for support in [0.9]:
                alpha=0.4

                print('Prefix :%s Support :%s Rndst :%s'%(length,support,rndst))       
                dir_path = './sepsis/rule1/indexbase/prefix'+str(length)+'/simple_timediscretize'
                filename = dir_path + '/train_rndst'+str(rndst)+'.csv'
                wholefile = dir_path+'/ARMinput_preprocessed.csv'
                wholefile,wh_collist = cuttinginput(pd.read_csv(wholefile),alpha)

                df = pd.read_csv(filename)
                try:
                    df = df.rename(columns={'Label_1.0':'Label_1','Label_0.0':'Label_0'})
                except:
                    pass
                threshold = 0.9
                df =df.loc[:,wh_collist]
                min_support = support
                min_threshold = threshold
                dir_path=dir_path+'/threshold'+str(threshold)+'/support_'+str(min_support)
                try:
                    os.makedirs(dir_path)
                except:
                    pass

                df = df.drop(columns=['Case ID'],axis=1)

                accepted = df[df['Label_1']==1]
                refused = df[df['Label_0']==1]
                '''
                Accepted
                '''
                frequent_itemsets = apriori(accepted,min_support=min_support,use_colnames=True)
                label1 = association_rules(frequent_itemsets,metric='confidence',min_threshold = min_threshold)
                label1['consequents'] = [list(x) for x in list(label1['consequents'])]

                labelin=[]
                for pos,x in enumerate(list(label1['consequents'])):
                    if 'Label_1' in x:
                        labelin.append(pos)
            
                label1_name = dir_path+'/association_result_1_rnd'+str(rndst)+'.json'
                label1 = label1.loc[labelin,:]#['antecedents','consequents']]
                label1['antecedents'] = [list(x) for x in list(label1['antecedents'])] 
                label1.to_json(label1_name,orient='columns')
                label1.to_csv(dir_path+'/label1result_rndst'+str(rndst)+'.csv',index=False)


                
                '''
                Refused
                '''
                # print('Label 0!')
                frequent_itemsets = apriori(refused,min_support=min_support,use_colnames=True)
                label1 = association_rules(frequent_itemsets,metric='confidence',min_threshold = min_threshold)
                label1['consequents'] = [list(x) for x in list(label1['consequents'])]

                labelin=[]
                for pos,x in enumerate(list(label1['consequents'])):
                    if 'Label_0' in x:
                        labelin.append(pos)

                label1_name = dir_path+'/association_result_0_rnd'+str(rndst)+'.json'
                label1 = label1.loc[labelin,:]#['antecedents','consequents']]
                label1['antecedents'] = [list(x) for x in list(label1['antecedents'])]
                label1.to_json(label1_name,orient='columns')
                label1.to_csv(dir_path+'/label0result_rndst'+str(rndst)+'.csv',index=False)




def bpic2011():
    for rndst in [0]:
        for length in range(2,3):
            for support in [0.9]:
                alpha=0.4
                print('Prefix :%s Support :%s Rndst :%s'%(length,support,rndst))
                
                dir_path = './sepsis/rule1/indexbase/prefix'+str(length)+'/simple_timediscretize'
                filename = dir_path + '/train_rndst'+str(rndst)+'.csv'
                wholefile = dir_path+'/ARMinput_preprocessed.csv'
                
                wholefile,wh_collist = cuttinginput(pd.read_csv(wholefile),alpha)

                df = pd.read_csv(filename)
                try:
                    df = df.rename(columns={'Label_1.0':'Label_1','Label_0.0':'Label_0'})
                except:
                    pass
                threshold = 0.9
                df =df.loc[:,wh_collist]
                min_support = support
                min_threshold = threshold
                dir_path=dir_path+'/withoutsparse_'+str(alpha)+'/threshold'+str(threshold)+'/support_'+str(min_support)
                try:
                    os.makedirs(dir_path)
                except:
                    pass

                df = df.drop(columns=['Case ID'],axis=1)

                accepted = df[df['Label_1']==1]
                refused = df[df['Label_0']==1]
                
                print('Label 1!')

                frequent_itemsets = apriori(accepted,min_support=min_support,use_colnames=True)
                label1 = association_rules(frequent_itemsets,metric='confidence',min_threshold = min_threshold)
                label1['consequents'] = [list(x) for x in list(label1['consequents'])]

                labelin=[]
                for pos,x in tqdm(enumerate(list(label1['consequents']))):
                    if 'Label_1' in x:
                        labelin.append(pos)
                
                label1 = label1.loc[labelin,:]
                label1_name = dir_path+'/association_result_1_rnd'+str(rndst)+'.json'

                label1 = label1.loc[labelin,:]#['antecedents','consequents']]
                label1 = label1.reset_index(drop=True)
                label1['antecedents'] = [list(x) for x in list(label1['antecedents'])] 
                label1.to_csv(dir_path+'/label1result_rndst'+str(rndst)+'.csv',index=False)

                label1 = label1.loc[labelin,['antecedents','consequents']]
                label1.to_json(label1_name,orient='columns')
                
                print('Label 0!')
                frequent_itemsets = apriori(refused,min_support=min_support,use_colnames=True)
                label1 = association_rules(frequent_itemsets,metric='confidence',min_threshold = min_threshold)
                label1['consequents'] = [list(x) for x in list(label1['consequents'])]

                labelin=[]
                for pos,x in tqdm(enumerate(list(label1['consequents']))):
                    if 'Label_0' in x:
                        labelin.append(pos)

                label1 = label1.loc[labelin,:]
                label1_name = dir_path+'/association_result_0_rnd'+str(rndst)+'.json'
                label1['antecedents'] = [list(x) for x in list(label1['antecedents'])]
                label1.to_json(label1_name,orient='columns')
                label1.to_csv(dir_path+'/label0result_rndst'+str(rndst)+'.csv',index=False)


                
bpic2015()
# bpic2011()
playsound('../Yattong+edited+version.mp3')