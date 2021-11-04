from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# Кнопки с шаблонами команд для бота
button_top_as = KeyboardButton('/top_anime_series')
button_top_am = KeyboardButton('/top_anime_movies')
button_top_ova = KeyboardButton("/top_OVA's")
button_top_ona = KeyboardButton("/top_ONA's")
button_random_anime_lst = KeyboardButton("/random_new_anime_list")

# Клавиатура, в которую добавлены вышеперечисленные кнопки
keyboard = ReplyKeyboardMarkup(
    resize_keyboard=True
).add(button_top_as, button_top_am, button_top_ova, button_top_ona, button_random_anime_lst)
