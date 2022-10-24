import requests
import pandas
import lxml
from bs4 import BeautifulSoup
import pandas as pd
from colorama import init, Fore, Style

def tableize(df):
    if not isinstance(df, pd.DataFrame):
        return
    df_columns = df.columns.tolist()
    max_len_in_lst = lambda lst: len(sorted(lst, reverse=True, key=len)[0])
    align_center = lambda st, sz: "{0}{1}{0}".format(" "*(1+(sz-len(st))//2), st)[:sz] if len(st) < sz else st
    align_right = lambda st, sz: "{0}{1} ".format(" "*(sz-len(st)-1), st) if len(st) < sz else st
    max_col_len = max_len_in_lst(df_columns)
    max_val_len_for_col = dict([(col, max_len_in_lst(df.iloc[:,idx].astype('str'))) for idx, col in enumerate(df_columns)])
    col_sizes = dict([(col, 2 + max(max_val_len_for_col.get(col, 0), max_col_len)) for col in df_columns])
    build_hline = lambda row: '+'.join(['-' * col_sizes[col] for col in row]).join(['+', '+'])
    build_data = lambda row, align: "|".join([align(str(val), col_sizes[df_columns[idx]]) for idx, val in enumerate(row)]).join(['|', '|'])
    hline = build_hline(df_columns)
    out = [hline, build_data(df_columns, align_center), hline]
    for _, row in df.iterrows():
        out.append(build_data(row.tolist(), align_right))
    out.append(hline)
    return "\n".join(out)

data = {
        'Команда': [], 'ФИ игрока': [], 'Роль': [],
        'Голы': [], 'Пенальти': [], 'Пасы': [],
        'Матчи': [],'Штрафные': [], 'Fair play': [],
        'Желтые карточки': [], '2ЖК': [],'Красные карточки': []
        }

response = requests.get(url= 'https://soccer365.ru/competitions/13/')
scr1 = response.text
soup1 = BeautifulSoup(scr1,'lxml')
table1 = soup1.find('table', class_='stngs')
pickachu = 0
table_tr = table1.find_all('tr',class_='')
for pika in table_tr:
      pickachu += 1

with open(f'index.html','w',encoding='utf-8') as file:
    scr = file.write(response.text)

with open(f'index.html',encoding='utf-8') as file:
    ss = file.read()
    soup = BeautifulSoup(ss,'lxml')
    fio = []
    teams = []
    role = []
    goals = []
    pengoal = []
    mathes = []
    passing = []
    fine = []
    fire = []
    yellow_cards = []
    two_yc = []
    red_card = []
    biba = soup.find_all('table',class_ = 'comp_table_v2')
    for tables in biba:
        for el in tables.find_all('div',class_='img16'):
             fio.append(el.text)
        for el in tables.find_all('img',class_='has-tip'):
             teams.append(el.get('title'))
        for el in tables.find_all('div',class_='img16'):
             role.append(tables.find('th',class_='title').text.strip())
        role_in_table = tables.find('th', class_='title').text
        role_in_tr = "Бомбардиры"
        role_in_tr1 = "Ассистенты"
        role_in_tr2 = "Штрафники"
        for ep in tables.find_all('tr',class_=''):
            if role_in_table.strip() == role_in_tr:
                proba = []
                for em in ep.find_all('td',class_='bkcenter'):
                    proba.append(em.text)
                goals.append(proba[0])
                mathes.append(proba[2])
                if proba[1].strip() == '':
                    pengoal.append('0')
                else:
                    pengoal.append(proba[1])
            else:
                goals.append("0")
                pengoal.append("0")
            if role_in_table.strip() == role_in_tr1:
                proba1 = []
                for em in ep.find_all('td', class_='bkcenter'):
                    proba1.append(em.text)
                mathes.append(proba1[1])
                name = ep.find('span').text
                passing.append(proba1[0])
            else:
                passing.append('0')
            if role_in_table.strip() == role_in_tr2:
                proba2 = []
                for em in ep.find_all('td', class_='bkcenter'):
                    proba2.append(em.text)
                fine.append('0')
                fire.append(proba2[0])
                yellow_cards.append(proba2[1])
                if proba2[2].strip() == '':
                    two_yc.append('0')
                else:
                    two_yc.append(proba2[2])
                if proba2[3].strip() == '':
                    red_card.append('0')
                else:
                    red_card.append(proba2[3])
                mathes.append(proba2[4])
            else:
                fine.append('0')
                fire.append('0')
                yellow_cards.append('0')
                two_yc.append('0')
                red_card.append('0')
    for tables in biba:
        role_in_table = tables.find('th', class_='title').text
        role_in_tr1 = "Ассистенты"
        role_in_tr2 = "Штрафники"
        for ep in tables.find_all('tr', class_=''):
            if role_in_table.strip() == role_in_tr1:
                proba1 = []
                for em in ep.find_all('td', class_='bkcenter'):
                    proba1.append(em.text)
                name = ep.find('span').text
                index = fio.index(name)
                passing[index] = proba1[0]
            if role_in_table.strip() == role_in_tr2:
                proba2 = []
                for em in ep.find_all('td', class_='bkcenter'):
                    proba2.append(em.text)
                name = ep.find('span').text
                index = fio.index(name)
                fire[index] = proba2[0]
                yellow_cards[index] = proba2[1]
                fine[index] = "1"
                if proba2[2].strip() == '':
                    two_yc[index] = '0'
                else:
                    two_yc[index] = proba2[2]
                if proba2[3].strip() == '':
                    red_card[index] = '0'
                else:
                    red_card[index] = proba2[3]
    pd.options.display.expand_frame_repr = False
    dframe = pd.DataFrame(data)
    dframe['ФИ игрока'] = fio
    dframe['Команда'] = teams
    dframe['Роль'] = role
    dframe['Голы'] = goals
    dframe['Пенальти'] = pengoal
    dframe['Матчи'] = mathes
    dframe['Пасы'] = passing
    dframe['Штрафные'] = fine
    dframe['Fair play'] = fire
    dframe['Желтые карточки'] = yellow_cards
    dframe['2ЖК'] = two_yc
    dframe['Красные карточки'] = red_card
    df = dframe.drop_duplicates(subset=['ФИ игрока'])
    print( Fore.GREEN + "DATAFRAME" + Style.RESET_ALL)
    print(tableize(df))
    # #Task1
    df_sum = df.groupby(["Команда","Голы"]).sum("Голы").reset_index()
    df_sum_result = df_sum.groupby(["Команда"], as_index=False).agg(lambda x: pd.to_numeric(x, errors='coerce').sum())
    print( Fore.GREEN + "Задание №1. \nПервая тройка команд по числу забитых голов с выводом их числа." + Style.RESET_ALL)
    print(tableize(df_sum_result.sort_values(by='Голы', ascending=False).head(3)))
    #Task2
    print(Fore.GREEN + "Задание №2. \nПервая тройка команд по числу желтых карточек." + Style.RESET_ALL)
    df_sum = df.groupby(["Команда", "Желтые карточки"]).sum("Желтые карточки").reset_index()
    df_sum_result = df_sum.groupby(["Команда"], as_index=False).agg(lambda x: pd.to_numeric(x, errors='coerce').sum())
    print(tableize(df_sum_result.sort_values(by='Желтые карточки', ascending=False).head(3)))
    #Task3
    print(Fore.GREEN + "Задание №3. \nСписок игроков, которые участвовали не во всех играх своей команды. Число игр\
    команды определить по максимальному числу матчей ее игроков." + Style.RESET_ALL)
    arr = df.values.tolist()
    counter_dict = {}
    walkers = []
    teams = []
    mathes = []
    for item in arr:
        if item[0] in counter_dict:
            if int(item[6]) > counter_dict[item[0]]:
                counter_dict[item[0]] = int(item[6])
        else:
            counter_dict[item[0]] = int(item[6])

        if int(item[6]) < counter_dict[item[0]]:
            walkers.append(item)
    print( Fore.GREEN + 'Количество матчей команд' + Style.RESET_ALL)
    print(tableize(pd.DataFrame(list(counter_dict.items()),
                       columns=['Команда', 'Матчи'])))
    print(Fore.GREEN + 'Список игроков, которые играли не во всех матчах команды' + Style.RESET_ALL)
    dataframe = pd.DataFrame(columns=['Игрок','Матчи'])
    player = []
    mathes = []
    for fio in walkers:
        player.append(fio[1])
        mathes.append(fio[6])
    dataframe['Игрок'] = player
    dataframe['Матчи'] = mathes
    print(tableize(dataframe))
    print(Fore.GREEN + 'Задание №4. \nДоля пенальти по отношению к числу голов для каждой команды.' + Style.RESET_ALL)
    counter_goals = {}
    penalty_counter = {}
    for item in arr:
        if item[0] in counter_goals:
            counter_goals[item[0]] += int(item[3])
        else:
            counter_goals[item[0]] = int(item[3])
        if item[0] in penalty_counter:
            penalty_counter[item[0]] += int(item[4])
        else:
            penalty_counter[item[0]] = int(item[4])
    dataframe = pd.DataFrame(columns=['Команда','Голы','Пенальти','Отношение'])
    goals = []
    pengoal = []
    otnosh = []
    teams = []
    for key in counter_goals:
        teams.append(key)
        goals.append(counter_goals[key])
        pengoal.append(penalty_counter[key])
        try:
            otnosh.append(penalty_counter[key] / counter_goals[key])
        except:
            otnosh.append("0")
    dataframe['Команда'] = teams
    dataframe['Голы'] = goals
    dataframe['Пенальти'] = pengoal
    dataframe['Отношение'] = otnosh
    print(tableize(dataframe))
    print(Fore.GREEN + 'Задание №5. \nКорреляция числа голов с количеством очков команды.' + Style.RESET_ALL)
    corr_Arr = []
    corr_goals = {}
    corr_points = {}
    for item in arr:
        if item[0] in corr_goals:
            corr_goals[item[0]] += int(item[3])
        else:
            corr_goals[item[0]] = int(item[3])
    for index in range(1,pickachu):
        teamName = table_tr[index].find('a', attrs={"rel": "nofollow"}).text
        points = table_tr[index].find_all('td', class_='ctr')[7].text
        corr_points[teamName] = int(points.strip())

    for key in corr_points:
        try:
            corr_Arr.append((corr_points[key], corr_goals[key]))
        except:
            continue
    df = pd.DataFrame(corr_Arr, columns=['очки', 'голы'])
    print(df.corr())
# Измененния с ноутбука
print('bla bla bla ')

