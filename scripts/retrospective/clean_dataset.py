from covidmonte.clean_retrospective import *

if __name__ == "__main__":
    
    # df = pd.read_csv("data/raw/COVID19_RETROSPECTIVE_5.15.csv")
    df = pd.read_excel('data/raw/COVID19_RETROSPECTIVE_DATA.5.15.xlsx')
    df = clean_data(df)
    df.to_csv("data/confidential/retrospective.csv")