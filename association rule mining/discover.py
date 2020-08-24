import json
from playsound import playsound

for prefix in range(2,11):
    for rndst in [0,1,2,3,4]:
        ruledict = {'Label_1':{},'Label_0':{}}
        threshold = 0.9
        label1 = './sepsis/rule1/ruleresult/way3/threshold'+str(threshold)+'/prefix_'+str(prefix)+'_label1_rnd_'+str(rndst)+'.json'
        
        with open(label1,'r') as f:
            label1 = json.load(f)
        
        supportlevelist = sorted(list(label1.keys()),key=len)
        label1rules = []
        
        for x in supportlevelist:
            label1rules +=label1[x]
            ruledict['Label_1'][x] = label1[x]

        label0 = './sepsis/rule1/ruleresult/way3/threshold'+str(threshold)+'/prefix_'+str(prefix)+'_label0_rnd_'+str(rndst)+'.json'
        with open(label0,'r') as f:
            label0 = json.load(f)
        
        supportlevelist = sorted(list(label0.keys()),key=len)
        label0rules = []
        
        for x in supportlevelist:
            label0rules +=label0[x]
            ruledict['Label_0'][x] = label0[x]

        savefilename = './sepsis/rule1/ruleresult/way3/threshold'+str(threshold)+'/Rule_prefix'+str(prefix)+'_rnd'+str(rndst)+'.json'
        with open(savefilename,'w') as f:
            json.dump(ruledict,f)
        f.close()
        

playsound('../Yattong+edited+version.mp3')