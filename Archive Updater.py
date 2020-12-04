import os
from channel_id_dict import channel_id_name_dictionary as cinm
import re
throwaway_doc = open('throaway.csv','w').close()
throwaway_doc_2 = open('throwaway.txt', 'w').close()
os.system('start /wait cmd /c "cd \"C:\\Users\\Owner\\Documents\\Archive Programs\\Archive - Copy\"" & del /s /q /f *.csv & del /s /q /f *.txt')
os.system('start /wait cmd /c "cd \"C:\\Users\\Owner\\Documents\\Archive Programs\\DiscordChatExporter-master\\DiscordChatExporter.CLI\" & DiscordChatExporter.Cli.exe & DiscordChatExporter.Cli.exe exportguild -t \"NzU0NzgxNjY1NDk4MjM0OTEw.X15vNA.EKFJlOZBi2NtPVr5V6DjjqqsmqA\" -b -g 536352124695740427 -f Csv -o \"C:\\Users\\Owner\\Documents\\Archive Programs\\Archive - Copy\"')
path = 'Archive - Copy'
files = []
file_type='csv'
for r, d, f in os.walk(path):
    for file in f:
        if file_type in file:
            files.append(os.path.join(r, file)) #Scan for files

dictionary_list=list(cinm.keys())
directory_id=[]
print(dictionary_list)
print("=============")
directory_list = []
for file in files:
    string = re.sub("[^0-9]", "", file)
    print(string)
    if int(string) in dictionary_list:
        directory_list.append(file)
        directory_id.append(string)
    else:
        os.remove(file)
# print(directory_list)
# print(directory_id)
file_number=-1

for file in directory_list:
    file_number+=1
    file_directory_new_string = "C:\\Users\\Owner\\Documents\\Archive Programs\\Archive - Copy\\" + cinm[int(directory_id[file_number])]
#     print(file_directory_new_string)
    file_direct_new = file.replace("Archive - Copy", file_directory_new_string)
#     print(file_direct_new)
    os.rename(file, file_direct_new)