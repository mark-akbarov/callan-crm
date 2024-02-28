import json
import enum

from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from telebot import TeleBot, types, custom_filters

from core.settings import TELEGRAM_TOKEN
from course.models import Group, ExamGrade, Course, Category
from course.serializers.group import GroupSerializer, GroupNameSerializer
from account.models.account import User, Enrollment

from bot.keyboards import (
    CustomKeyboard,

)


user_info = {}


class GetGroupInfoState(enum.Enum):
    GROUP_NAME = 'group name'


class GetCourseResultsState(enum.Enum):
    COURSE_NAME = 'course name'


class KnowledgeLevel(enum.Enum):
    BEGINNER = 'beginner'
    ELEMENTARY = 'elementary'
    INTERMEDIATE = 'intermediate'
    UPPER_INTERMEDIATE = 'upper intermediate'
    

class RegistrationState(enum.Enum):
    CATEGORY = 'category'
    COURSE = 'course'
    KNOWLEDGE_LEVEL = 'knowledge level'
    FIRST_NAME = 'first name'
    LAST_NAME = 'last name'
    PHONE_NUMBER = 'phone number'
    FINISH = 'finish registration'
    # PARENT_NAME = 'parent name'
    # PARENT_PHONE_NUMBER = 'phone phone number'

    
def get_state(message):
    return bot.get_state(message.from_user.id, message.chat.id)


def remove_inline_keyboard(call):
    message_id = call.message.message_id
    chat_id = call.message.chat.id
    bot.edit_message_reply_markup(chat_id=chat_id, message_id=message_id, reply_markup=None)



bot = TeleBot(TELEGRAM_TOKEN)
bot.add_custom_filter(custom_filters.StateFilter(bot))


def handle_start_command(message):
    pass


def handle_group_results(message):
    pass


def handle_courses(message):
    pass


def handle_register_course(message):
    pass


def handle_help(message):
    pass


def handle_cancel(message):
    pass


@csrf_exempt
def webhook(request):
    try:
        data = json.loads(request.body)
        update = types.Update.de_json(data)
        bot.process_new_updates([update])
        return HttpResponse()
    except Exception as errors:
        print(f"Errors at : {errors}")


@bot.message_handler(commands=['help'])
def handle_help(message):
    bot.reply_to(
        message,
"""
Ushbu bot CALLAN filiallari haqida ma'lumot olishga yordam beradi
va talabalar o'zlarining kurs baholarini/natijalarini ko'rishlari mumkin.

Buyruqlar ro'yxati:

/start - botni ishga tushirish
/results - test natijalarini ko'rish
/courses - CALLAN o'quv markazidagi kurslar haqida ma'lumot
/register - mavjud kurslarga yozilish
/help - barcha buyruqlarni ko'rish
/cancel - buyruqni bekor qilish
""",
    reply_markup=types.ReplyKeyboardRemove()
    )


@bot.message_handler(commands=['cancel'])
def handle_cancel(message):
    bot.delete_state(message.from_user.id, message.chat.id)
    bot.reply_to(
        message,
        f"Buyruq bekor qilindi. Barcha buyruqlarni ko'rish uchun /help tugmasini bosing",
        reply_markup=types.ReplyKeyboardRemove()
    )


@bot.message_handler(commands=['start'])
def handle_start_command(message):
    bot.send_location(
        message.chat.id,
        latitude=40.53436921352104,
        longitude=70.94687947342611,
        heading="Hello",
    )
    bot.reply_to(
        message, 
f"""
CALLAN Education Botiga xush kelibsiz!
Botning barcha funksiyalarini ko'rish uchun /help tugmasini bosing.
"""
    )    


@bot.message_handler(commands=['results'])
def handle_group_results(message):
    groups = Group.objects.all()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    course_markup = CustomKeyboard(
        [group.name for group in groups], 
        one_time_keyboard=True
        )
    try:
        bot.set_state(
            message.from_user.id,
            GetCourseResultsState.COURSE_NAME.value
        )
        bot.reply_to(
            message,
            'Guruh nomini tanlang.',
            reply_markup=markup.add(*course_markup.create()),
        )
    except Exception as e:
        print(f"Error at: {e}")


@bot.message_handler(state=GetCourseResultsState.COURSE_NAME.value)
def handle_group_results(message):
    group = get_object_or_404(Group, name=message.text)
    results = ExamGrade.objects.filter(group=group).last() # retrieve last test results
    try:
        bot.send_photo(
            message.chat.id,
            results.grades_photo,
            reply_to_message_id=message.id
        )
    except Exception as e:
        print(f"Error at: {e}")


@bot.message_handler(commands=['courses'])
def handle_courses(message):
    courses = Course.objects.all()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    group_markup = CustomKeyboard([course.name for course in courses])
    try:
        bot.reply_to(
            message,
            'Kurs nomini tanlang:',
            reply_markup=markup.add(*group_markup.create()),
        )
        bot.set_state(
            message.from_user.id,
            state=GetGroupInfoState.GROUP_NAME.value
        )
    except Exception as e:
        print(f"Error at: {e}")


