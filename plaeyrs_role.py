import pandas as pd
import glob
import operator

path = r'/home/gleb/Desktop/player position/Player stats' 
all_files = glob.glob(path + "/*.xlsx")
li = []
#Определение основной роли и проставление ее по пустым и множественным полям
for filename in all_files:
    #ebal_rot_excelya = open(filename, 'rb')
    df = pd.read_excel(filename, index_col=None, header=0)
    df = df[['Match', 'Date', 'Position']]
    df['player'] = filename.split('/')[-1].replace('.xlsx', '').replace('Player stats ', '')
    
    counter_pos = {}
    for i, r in df.iterrows():
        if type(df['Position'][i]) == list:
            for pos in df['Position'][i]:
                if pos not in counter_pos:
                    counter_pos[pos] = 1
                else:
                    counter_pos[pos] += 1
        else:
            if df['Position'][i] not in counter_pos:
                counter_pos[df['Position'][i]] = 1
            else:
                counter_pos[df['Position'][i]] += 1
    try:
        max_pos = max(counter_pos.items(), key=operator.itemgetter(1))[0]
    except:
        max_pos = 'No data'
    
    for index, row in df.iterrows():
        if df['Position'][index] == 0 or ',' in df['Position'][index]:
            df['Position'][index] = max_pos
            
    li.append(df)
frame = pd.concat(li, axis=0, ignore_index=True)
frame.to_csv('/home/gleb/Desktop/result/payers_roles_per_mathces.csv', index=False)  
