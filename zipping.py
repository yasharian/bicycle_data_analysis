import zlib
import zipfile
import asyncio 
from cyclists import main , DF , GROUPED
asyncio.run(main())
DF.to_csv('bikes.csv', index=True , header=True )
GROUPED.to_csv("cnt_mean_grouped.csv", index=False)

def compress(file_names):
    print("File Paths:")
    print(file_names)
    compression = zipfile.ZIP_DEFLATED
    with zipfile.ZipFile("result2.zip", mode="w") as zf:
        for file_name in file_names:
            zf.write('./' + file_name, file_name, compress_type=compression)

file_names = ["plot2.jpg" , "plot1.jpg" , "cyclists.py", "bikes.csv", "cnt_mean_grouped.csv"]
compress(file_names)