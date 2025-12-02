import pandas as pd

def cleaning(fileName): 
    df = pd.read_csv(fileName)
    df = df.replace('away', None)
    df = df.dropna() 
    df.to_csv(fileName[0:-5] + "-CLEANED" + ".csv", index=False, encoding="utf-8")

def main():    
    fileList =  ["petDatacats-for-ado.csv",
                 "petDatacats-adopted.csv",
                 "petDatadogs-for-ado.csv",
                 "petDatadogs-adopted.csv"]

    for file in fileList:
        cleaning(file)
        print(f"finished cleaning {file}")

main()