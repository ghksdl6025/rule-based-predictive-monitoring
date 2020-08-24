import pandas as pd
import os 
from tqdm import tqdm
from playsound import playsound
import warnings
def trafficlabeling(df):
    groups = df.groupby('Case ID')
    labelas1 =[]
    for case,group in groups:
        actlist = list(group['concept:name'])
        if 'Send for Credit Collection' in actlist:
            labelas1.append(case)
    df['Traffic_label'] =0
    
    df.loc[df['case_name'].isin(labelas1),'Traffic_label'] =1
    return df


def morethan(df,length):
    df['Complete Timestamp'] = pd.to_datetime(df['Complete Timestamp'])
    groups = df.groupby('Case ID')
    lenmorethan=[]
    
    for case, group in tqdm(groups):
        group = group.sort_values(by='Complete Timestamp').reset_index(drop=True)
        if len(group) >length:
            addgroup = group.iloc[:length,:]
            activitylist = list(addgroup['Activity'])
            if 'Release A' in activitylist:
                pass
            else:
                lenmorethan.append(addgroup)
    df = pd.concat(lenmorethan)
    return df




if __name__ =='__main__':
    warnings.filterwarnings(action='ignore')
    for x in range(2,11):
        length = x
        df = pd.read_csv('../sepsis/Sepsis Cases_pre.csv')
        print('Prefix :', length)
        df = morethan(df,length)
        dir_path = '../sepsis/rule1/prefix'+str(length)
        try:
            os.makedirs(dir_path)
        except:
            pass

        df.to_csv(dir_path+'/Sepsis Cases_prep.csv',index=False)
    playsound('../Yattong edited version.mp3')