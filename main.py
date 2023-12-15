import telebot
import random
import sqlite3
import datetime

bot = telebot.TeleBot('6253967421:AAFrb_qqaWLJ_AK-zVUpNDHjcKcQMgH5xWM')


@bot.message_handler(commands=['help', 'start'])
def help(message):
  bot.send_message(
      message.chat.id,
      f'<i> Добро пожаловать на посиделки у мангала!\n\nИспользуй <b>/shashlik</b>, чтобы перекусить.\n\nПодпишись на <b><a href="https://t.me/+exwZtIpxjZtmYmZi">Канал</a></b> (Пожалуйста🥹), чтобы быть в курсе новостей проекта!</i>',
      parse_mode='html', disable_web_page_preview=True)

@bot.message_handler(commands=['topall'])
def topall(message):
  db = sqlite3.connect('shashlik.db')
  sql = db.cursor()
  user_id = message.from_user.id
  sql.execute('SELECT shashlik FROM shashlik ORDER BY shashlik + 0 DESC')
  res = sql.fetchall()
  bot.send_message(message.chat.id, f'1. 🔥 {res[0][0]} - {res} кг.\n2. 🔥 ', parse_mode='html')


@bot.message_handler(commands=['shashlik'])
def lalala(message):
  db = sqlite3.connect('shashlik.db')
  sql = db.cursor()
  user_id = message.from_user.id
  shashlik = random.uniform(1.5, 4.5)
  c = round(shashlik, 1)
  i = datetime.datetime.now().strftime("%Y:%m:%d:%H:%M:%S")
  username = message.from_user.username

  sql.execute("""CREATE TABLE IF NOT EXISTS shashlik (user_id INT, first_name TEXT, shashlik STRING, real_time TEXT)""")
  db.commit()
  sql.execute("SELECT shashlik, real_time FROM shashlik WHERE user_id=?", (user_id, ))
  result = sql.fetchone()

  if result is not None:
    existing_shashlik = float(result[0])
    last_shashlik_time_str = result[1]
    last_shashlik_time1 = datetime.datetime.strptime(last_shashlik_time_str, '%Y:%m:%d:%H:%M:%S')
    last_shashlik_time2 = datetime.datetime.strftime(last_shashlik_time1, '%H:%M:%S')
    last_shashlik_time = datetime.datetime.strptime(last_shashlik_time2, '%H:%M:%S')
    hhh = datetime.datetime.now().strftime('%Y:%m:%d:%H:%M:%S')

    if last_shashlik_time1 + datetime.timedelta(minutes=30) < datetime.datetime.now().strptime(hhh, '%Y:%m:%d:%H:%M:%S'):
      new_shashlik = existing_shashlik + c
      n = round(new_shashlik, 1)
      m = message.from_user.username
      sql.execute("UPDATE shashlik SET shashlik=?, real_time=? WHERE user_id=?", (n, i, user_id))
      db.commit()
      bot.send_message(
        message.chat.id, f' <a href="t.me/{m}">{message.from_user.first_name} </a>, ты съел(а) {c}кг шашлыка. Съедено всего: {n}кг.', parse_mode='html', disable_web_page_preview=True)
    else:
      current_time = datetime.datetime.now()
      time_remaining = last_shashlik_time - current_time + datetime.timedelta(minutes=30)
      m = message.from_user.username
      sql.execute("SELECT shashlik FROM shashlik WHERE user_id=?", (user_id, ))
      lll = sql.fetchone()[0]
      bot.send_message(message.chat.id, f"<i><b> <a href='t.me/{m}/'>{message.from_user.first_name}</a></b>, повтори через: {time_remaining.seconds // 60} мин. {time_remaining.seconds % 60} сек. Съедено всего: {lll}кг шашлыка.</i>", parse_mode='html', disable_web_page_preview=True)
  else:
    username = message.from_user.username
    m = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    sql.execute("INSERT INTO shashlik VALUES (?, ?, ?)", (user_id, c, i))
    db.commit()
    bot.send_message(message.chat.id, f"<a href='t.me/{m}'>{first_name} </a>, ты съел(а) {c}кг шашлыка. Съедено всего: {c}кг шашлыка.", parse_mode='html', disable_web_page_preview=True)
    
bot.infinity_polling()