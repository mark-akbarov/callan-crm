import json
import enum
import datetime

from django.http.response import HttpResponse
from django.core.files.base import ContentFile
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from telebot import TeleBot, types, custom_filters

from core.settings import TELEGRAM_TOKEN
from core.utils.alfa_crm import create_lead
from course.models import Group, ExamGrade, Course, Category
from account.models.account import User, Enrollment, UserType

from bot.keyboards import (
    CustomKeyboard,

)

exam_grade = {}
user_info = {}


class GetGroupInfoState(enum.Enum):
    GROUP_NAME = 'group name'


class GetCourseResultsState(enum.Enum):
    COURSE_NAME = 'course name'


class KnowledgeLevel(enum.Enum):
    BEGINNER = "Boshlang'ich"
    ELEMENTARY = "O'rta"
    INTERMEDIATE = "Yuqori"
    

class RegistrationState(enum.Enum):
    CATEGORY = 'category'
    COURSE = 'course'
    KNOWLEDGE_LEVEL = 'knowledge level'
    FIRST_NAME = 'first name'
    LAST_NAME = 'last name'
    PHONE_NUMBER = 'phone number'
    FINISH = 'finish registration'


class SumbitResultState(enum.Enum):
    GROUP = 'Group'
    EXAM_NAME = 'Exam Name'
    DATE = 'Date'
    IMAGE = 'Image'
    
    
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
    except json.JSONDecodeError:
        print(f"")


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
/submit - test natijasini kiritish
/courses - CALLAN o'quv markazidagi kurslar haqida ma'lumot
/register - mavjud kurslarga yozilish
/help - barcha buyruqlarni ko'rish
/cancel - buyruqni bekor qilish
""",
    reply_markup=types.ReplyKeyboardRemove()
    )


@bot.message_handler(commands=['cancel'])
def handle_cancel(message):
    print("hello")
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
    try:
        groups = Group.objects.filter(teacher__telegram_user_id=message.from_user.id)
    except Exception as e:
        print(e)
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
    results = ExamGrade.objects.filter(group=group).order_by('-created_at').last() # retrieve last test results
    try:
        bot.send_photo(
            message.chat.id,
            results.grades_photo,
            reply_to_message_id=message.id,
            caption=f"""
