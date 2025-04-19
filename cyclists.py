import asyncio
import pandas as pd
from matplotlib import pyplot as plt 
from time import sleep , time
import zipping


DF: pd.DataFrame = None
GROUPED : pd.DataFrame = None
def fill_na_with_mean(col): 
    global DF 
    mean = DF[col].mean()
    DF[col].fillna(mean.astype('int64'), inplace=True)

def rm_col_cons_percentage(per): 
    global DF 
    columns = DF.columns[DF.isna().mean() > per]
    DF.drop(columns=columns, inplace=True)

async def Reading():
    global DF , GROUPED 
    DF = pd.read_csv('./bikes_borrowed.csv')  # Load DF first (synchronous)
    
    # Run synchronous functions in threads (concurrently)
    await asyncio.gather(
        asyncio.to_thread(fill_na_with_mean, "humidity"),
        asyncio.to_thread(rm_col_cons_percentage, 0.9),
    )
    #جالب اینه که خود پانداز میگه inplace هیوقت کار نمیکنه در ورژن های اتی و پیشنهاد میده که به صورت معمول این کار رو بکنیم 
    #چرا که مدل مدل های پانداز از نوع کپی کردن است 
    #df[col] = df[col].method(value)  ### is correct 
    #WOW
    # Continue with other sync operations
    DF.dropna(inplace=True)
    DF.rename(columns={"t1": "t_real", "t2": "t_feels_like"}, inplace=True)
    GROUPED =  DF.groupby("t_feels_like", as_index= False )['cnt'].mean()

async def main():
    await Reading()
    print(DF.describe())

if __name__ == "__main__":
    first = time()
    asyncio.run(main())
    print(time() - first )
    DF.describe()
    plt.figure(1) 
    plt.scatter(x=DF["t_real"], y=DF["t_feels_like"] ) # TODO
    plt.savefig('plot1.jpg' , dpi = 300 ,  bbox_inches="tight")
    plt.figure(2)
    plt.scatter(x = GROUPED['t_feels_like'] , y = GROUPED['cnt'] )
    plt.savefig('plot2.jpg' , dpi = 300 ,  bbox_inches="tight")
    zipping() 