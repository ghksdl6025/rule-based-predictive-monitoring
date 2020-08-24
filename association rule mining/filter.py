import json

import pandas as pd
import matplotlib.pyplot as plt

from tqdm import tqdm
from itertools import combinations
import re
from collections import Counter
import os
from playsound import playsound

def way1():
    for prefixlength in range(2,11):
        acceptruledict={}
        refuseruledict={}
        ruleset=set()
        for support in [0.4,0.5,0.6,0.7,0.8,0.9]:
            # prefixlength = 6
            # support = 0.7
            print(prefixlength)
            print(support)
            
            dir_path = './prefix'+str(prefixlength)+'/simple_timediscretize/fpgrowth/support_'+str(support)
            accepted = dir_path+'/association_result_1.json'
            refused = dir_path+'/association_result_0.json'

            with open(accepted) as json_file:
                accepted = json.load(json_file)

            with open(refused) as json_file:
                refused = json.load(json_file)

            accept = set()
            acceptconse = list(accepted['consequents'].values())
            for pos,x in enumerate(list(accepted['antecedents'].values())):
                cons = acceptconse[pos]
                cons.remove('Label_1')
                rule = sorted(x) + ['/']+sorted(cons)
                accept.add(tuple(rule))

            refuse = set()
            refuseconse = list(refused['consequents'].values())
            for pos,x in enumerate(list(refused['antecedents'].values())):
                cons = refuseconse[pos]
                cons.remove('Label_0')
                rule = sorted(x) + ['/']+sorted(cons)
                refuse.add(tuple(rule))

            uniqueaccept=[]
            uniquerefuse=[]
            common=[]
            for rule in tqdm(accept):
                if rule not in refuse:
                    uniqueaccept.append(rule)
                else:
                    common.append(rule)

            for rule in tqdm(refuse):
                if rule not in accept:
                    uniquerefuse.append(rule)
            


            for pos,uniqacc in enumerate(uniqueaccept):
                uniqueaccept[pos] = uniqacc[:uniqacc.index('/')]
            
            for pos,uniqref in enumerate(uniquerefuse):
                uniquerefuse[pos] = uniqref[:uniqref.index('/')]



            accepted['antecedents']=uniqueaccept
            refused['antecedents']=uniquerefuse
            count = 's'+str(support)

            for k in set(uniqueaccept):
                if k not in acceptruledict.keys():
                    acceptruledict[k]=[]
                    acceptruledict[k].append(count)
                else:
                    acceptruledict[k].append(count)

        print('Prefix : %s'%(prefixlength))
        valedict={}
        for k in acceptruledict.keys():
            supportlevel =''
            for t in acceptruledict[k]:
                supportlevel =supportlevel+' '+t

            if supportlevel not in list(valedict.keys()):
                valedict[supportlevel] = [k]
            else:
                valedict[supportlevel].append(k)

        dir_path = './ruleresult/'
        try:
            os.makedirs(dir_path)
        except:
            pass
        json_name = dir_path+'/prefix_'+str(prefixlength)+'.json'
        print(json_name)
        with open(json_name,'w') as json_file:
            json.dump(valedict,json_file)



def way2():
    for rndst in range(0,10):
        for prefixlength in range(2,11):
            label1ruledict={}
            label0ruledict={}
            label0rule=set()
            label1rule=set()
            ruleset=set()
            threshold=0.7
            for support in [0.8,0.85,0.9]:
                    print('Prefix : %s, Support :%s'%(prefixlength,support))

                    dir_path = './bpic2011/ltl2/indexbase/prefix'+str(prefixlength)+'/simple_timediscretize'+'/threshold'+str(threshold)+'/support_'+str(support)
                    label1 = dir_path+'/association_result_1_rnd'+str(rndst)+'.json'
                    label0 = dir_path+'/association_result_0_rnd'+str(rndst)+'.json'
                    label1ruledict[support] =set()
                    label0ruledict[support] =set()

                    with open(label1) as json_file:
                        label1 = json.load(json_file)['antecedents']

                    with open(label0) as json_file:
                        label0 = json.load(json_file)['antecedents']

                    for rule in label1.values():
                        if len(rule) != 1:
                            rule = sorted(rule)
                            rule = '/'.join(rule)                               
                        else:
                            rule = rule[0]
                        label1ruledict[support].add(rule)
                        label1rule.add(rule)

                    for rule in label0.values():
                        if len(rule) !=1:
                            rule = sorted(rule)
                            rule = '/'.join(rule)                               
                        else:
                            rule = rule[0]
                        label0ruledict[support].add(rule)
                        label0rule.add(rule)

            for support in [0.6,0.7]:
                    print('Prefix : %s, Support :%s'%(prefixlength,support))

                    dir_path = './bpic2011/ltl2/indexbase/prefix'+str(prefixlength)+'/simple_timediscretize'+'/threshold'+str(threshold)+'/support_'+str(support)
                    label0 = dir_path+'/association_result_0_rnd'+str(rndst)+'.json'
                    label0ruledict[support] =set()

                    with open(label0) as json_file:
                        label0 = json.load(json_file)['antecedents']

                    for rule in label0.values():
                        if len(rule) !=1:
                            rule = sorted(rule)
                            rule = '/'.join(rule)                               
                        else:
                            rule = rule[0]
                        label0ruledict[support].add(rule)
                        label0rule.add(rule)

            for supp in label1ruledict.keys():
                rules = list(label1ruledict[supp])
                for value in rules:
                    if value in label0rule:
                        label1ruledict[supp].remove(value)
            for supp in label0ruledict.keys():
                rules = list(label0ruledict[supp])
                for value in rules:
                    if value in label1rule:
                        label0ruledict[supp].remove(value)
            for k in list(label1ruledict.keys()):
                if len(label1ruledict[k])==0:
                    del label1ruledict[k]
                else:
                    label1ruledict[k] = list(label1ruledict[k])

            for k in list(label0ruledict.keys()):
                if len(label0ruledict[k])==0:
                    del label0ruledict[k]
                else:
                    label0ruledict[k] = list(label0ruledict[k])
            
            ruleresult = './bpic2011/ltl2/ruleresult/way3/bpic2011/threshold'+str(threshold)
            try:
                os.makedirs(ruleresult)
            except:
                pass
            json_name = ruleresult+'/prefix_'+str(prefixlength)+'_label1_rnd_'+str(rndst)+'.json'
            with open(json_name,'w') as json_file:
                json.dump(label1ruledict,json_file)

            json_name = ruleresult+'/prefix_'+str(prefixlength)+'_label0_rnd_'+str(rndst)+'.json'
            print(json_name)
            with open(json_name,'w') as json_file:
                json.dump(label0ruledict,json_file)


