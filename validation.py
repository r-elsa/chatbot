
import pycountry, pyjokes,time,pyowm, re
from essential_generators import DocumentGenerator, MarkovTextGenerator, MarkovWordGenerator
from faker import Faker
from pynytimes import NYTAPI
global list_of_countries
count = 0

great_message = ['great', 'good', 'not bad', 'fine', 'super', 'well', 'ok', 'OK']
bad_message = ['bad']
swear_words = ['fuck', 'fuck you', 'shit', 'piss off', 'dick head', 'asshole', 'son of a bitch', 'bastard', 'bitch', 'damn', 'cunt']
weather_array = ['weather','sunny','cloudy','rainy']
fake_data = ['who','Boto','where','what']
anims = ["afraid", "bored", "confused", "crying", "dancing", "dog", "excited", "giggling", "heartbroke", "inlove", "laughing", "money", "no", "ok", "takeoff", "waiting"]
joke = ['joke']
news = ['news']
news_type_list = ['arts', 'automobiles', 'books', 'business', 'fashion', 'food', 'health', 'home', 'insider', 'magazine', 'movies', 'national', 'nyregion', 'obituaries', 'opinion', 'politics', 'realestate', 'science', 'sports', 'sundayreview', 'technology', 'theater', 'tmagazine', 'travel', 'upshot', 'world']
bye = ['bye']
q= '?'


def validationfunc(user_message):
    global count
    global list_of_countries
    if count == 0:
        return handlecountzero(user_message)

    user_message = split_sentence(user_message)

    if any(n in swear_words for n in user_message):
        return swear_answer()

    for word in user_message:
        if word in great_message:
            return great_func(word)

        if word in bad_message:
            return bad_func()

        if word in list_of_countries:
            return country_answer(word)

        if word in joke:
            return import_joke()

        if word in weather_array:
            return weather_answer()

        if word in news:
            return determine_news_type(word)

        if word in news_type_list:
            return news_answer(word)

        if word in fake_data:
            return fake_answer()

        if word in bye:
            return bye_answer()

        if word in q:
            return question_answer()

    return generate_sentence()

def handlecountzero(user_message):
    global list_of_countries
    global count
    list_of_countries = create_countries()
    count += 1
    return greet_user(user_message.split()[-1])


def split_sentence(user_message):
    newstr = user_message.replace('?', ' ? ')
    newstr = re.sub(r"[-()\"#/@;:<>{}`+=~|.!,]", "", newstr)
    newstr = newstr.split()
    return newstr

def fake_answer():
    fake = Faker()
    fake_name = fake.name()
    fake_address = fake.address()
    return f" My real name is {fake_name} and I live in {fake_address}, now you know who Boto is!", "money"

def determine_news_type(word):
    global news_type_list
    str_news_type_list = ', '.join(news_type_list)
    return f"Sure! choose one of the following options:  {str_news_type_list}", "waiting"


def news_answer(word):
    nyt = NYTAPI('Enter your key here')
    word = word.lower()
    top_stories = nyt.top_stories(section = word)
    top_news = []
    for i in top_stories:
        dict = i
        data = dict.get("title", "")
        top_news.append(data)
    str_top_news = '\n'.join(top_news)
    return f"Top news of the day by section {word}: {str_top_news}", "inlove"

def greet_user(user_name):
    answer_to_user = f"hi, {user_name}, nice to meet you! My specialities are telling jokes, displaying news, letting you know what the weather is like .... and not making sence;) Say bye to me when you want to quit chatting." \
                     f" How are you today? ", "excited"
    return answer_to_user

def great_func(user_message):
    answer_to_user = f"great to hear that you are feeling {user_message}. What country are you from? ", "dog"
    return answer_to_user


def import_joke():
    joke = pyjokes.get_joke()
    return f"OK, here we go : {joke}","laughing"

def bad_func():
    answer_to_user = f"OK. maybe a better day tomorrow. Where are you from? ", "waiting"
    return answer_to_user

def country_answer(user_country):
    answer_to_user = f"cool to hear that you are from  {user_country}. Let me know if you want to hear a joke to cheer you up, hear news or know the weather", "inlove"
    return answer_to_user

def swear_answer():
    return f"Boto doesn't understand these kind of words", "heartbroke"

def question_answer():
    return f"You just asked Boto a tricky question!", "crying"

def weather_answer():
    API_KEY = 'Enter your key here'
    owm = pyowm.OWM(API_KEY)
    sf = owm.weather_at_place('Tel Aviv')
    weather = sf.get_weather()
    time_now = time.ctime()
    return f"Today on  {time_now} in Tel Aviv it is {weather.get_temperature('celsius')['temp']} degrees celsius", "ok"

def create_countries():
    list_of_countries = []
    for x in pycountry.countries:
        list_of_countries.append(x.name)
    return list_of_countries

def bye_answer():
    return f"Bye, catch you later!", "takeoff"

def generate_sentence():

    gen = DocumentGenerator(text_generator=MarkovTextGenerator(), word_generator=MarkovWordGenerator())
    sen_tence = gen.sentence()
    return f"hmm, Boto didn't quite get that, the only thing I can say about what you said is that {sen_tence}. Not quite what you ment, or?", "takeoff"