@bot.message_handler(state=GetGroupInfoState.GROUP_NAME.value)
def handle_group_info_state(message):
    bot.delete_state(message.from_user.id, message.chat.id)
    try:
        course = get_object_or_404(Course, name=message.text)
        bot.reply_to(
            message,
            course.info,
        )
    except Exception as e:
        print(f"Error at: {e}")


@bot.message_handler(commands=['register'])
def handle_register_category(message):
    categories = Category.objects.all()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    categories_buttons = CustomKeyboard([course.name for course in categories])
    try:
        bot.reply_to(
            message,
            "Kategoriyani tanlang:",
            reply_markup=markup.add(*categories_buttons.create())
        )
        bot.set_state(
            message.from_user.id,
            state=RegistrationState.CATEGORY.value
        )
    except Exception as e:
        print(f"Error at: {e}")


@bot.message_handler(state=RegistrationState.COURSE.value)
def handle_register_course(message):
    category_name = message.text
    courses = Course.objects.filter(category__name=category_name)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    courses_buttons = CustomKeyboard([course.name for course in courses])
    try:
        bot.reply_to(
            message,
            "Qaysi kursga ro'yxatga o'tmoqchisiz?",
            reply_markup=markup.add(*courses_buttons.create())
        )
        bot.set_state(
            message.from_user.id,
            state=RegistrationState.COURSE.value
        )
    except Exception as e:
        print(f"Error at: {e}")


@bot.message_handler(state=RegistrationState.COURSE.value)
def handle_first_name(message):
    user_info['COURSE'] = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    levels_buttons = CustomKeyboard([name.name for name in KnowledgeLevel])
    bot.reply_to(
        message,
        "Fan yoki kurs bo'yicha bilim darajangizni belgilang: ",
        reply_markup=markup.add(*levels_buttons.create())
    )
    bot.set_state(
        message.from_user.id,
        state=RegistrationState.KNOWLEDGE_LEVEL.value
    )


@bot.message_handler(state=RegistrationState.KNOWLEDGE_LEVEL.value)
def handle_knowledge_level(message):
    bot.delete_state(message.from_user.id, message.chat.id)
    user_info['KNOWLEDGE_LEVEL'] = message.text
    existing_user = User.objects.filter(
        telegram_username=message.from_user.username, 
        telegram_user_id=message.from_user.id
        ).exists()
    
    if existing_user:
        try:
            course = Course.objects.get(name=user_info['COURSE'])
            user = User.objects.get(
                telegram_username=message.from_user.username,
                telegram_user_id=message.from_user.id
                )
            Enrollment.objects.create(
                user=user,
                course=course,
                knowledge_level=user_info['KNOWLEDGE_LEVEL']
            )
            bot.reply_to(
            message,
            "Siz ro'yxatdan muvaffaqiyatli o'tdingiz!\
                \nSiz bilan 1-2 kun ichida administratorlarimiz aloqaga chiqishadi."
        )
        except Exception as e:
            print(f"Error when creating Enrollment: {e}")
    else:
        bot.reply_to(message, "Ismingizni kiriting:",)
        bot.set_state(
            message.from_user.id,
            state=RegistrationState.FIRST_NAME.value
            )


@bot.message_handler(state=RegistrationState.FIRST_NAME.value)
def handle_last_name(message):
    user_info['FIRST_NAME'] = message.text
    bot.reply_to(message, 'Familyangizni kiriting:')
    bot.set_state(
        message.from_user.id,
        state=RegistrationState.LAST_NAME.value
    )


@bot.message_handler(state=RegistrationState.LAST_NAME.value)
def handle_phone_number(message):
    user_info['LAST_NAME'] = message.text
    bot.set_state(
        message.from_user.id,
        state=RegistrationState.PHONE_NUMBER.value
    )
    bot.reply_to(
        message,
        'Telefon raqamingizni kiriting (998901234567)',
    )


@bot.message_handler(state=RegistrationState.PHONE_NUMBER.value)
def handle_parent_phone_number(message):
    user_info['PHONE_NUMBER'] = message.text
    try:
        course = get_object_or_404(Course, name=user_info['COURSE'])
        user, _ = User.objects.get_or_create(
            first_name=user_info['FIRST_NAME'],
            last_name=user_info['LAST_NAME'],
            phone_number=user_info['PHONE_NUMBER'],
            parent_name=user_info['PARENT_NAME'],
            parent_phone_number=user_info['PARENT_PHONE_NUMBER'],
            telegram_username=message.from_user.username,
            telegram_user_id=message.from_user.id
        )
        
        Enrollment.objects.create(
            user=user,
            course=course,
            knowledge_level=user_info['KNOWLEDGE_LEVEL']
        )
        bot.reply_to(
        message,
        "Siz ro'yxatdan muvaffaqiyatli o'tdingiz!\
            \nSiz bilan 1-2 kun ichida administratorlarimiz aloqaga chiqishadi."
    )
    except Exception as e:
        print(f"Error when creating object: {e}")
