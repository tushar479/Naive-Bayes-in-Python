import os
import pandas as pd
import numpy as np
import re
import sys

TrainSet={}
TestSet={}
def searchKey(Key):
    count=0
    for i,v in TrainSet.iteritems():
        if i == Key:
            count = v
            return count
    return count

#Test the result and predict the outcomes
def TestData(filenameTest,target_attribute):

    # Read the data and store it into a dataframe
    df2 = pd.read_csv(filenameTest, delim_whitespace=True)

    TotalRowsOfDataSet = len(df2.index)
    TargetAttributes = df2.unstack().groupby(level=0).nunique()

    tgtAttr = {}
    headers = {}
    tgtAttrDict = {}
    count = 0
    countHeadr = 0
    tgtfound = 0
    for i, v in TargetAttributes.iteritems():
        tgtAttr[i] = v
        count += 1
        tgtAttrDict[i] = count
        countHeadr += 1
        headers[i] = countHeadr

    for ktgt, valtgt in tgtAttrDict.items():
        if ktgt == target_attribute:
            target_attribute = ktgt
            tgtfound = 1
            break
    if tgtfound == 0:
        print 'Target Attribute is not found in the Test Dataset'
        sys.exit()


    dic = {}
    dic = df2.groupby([target_attribute]).count()
    SumOfTargerAttr = df2.groupby([target_attribute]).count().sum()[0]
    Result=[]
    for key,data in df2.iterrows():
        #print data
        cmpTgtItem = ''
        cmpProb = 0
        finalStr=''
        finalStrAfterCalcProb=''
        for i in df2.groupby([target_attribute]):
            tattrib = str(i[:1]).replace("'", '').replace(")", '').replace("(", '').replace(",", '').strip()
            Probability=1
            countHead = 1
            for items in data:
                c=0
                headerOfTgtAttr = re.sub('[^A-Za-z0-9]+','',str([k for k, h in tgtAttrDict.items() if h == countHead]))
                if  headerOfTgtAttr!= target_attribute:
                    countHead+=1
                    c = Probability *   searchKey(str(items)+'/'+str(tattrib))
                    Probability = c
                    if finalStr =='':
                        finalStr+=str(items)
                    else:
                        finalStr+= ','+str(items)
                else:
                    if finalStr =='':
                        finalStr+=str(items)
                    else:
                        finalStr+= ','+str(items)
                    c = Probability *   searchKey(str(tattrib))
                    Probability = c
            if Probability>cmpProb:
                cmpProb = Probability
                cmpTgtItem = str(tattrib)
                finalStr += ','+str(tattrib)
                finalStrAfterCalcProb = finalStr
                finalStr=''
            else:
                finalStr = ''
        Result.append(finalStrAfterCalcProb)
    return Result

