import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import datetime

def make_duration_graf(json_data):
    duration_data = list()
    for issue in json_data["issues"]:
        if issue["fields"]["status"]["name"] == "Closed":
            created_time = datetime.datetime.fromisoformat(issue["fields"]["created"])
            closed_time = datetime.datetime.fromisoformat(issue["fields"]["resolutiondate"])
            duration = (closed_time - created_time).total_seconds() / 3600 / 24
            duration_data.append({"id": issue["id"], "duration": duration })

    durations = [issue["duration"] for issue in duration_data]
    plt.hist(durations, bins=10, edgecolor='black')  # Разделить на 10 бинов (интервалов)
    plt.xlabel('Время в открытом состоянии (дни)')
    plt.ylabel('Количество задач')
    plt.title('Гистограмма времени в открытом состоянии')
    plt.show()

def make_summ_graf(json_data):
    task_data = list()
    for issue in json_data["issues"]:
        created_time = datetime.datetime.fromisoformat(issue["fields"]["created"])
        if issue["fields"]["resolutiondate"] != None:
            closed_time = datetime.datetime.fromisoformat(issue["fields"]["resolutiondate"])
        else:
            closed_time = None
        #duration = (closed_time - created_time).total_seconds() / 3600 / 24
        task_data.append({"id": issue["id"], "created": created_time,
                               "closed": closed_time })
        
    df = pd.DataFrame(task_data)
    
    # Добавление столбцов с количеством задач и накопительным итогом
    df['created_tasks'] = 1
    df['closed_tasks'] = df['closed'].apply(lambda x: 1 if x is not None else 0)

    # Группировка данных по дням и расчет накопительного итога
    df['created_date'] = df['created'].dt.date
    df['closed_date'] = df['closed'].dt.date
    daily_data_created = df.groupby('created_date').agg({'created_tasks': 'sum'}).fillna(0)
    daily_data_closed = df.groupby('closed_date').agg({'closed_tasks': 'sum'}).fillna(0)

    daily_data_created['cumulative_created'] = daily_data_created['created_tasks'].cumsum()
    daily_data_closed['cumulative_closed'] = daily_data_closed['closed_tasks'].cumsum()

    # Создание графика
    plt.figure(figsize=(10, 6))
    plt.plot(daily_data_created.index, daily_data_created['created_tasks'], label='Созданные задачи', marker='o')
    plt.plot(daily_data_closed.index, daily_data_closed['closed_tasks'], label='Закрытые задачи', marker='o')
    plt.plot(daily_data_created.index, daily_data_created['cumulative_created'], label='Накопительный итог созданных задач', linestyle='--')
    plt.plot(daily_data_closed.index, daily_data_closed['cumulative_closed'], label='Накопительный итог закрытых задач', linestyle='--')

    plt.xlabel('Дата')
    plt.ylabel('Количество задач')
    plt.title('График созданных и закрытых задач с накопительным итогом')
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)

    plt.show()


def make_top_authors_graf(json_data):
    author_data = list()
    for issue in json_data["issues"]:
        assignee = None
        if issue["fields"]["assignee"] != None:
            assignee = issue["fields"]["assignee"]["displayName"]
        reporter = issue["fields"]["reporter"]["displayName"]
        author_data.append({"id": issue["id"], "assignee": assignee, "reporter": reporter})
    # Преобразование данных в DataFrame
    df = pd.DataFrame(author_data)
    # Объедините столбцы assignee и reporter в столбец user
    df['user'] = df['assignee'].fillna(df['reporter'])

    # Удалите дубликаты пользователей
    df = df.drop_duplicates(subset=['id', 'user'])

    # Посчитайте количество задач для каждого уникального пользователя
    user_counts = df['user'].value_counts()

    # Создайте DataFrame с результатами
    result_df = user_counts.reset_index()
    result_df.columns = ['user', 'count']


    # Выбор 30 топовых пользователей
    top_users = result_df.head(30)

    # Создание графика
    plt.figure(figsize=(10, 8))
    plt.barh(top_users['user'], top_users['count'])
    plt.xlabel('Количество задач')
    plt.ylabel('Пользователь')
    plt.title('Топ 30 пользователей по количеству задач')
    plt.gca().invert_yaxis()  # Инвертировать ось ординат для отображения наибольшего количества сверху
    plt.grid(axis='x', linestyle='--', alpha=0.6)

    plt.show()

def make_duration_graf(json_data):
    duration_data = list()
    for issue in json_data["issues"]:
        if issue["fields"]["status"]["name"] == "Closed":
            created_time = datetime.datetime.fromisoformat(issue["fields"]["created"])
            closed_time = datetime.datetime.fromisoformat(issue["fields"]["resolutiondate"])
            duration = (closed_time - created_time).total_seconds() / 3600 / 24
            duration_data.append({"id": issue["id"], "duration": duration })

    durations = [issue["duration"] for issue in duration_data]
    plt.hist(durations, bins=10, edgecolor='black')  # Разделить на 10 бинов (интервалов)
    plt.xlabel('Время в открытом состоянии (дни)')
    plt.ylabel('Количество задач')
    plt.title('Гистограмма времени в открытом состоянии')
    plt.show()

def make_logged_time(json_data):
    data = list()
    for issue in json_data["issues"]:
        time = int(issue["fields"]["progress"]["total"]) / 60
        data.append({"id": issue["id"], "time": time})

   # Преобразование данных в DataFrame
    df = pd.DataFrame(data)

    # Группировка данных по времени и подсчет количества задач для каждого уникального времени
    time_grouped = df.groupby('time').size().reset_index(name='task_count')

    # Создание гистограммы
    plt.figure(figsize=(10, 6))
    plt.bar(time_grouped['time'], time_grouped['task_count'])
    plt.xlabel('Затраченное время (в минутах)')
    plt.ylabel('Количество задач')
    plt.title('Гистограмма затраченного времени на задачи')
    plt.yticks(range(time_grouped['task_count'].min(), time_grouped['task_count'].max() + 1))  # Установка целых делений на оси y
    plt.grid(True)

    plt.show()

def make_priority_graf(json_data):
    data = list()
    for issue in json_data["issues"]:
        priority = issue["fields"]["priority"]["name"]
        data.append({"id": issue["id"], "priority": priority})
    # Преобразование данных в DataFrame
    df = pd.DataFrame(data)

    # Группировка данных по степени серьезности и подсчет количества задач
    severity_counts = df['priority'].value_counts().reset_index()
    severity_counts.columns = ['priority', 'Task Count']

    # Создание графика
    plt.figure(figsize=(10, 6))
    plt.bar(severity_counts['priority'], severity_counts['Task Count'])
    plt.xlabel('Степень серьезности')
    plt.ylabel('Количество задач')
    plt.title('График количества задач по степени серьезности')
    plt.grid(True)

    plt.show()

url = "https://issues.apache.org/jira/rest/api/2/search?jql=project=AMQ"  # Замените URL на адрес вашего API
response = requests.get(url)

if response.status_code == 200:
    json_data = response.json()  # Распарсить JSON-ответ
    make_duration_graf(json_data)
    make_summ_graf(json_data)
    make_top_authors_graf(json_data)
    make_logged_time(json_data)
    make_priority_graf(json_data)
else:
    print("Не удалось получить JSON. Код состояния:", response.status_code)