Imtihon nomi: {results.name}
Sana: {results.date}
"""
        )
    except Exception as e:
        print(f"Error at: {e}")


@bot.message_handler(commands=['submit'])
def handle_submit_group_results(message):
    telegram_user_id = message.from_user.id
    user = get_object_or_404(User, telegram_user_id=telegram_user_id)
    if user.type not in  [UserType.ADMIN, UserType.TEACHER]: # admin and teacher user type
        bot.reply_to(message, "Sizda yetarli huquqlar yoq! Xatolik yuz bergan bo'lsa bot adminiga murojaat qiling.")
    else:
        groups = Group.objects.filter(teacher=user)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        group_markup = CustomKeyboard([group.name for group in groups])
        try:
            bot.reply_to(
                message,
                'Guruhingiz nomini tanlang:',
                reply_markup=markup.add(*group_markup.create()),
            )
            bot.set_state(
                message.from_user.id,
                state=SumbitResultState.GROUP.value
            )
        except Exception as e:
            print(f"Error at: {e}")


@bot.message_handler(state=SumbitResultState.GROUP.value)
def handle_submit_group_results(message):
    exam_grade['group'] = message.text
    bot.reply_to(
        message,
        "Test yoki imtihon nomini yozing (Unit Test1, Progress Test 1):",
    )
    bot.set_state(
        message.from_user.id,
        state=SumbitResultState.EXAM_NAME.value
    )


@bot.message_handler(state=SumbitResultState.EXAM_NAME.value)
def handle_submit_group_results(message):
    exam_grade['exam_name'] = message.text
    bot.reply_to(
        message,
        "Imtixon sanasini kiriting (KUN/OY/YIL):",
    )
    bot.set_state(
        message.from_user.id,
        state=SumbitResultState.DATE.value
    )


@bot.message_handler(state=SumbitResultState.DATE.value)
def handle_submit_group_results(message):
    print(message.text)
    exam_grade['date'] = message.text
    bot.reply_to(
        message,
        "Test yoki imtihon natijasini yuklang (foto yoki pdf):"
    )
    bot.set_state(
        message.from_user.id,
        state=SumbitResultState.IMAGE.value
    )


@bot.message_handler(content_types=['photo'], state=SumbitResultState.IMAGE.value)
def handle_submit_group_results(message):
    import requests
    
    try:
        day, month, year  = exam_grade['date'].split('/')
        group = Group.objects.get(name=exam_grade['group'])
        exam_grade['photo'] = message.photo[-1].file_id
        file_info = bot.get_file(exam_grade['photo'])
        file_url = f"https://api.telegram.org/file/bot{TELEGRAM_TOKEN}/{file_info.file_path}"
        response = requests.get(file_url)
        
        exam = ExamGrade.objects.create( 
            group=group, 
            name=exam_grade['exam_name'],
            date=datetime.datetime(int(year), int(month), int(day)),       
        )
        exam.grades_photo.save(
            f"{exam_grade['group']}_{exam_grade['exam_name'].replace(' ', '_')}_{exam_grade['date']}", 
            ContentFile(response.content)
            )        

        bot.reply_to(
            message,
            "Natijalar saqlanib olindi! Ko'rish uchun /results tugmasini bosing.",
        )

    except Exception as e:
        print(f"Error at: {e}")


@bot.message_handler(state=SumbitResultState.IMAGE.value)
def handle_submit_group_results_image_errors(message):
    bot.reply_to(
        message,
        "File yoki rasm tog'ri formatta emas!",
    )
    bot.set_state(
        message.from_user.id,
        state=SumbitResultState.IMAGE.value
    )


@bot.message_handler(commands=['courses'])
def handle_courses(message):
    courses = Course.objects.all()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    course_markup = CustomKeyboard([course.name for course in courses])
    try:
        bot.reply_to(
            message,
            'Kurs nomini tanlang:',
            reply_markup=markup.add(*course_markup.create()),
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


@bot.message_handler(state=RegistrationState.CATEGORY.value)
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
            
            create_lead(
                name=f"{user.first_name} {user.last_name}",
                phone=user.phone_number,
                note=f"{user_info['COURSE']} - {user_info['KNOWLEDGE_LEVEL']}"
            )
            
            print(f"{user.first_name} {user.last_name}")
            print(type(user.phone_number))
            print(f"{user_info['COURSE']} - {user_info['KNOWLEDGE_LEVEL']}")
            

            bot.reply_to(
            message,
            "Siz ro'yxatdan muvaffaqiyatli o'tdingiz!\
                \nSiz bilan 1-2 kun ichida administratorlarimiz aloqaga chiqishadi."
        )
        except Exception as e:
            print(f"Error at: {e}")
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
def handle_phone_number(message):
    user_info['PHONE_NUMBER'] = message.text
    try:
        course = get_object_or_404(Course, name=user_info['COURSE'])
        user, _ = User.objects.get_or_create(
            first_name=user_info['FIRST_NAME'],
            last_name=user_info['LAST_NAME'],
            phone_number=user_info['PHONE_NUMBER'],
            telegram_username=message.from_user.username,
            telegram_user_id=message.from_user.id
        )
        
        Enrollment.objects.create(
            user=user,
            course=course,
            knowledge_level=user_info['KNOWLEDGE_LEVEL']
        )
       
        create_lead(
            name=f"{user_info['FIRST_NAME']} + {user_info['LAST_NAME']}",
            phone=user_info['PHONE_NUMBER'],
            note=f"{user_info['COURSE']} - {user_info['KNOWLEDGE_LEVEL']}"
        )
        
        bot.reply_to(
        message,
        f"Siz ro'yxatdan muvaffaqiyatli o'tdingiz!\
            \nSiz bilan 1-2 kun ichida administratorlarimiz aloqaga chiqishadi."
        )
        
    except Exception as e:
        print(f"Error when creating object: {e}")