# main function which is called first when the program is executed
def main():

    filename = raw_input("Enter a file name for Train :")
    filename = filename.strip()
    if os.path.exists(filename)==False:
        filename = raw_input("Please Enter correct file name :")
        filename = filename.strip()

    filenameTest = raw_input("Enter a file name for Test :")
    filenameTest = filenameTest.strip()
    if os.path.exists(filenameTest) == False:
        filenameTest = raw_input("Please Enter correct file name for Test :")
        filenameTest = filenameTest.strip()

    tgtAttr = {}
    headers = {}
    tgtAttrDict = {}

    # Read the data and store it into a dataframe
    df2 = pd.read_csv(filename, delim_whitespace=True)

    TotalRowsOfDataSet = len(df2.index)
    TargetAttributes = df2.unstack().groupby(level=0).nunique()

    tgtAttr = {}
    count = 0
    countHeadr = 0
    strheaders=''
    for i, v in TargetAttributes.iteritems():
        tgtAttr[i] = v
        count += 1
        tgtAttrDict[i] = count
        if strheaders=='':
            strheaders=str(i)
        else:
            strheaders+=','+str(i)
        print('{:2}: {:2}'.format(count, i))
        countHeadr += 1
        headers[i] = countHeadr

    TargetInput = raw_input("Please Enter only one Integer value from the above:")
 
    for ktgt, valtgt in tgtAttrDict.items():
        if valtgt == int(TargetInput):
            target_attribute = ktgt
            tgtfound = 1
            break
    if tgtfound == 0:
        TargetInput = raw_input("You have entered an incorrect value. Please Re-Enter one Integer value from the above:")

    #Train the data set and store the probabilities of individual items
    dic = {}
    dic = df2.groupby([target_attribute]).count()
    SumOfTargerAttr = df2.groupby([target_attribute]).count().sum()[0]
    headerOfItem=''
    Result=[]
    for key,data in df2.iterrows():
        #print data
        for i in df2.groupby([target_attribute]):
            tattrib = str(i[:1]).replace("'", '').replace(")", '').replace("(", '').replace(",", '').strip()
            countHead = 1
            for items in data:
                headerOfTgtAttr = re.sub('[^A-Za-z0-9]+','',str([k for k, h in tgtAttrDict.items() if h == countHead]))
                if headerOfTgtAttr != target_attribute:
                    headerOfItem = str([k for k,h in tgtAttrDict.items() if h==countHead])
                    countHead+=1

                    df3 = df2[[re.sub('[^A-Za-z0-9]+','',headerOfItem), target_attribute]]
                    df4 = df3[df3[re.sub('[^A-Za-z0-9]+','',headerOfItem)]==items]
                    if str(tattrib)=='False':
                        df5 = df4[df4[target_attribute]!=bool(tattrib)]
                    elif str(tattrib)=='True':
                        df5 = df4[df4[target_attribute]==bool(tattrib)]
                    elif str(tattrib).isdigit():
                        df5 = df4[df4[target_attribute] == float(tattrib)]
                    else:
                        df5 = df4[df4[target_attribute] == str(tattrib)]
                    if len(df5)>0:
                        sumOfItem = df5.groupby([re.sub('[^A-Za-z0-9]+','',headerOfItem)]).count().sum()[0]
                        if str(tattrib) == 'False':
                            sumOfTgtAttr = df2[df2[target_attribute] != bool(tattrib)].groupby([target_attribute]).count().sum()[0]
                        elif str(tattrib) == 'True':
                            sumOfTgtAttr = df2[df2[target_attribute] == bool(tattrib)].groupby([target_attribute]).count().sum()[0]
                        elif str(tattrib).isdigit():
                            sumOfTgtAttr = \
                            df2[df2[target_attribute] == float(tattrib)].groupby([target_attribute]).count().sum()[0]
                        else:
                            sumOfTgtAttr = df2[df2[target_attribute] == str(tattrib)].groupby([target_attribute]).count().sum()[0]
                        #sumOfTgtAttr = df2[df2[target_attribute] == str(tattrib)].groupby([target_attribute]).count().sum()[0]
                        if searchKey(str(items) + '/' + str(tattrib)) == 0:
                            TrainSet[str(items) + '/' + str(tattrib)] = (float(sumOfItem) / float(sumOfTgtAttr))
                    else:
                        TrainSet[str(items) + '/' + str(tattrib)] = 0
                else:
                    if str(tattrib) == 'False':
                        sumOfTgtAttr = df2[df2[target_attribute] != bool(tattrib)].groupby([target_attribute]).count().sum()[0]
                    elif str(tattrib) == 'True':
                        sumOfTgtAttr = df2[df2[target_attribute] == bool(tattrib)].groupby([target_attribute]).count().sum()[0]
                    elif str(tattrib).isdigit():
                        sumOfTgtAttr = df2[df2[target_attribute] == float(tattrib)].groupby([target_attribute]).count().sum()[0]
                    else:
                        sumOfTgtAttr = df2[df2[target_attribute] == str(tattrib)].groupby([target_attribute]).count().sum()[0]
                    if searchKey(str(tattrib)) == 0:
                        TrainSet[ str(tattrib)] = (float(sumOfTgtAttr) / float(TotalRowsOfDataSet))

    path = '/Users/tushar/Desktop/DAL/DataMining/Ass5/Output.txt'

    # Delete file test2.txt
    if os.path.exists(path):
        os.remove(path)

    f = open(path, 'w+')
    f.write(strheaders+',Classification' + '\n')
    finalResult = TestData(filenameTest, target_attribute)
    CountTotalRows=0
    CountAccuracy=0
    for a in finalResult:
        Train = str(a).split(',')[-1]
        if int(TargetInput)==1:
            Test = str(a).split(',')[0]
        else:
            Test = str(a).split(',')[int(TargetInput)-1]
        if Train==Test:
            CountAccuracy+=1
        CountTotalRows+=1
        f.write(a + '\n')
    f.write('\n')
    f.write('Total Accuracy is: ' +str(CountAccuracy) +'/'+ str(CountTotalRows) +'  (' + str((float(CountAccuracy)/float(CountTotalRows)*100)) + ' % )' + '\n')
    f.close()
    print 'Output is saved to : ' + path
# this will call the main() function first
if __name__ == '__main__':
    main()
