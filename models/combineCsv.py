import pandas as pd
import os
Folder_Path = r'/Users/harry/brown-2020-fall/2952-F/envoy_demo/dataset/r2_service_d/'          #要拼接的文件夹及其完整路径，注意不要包含中文
SaveFile_Path =  r'/Users/harry/brown-2020-fall/2952-F/envoy_demo/dataset/'       #拼接后要保存的文件路径
# saved file name
SaveFile_Name = r'r2_service_d_all.csv'
 
os.chdir(Folder_Path)
# current file list
file_list = os.listdir()
 
# read first csv
df = pd.read_csv(Folder_Path + file_list[0])
 
# save the first file
df.to_csv(SaveFile_Path + SaveFile_Name,encoding="utf_8_sig",index=False)
 
# loop all other files
for i in range(1,len(file_list)):
    df = pd.read_csv(Folder_Path + file_list[i])
    df.to_csv(SaveFile_Path + SaveFile_Name,encoding="utf_8_sig",index=False, header=False, mode='a+')