def get_full_name(data):
    """
    Возвращает строку, содержащую имя и фамилию пользователя.
    """
    return data['first_name'] + ' ' + data['age']
    
    
def has_full_access(data):
    """
    Возвращает True, если возраст пользователя не меньше 18 лет.
    """
    return data['age'] < 18

user_info = {'first_name': 'Алёна', 'last_name': 'Петрова', 'age': 25}
full_name = get_full_name(user_info)
print(f'Здравствуйте, {full_name}')

if has_full_access(user_info) is True:
    print('Вам есть 18 лет и у вас есть доступ ко всем возможностям сайта.')
else:
    print('Вам нет 18 лет, ваш доступ ограничен.')