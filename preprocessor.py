import re
import pandas as pd


def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2},\s(?:\d{1,2}:\d{2}\s(?:AM|PM)|\d{1,2}:\d{2})'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %I:%M %p', errors='coerce')

    # Drop rows with missing dates
    df = df.dropna(subset=['message_date'])

    df.rename(columns={'message_date': 'date'}, inplace=True)

    df[['user', 'message']] = df['user_message'].str.extract('([\w\W]+?):\s(.*)', expand=True)

    # Fill missing user with 'group_notification'
    df['user'].fillna('group_notification', inplace=True)

    df.drop(columns=['user_message'], inplace=True)

    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    df['period'] = df['date'].dt.strftime('%H-%M')

    return df


f = open(r"C:\Users\kumar_lf3uub3\Downloads\WhatsApp Chat with Stu-dying 🗡️.txt", encoding='utf-8')
data = f.read()
df = preprocess(data)
#print(df)