def way3():
    for rndst in [0,1,2,3,4]:
        for prefixlength in range(2,11):
            label1ruledict={}
            label0ruledict={}
            label0rule=set()
            label1rule=set()
            ruleset=set()
            threshold=0.9
            label1count = 0
            label0count = 0
            for support in [0.9]:
                    print('Prefix : %s, Support :%s'%(prefixlength,support))
                    dir_path = './sepsis/rule1//indexbase/prefix'+str(prefixlength)+'/simple_timediscretize/threshold'+str(threshold)+'/support_'+str(support)
                    label1 = dir_path+'/association_result_1_rnd'+str(rndst)+'.json'
                    label0 = dir_path+'/association_result_0_rnd'+str(rndst)+'.json'
                    label1ruledict[support] =set()
                    label0ruledict[support] =set()

                    with open(label1) as json_file:
                        label1 = json.load(json_file)['antecedents']

                    with open(label0) as json_file:
                        label0 = json.load(json_file)['antecedents']

                    for rule in label1.values():
                        if len(rule) != 1:
                            rule = sorted(rule)
                            rule = '/'.join(rule)                               
                        else:
                            rule = rule[0]                        
                        if rule not in label1rule:
                            label1ruledict[support].add(rule)
                            label1rule.add(rule)
                        else:
                            label1count +=1

                    for rule in label0.values():
                        if len(rule) !=1:
                            rule = sorted(rule)
                            rule = '/'.join(rule)                               
                        else:
                            rule = rule[0]
                        
                        if rule not in label0rule:
                            label0ruledict[support].add(rule)
                            label0rule.add(rule)
                        else:
                            label0count +=1
            

            for supp in label1ruledict.keys():
                rules = list(label1ruledict[supp])
                for value in rules:
                    if value in label0rule:
                        label1ruledict[supp].remove(value)

            for supp in label0ruledict.keys():
                rules = list(label0ruledict[supp])
                for value in rules:
                    if value in label1rule:
                        label0ruledict[supp].remove(value)

            for k in list(label1ruledict.keys()):
                if len(label1ruledict[k])==0:
                    del label1ruledict[k]
                else:
                    label1ruledict[k] = list(label1ruledict[k])

            for k in list(label0ruledict.keys()):
                if len(label0ruledict[k])==0:
                    del label0ruledict[k]
                else:
                    label0ruledict[k] = list(label0ruledict[k])
            
            label0rulelist = []
            label1rulelist = []
            for k in label0ruledict.values():
                label0rulelist +=k
            
            for k in label1ruledict.values():
                label1rulelist +=k
            
            for s in label0rulelist:
                if s in label1rulelist:
                    print(s)

            ruleresult = './sepsis/rule1/ruleresult/way3/threshold'+str(threshold)
            try:
                os.makedirs(ruleresult)
            except:
                pass

            json_name = ruleresult+'/prefix_'+str(prefixlength)+'_label1_rnd_'+str(rndst)+'.json'
            with open(json_name,'w') as json_file:
                json.dump(label1ruledict,json_file)

            json_name = ruleresult+'/prefix_'+str(prefixlength)+'_label0_rnd_'+str(rndst)+'.json'
            print(json_name)
            with open(json_name,'w') as json_file:
                json.dump(label0ruledict,json_file)

if __name__ =='__main__':
    way3()
    playsound('../Yattong+edited+version.mp3')