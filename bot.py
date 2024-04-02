
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup 
from telegram.ext import ApplicationBuilder, filters, CallbackQueryHandler, CommandHandler, CallbackContext, MessageHandler
import csv
import random

TOKEN = open('Token.txt', 'r', encoding='utf-8').read().strip()

async def start(update: Update, context: CallbackContext) -> None:
    keyboard = [[InlineKeyboardButton('Начать обучение', callback_data='start')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Нажмите на кнопку ниже чтобы начать', reply_markup=reply_markup)
    
    
async def sentence(update: Update, context: CallbackContext) -> None:
    with open('Data/database.txt', 'r', encoding='utf-8') as infile:
        reader = csv.reader(infile, delimiter='"')
        new_sentence = random.choice([tuple(row) for row in reader])
    context.user_data['correct_word'] = new_sentence[1]
    await update.callback_query.message.reply_text(new_sentence[0])


async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    if query.data == 'start':
        await sentence(update, context)
        return
    if query.data == 'continue':
        await sentence(update, context)
        return
    if query.data == 'show_answer':
        await query.edit_message_text(f'Правильный ответ: →  *{context.user_data["correct_word"]}*', parse_mode='Markdown')
        keyboard = [[InlineKeyboardButton('Новое предложение', callback_data='continue')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text('Давайте продолжим', reply_markup=reply_markup)
        return
    if query.data == 'give_rule':
        photo_dict = {
            'patīk': 'Data/patikt.jpeg',
            'dzīvoju': 'Data/dzīvoju.jpg',
            'braucam': 'Data/braucam.jpg',
            'brauks': 'Data/braucam.jpg',
            'strādā': 'Data/strādāt.jpg',
            'remontē': 'Data/remontēt.jpg',
            'krāso': 'Data/krāsot.jpg',
            'ir': 'Data/ir.jpg',
            'dejo': 'Data/dejot.jpg',
            'slidoju': 'Data/slidot.jpg'
        }

        if context.user_data['correct_word'] in photo_dict:
            with open(photo_dict[context.user_data['correct_word']], 'rb') as photo:
                await context.bot.send_photo(chat_id=query.message.chat_id, photo=photo)
        else:
            with open('Data/rules.jpeg', 'rb') as photo:
                await context.bot.send_photo(chat_id=query.message.chat_id, photo=photo)
        keyboard = [
            [InlineKeyboardButton('Показать правильный ответ', callback_data='show_answer')],
            [InlineKeyboardButton('Попробовать еще раз', callback_data='try_again')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text('Попробуем еще раз или сдаемся?. Выберите действие:', reply_markup=reply_markup)
        return
        
    if query.data == 'try_again':
        await query.edit_message_text('Попробуйте еще раз.')
        return


async def check_answer(update: Update, context: CallbackContext) -> None:
    if update.message.text.lower() == context.user_data['correct_word']:
        keyboard = [[InlineKeyboardButton('Продолжить', callback_data='continue')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text('Ваш ответ правильный! Нажмите Продолжить', reply_markup=reply_markup)
        return

    keyboard = [
        [InlineKeyboardButton('Показать правильный ответ', callback_data='show_answer')],
        [InlineKeyboardButton('Дать правило', callback_data='give_rule')],
        [InlineKeyboardButton('Попробовать еще раз', callback_data='try_again')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Ваш ответ неправильный. Выберите действие:', reply_markup=reply_markup)
    return


def main():
    app = ApplicationBuilder().token(TOKEN).build()

  
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT, check_answer))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(CommandHandler("sentence", sentence))
    
    

    app.run_polling(allowed_updates=Update.ALL_TYPES)



if __name__ == '__main__':
    main()