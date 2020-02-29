#Матчить игроков и подтягивать match_id, а не match_name.

import pandas as pd
import json
import glob
from sqlalchemy import create_engine, select, MetaData, Table, and_

#Обработка имен под формат BD
def matchName_pattern(string:str):
    import re
    penalty = ''
    additional = ''
    str_start = string.find('[')
    str_end = string.find(']')
    new_string = string[str_start + 1:str_end]

    score = re.search(r'\d\-\d', new_string)
    

    if '(P)' in new_string or '(E)' in new_string:
        penalty = re.search('\(P\)', new_string)
        additional = re.search('\(E\)', new_string)
        
        name1 = new_string[:new_string.find(score[0]) - 1]

        if '(P)' in name1:
            name1 = name1[:-4]
            name2 = new_string[new_string.find(score[0]) + 4:]
            new_game_name = name1 + ' - ' + name2 + ' '+ penalty[0] + ' ' + score[0].replace('-', ':')
        else:
            name2 = new_string[new_string.find(score[0]) + 4:]
            name2 = name2[4:]
            new_game_name = name1 + ' - ' + name2 + ' ' + score[0].replace('-', ':') + ' '
            if penalty:
                new_game_name += penalty[0]
            else:
                new_game_name += additional[0]

    else:
        name1 = new_string[:new_string.find(score[0]) - 1]
        name2 = new_string[new_string.find(score[0]) + 4:]
        new_game_name = name1 + ' - ' + name2 + ' ' + score[0].replace('-', ':')
    if penalty != '':
        return name1, name2, score[0].replace('-', ':'), penalty[0]
    elif additional != '':
        return name1, name2, score[0].replace('-', ':'), additional[0]
    else:
        return name1, name2, score[0].replace('-', ':')
    
#Конект к БД и возврат таблицы из БД
def connect_bd(table_name:str, column_name, value):
    engine = create_engine('postgresql+pg8000://bayes:bayes@194.87.238.175:5432/bayes_scout')
    metadata = MetaData(bind=None)
    table = Table(table_name, metadata, autoload = True, autoload_with = engine)
    if column_name == 'match_name':
        select_info = select([table]).where(and_(table.columns.match_name.contains(value[0]), \
                                           table.columns.match_name.contains(value[1]), \
                                           table.columns.match_name.contains(value[2])))
    elif column_name == 'player_name':
        select_info = select([table]).where(table.columns.player_name == value)
    elif column_name == 'role_name':
        select_info = select([table]).where(table.columns.role_name == value)
    else:
        return 'Error'
    connection = engine.connect()
    results = connection.execute(select_info).fetchall()
    return results

# Тест файлов, попарвить обработку файлов - вылетает ошибка TypeError: 'NoneType' object is not subscriptable
# Проблемный Spartak 2. Разные имена в BD и в файлах.
def cursor():
    path = glob.glob(r'/home/gleb/Desktop/data_FNL/*')
    for i in path:
        in_db = []
        in_folders = []
        path_to_passes = i + '/passes/*.csv'
        for j in glob.glob(path_to_passes):
            in_folders.append(matchName_pattern(j))
            match_id = connect_bd('matches', 'match_name', matchName_pattern(j))
            if len(match_id) == 0:
                print(matchName_pattern(j))
                print(j)
                continue
            in_db.append(match_id[0][1])
                
            

#Дописать сбор JSON
def getMatrixByParams():

    #Запрос к БД

    coordinates = pd.read_csv(coordinates, sep = '\t')
    #matrix = pd.read_csv(path_matrix, sep = ','|)

    df_coordinates = pd.DataFrame(coordinates)
    df_matrix = pd.DataFrame(matrix)

    result = {}
    result['result'] = {'nodes': [],
                               "edges": []}
    for i, v in df_matrix.iterrows():
        result['result']['nodes'].append({"player_id": df_matrix['Name1'][i], 
                                                    "player_name": df_matrix['Name1'][i], 
                                                    "group": "string", 
                                                    "role_name": "kek", 
                                                    "x": random.randint(1, 11), 
                                                    "y": random.randint(0, 7), 
                                                    "passes_all": "int", 
                                                    "isFocused": False})
        result['result']['edges'].append({
                                                    "source": df_matrix['Name1'][i], 
                                                    "target": df_matrix['Name2'][i], 
                                                    "passes_to_target": int(df_matrix['Passes_to'][i])})


    jsonify(result['result'])
