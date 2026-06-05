# app.py
from flask import Flask, render_template, redirect, url_for, session, request
from create_db import create_db
from models import db, Sushi, Main, Dop


app = Flask(__name__)

# --- КОНФІГУРАЦІЯ FLASK ---
app.config['SECRET_KEY'] = 'your_super_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


# --- МАРШРУТИ (ROUTES) ---

@app.route('/')
def home():
    """
    Головна сторінка додатку.
    """
    return render_template('index.html')

@app.route('/step1', methods=["GET", "POST"])
def step1():
    #коли натискаємо кнопку далі
    if request.method == "POST":
        sushi_id = request.form.get("sushi")
        if sushi_id:
           session['sushi_id'] = int(sushi_id)
        print(session)

        return redirect(url_for('step2'))
    #Get запит
    session.clear() #очищяємо сесію



    sushis = Sushi.query.all()#отримаємо всі типо суші
    return render_template('step1.html', sushis=sushis)





@app.route('/step2', methods=["GET", "POST"])
def step2():
    if 'sushi_id'not in session:
        return redirect(url_for('step1'))
    #коли натискаємо кнопку далі
    if request.method == "POST":
        main_id = request.form.get("main")
        if main_id:
           session['main_id'] = int(main_id)
        print(session)

        return redirect(url_for('step3'))
    #Get запит
    mains =  Main.query.all()
    selected_main_id = session.get('main_id')
    return render_template( 'step2.html', mains=mains,selected_main_id=selected_main_id)


@app.route('/step3', methods=["GET", "POST"])
def step3():
    if 'main_id' not in session:
        return redirect(url_for('step2'))

    if request.method == "POST":
        name = request.form.get('name', '')
        phone = request.form.get('phone', '')
        comment = request.form.get('comment', '')

        session['name'] = name
        session['phone'] = phone
        session['comment'] = comment

        dop_ids = [int(value) for value in request.form.getlist('dop')]
        session['dop_ids'] = dop_ids

        dop_quantities = {}
        for dop_id in dop_ids:
            count = request.form.get(f'count_{dop_id}')
            dop_quantities[dop_id] = int(count)

        session['dop_quantities'] = dop_quantities

        return redirect(url_for('sum'))

    dops = Dop.query.all()
    return render_template('step3.html', dops=dops)

@app.route('/sum', methods=["GET", "POST"])
def sum():
    total_price = 0
    name = session.get('name', "")
    phone = session.get('phone', "")
    comment = session.get('comment',"")
    sushi_id = session.get('sushi_id')
    sushi = Sushi.query.get(sushi_id)

    main_id = session.get('main_id')
    main = Main.query.get(main_id)
    dop_ids = session.get('dop_ids')
    dops = Dop.query.filter(Dop.id.in_(dop_ids)).all()
    selected_quantities = {
        int(key): value for key, value in session.get('dop_quantities', {}).items()
    }
    total_price= sushi.price = main.price
    for dop in dops:
        count = selected_quantities.get(dop.id, 1)
        total_price += dop.price * count
    return render_template('sum.html',total_price=total_price,
    name=name, phone=phone, comment=comment, sushi=sushi , main=main  ,dops=dops,selected_quantities=selected_quantities)


@app.route('/confirm', methods=["GET", "POST"])
def confirm():
    session.clear()
    return redirect("/")

import random


quotes = [
    # --- МОТИВАЦІЯ ТА УСПІХ ---
    {"text": "Будь собою, всі інші ролі вже зайняті. — Оскар Вайльд"},
    {"text": "Щоб дійти до мети, людині потрібно тільки одне — йти. — Оноре де Бальзак"},
    {"text": "Успіх — це здатність крокувати від однієї невдачі до іншої, не втрачаючи ентузіазму. — Вінстон Черчилль"},
    {"text": "Найкращий спосіб передбачити майбутнє — створити його. — Пітер Друкер"},
    {"text": "Логіка може привести вас від пункту А до пункту Б, а уява — куди завгодно. — Альберт Ейнштейн"},
    {"text": "Ніколи не пізно стати тим, ким ти міг би бути. — Джордж Еліот"},
    {"text": "Зробіть перший крок, вірячи. Вам не обов'язково бачити всі сходи, просто зробіть перший крок. — Мартін Лютер Кінг"},
    {"text": "Ваш час обмежений, тому не витрачайте його, живучи чужим життям. — Стів Джобс"},
    {"text": "Те, що нас не вбиває, робить нас сильнішими. — Фрідріх Ніцше"},
    {"text": "Перешкоди — це ті страшні речі, які ви бачите, коли відводите погляд від мети. — Генрі Форд"},

    # --- МУДРІСТЬ ТА ЖИТТЯ ---
    {"text": "Життя — це те, що з нами відбувається, поки ми будуємо інші плани. — Джон Леннон"},
    {"text": "Я знаю, що нічого не знаю. — Сократ"},
    {"text": "Хто рухається вперед, той долає гори. — Українське прислів'я"},
    {"text": "Не шукайте винних, шукайте засоби виправлення. — Генрі Форд"},
    {"text": "Щастя — це не щось готове. Воно походить від ваших власних дій. — Далай-лама"},
    {"text": "Ми оцінюємо себе за тим, що відчуваємо здатними зробити, тоді як інші оцінюють нас за тим, що ми вже зробили. — Генрі Лонгфелло"},
    {"text": "Справжнє правило життя: роби те, що любиш, і люби те, що робиш."},
    {"text": "Мир не можна зберегти силою. Його можна досягти лише взаєморозумінням. — Альберт Ейнштейн"},
    {"text": "Той, хто має «навіщо» жити, може витримати майже будь-яке «як». — Фрідріх Ніцше"},

    # --- КУМЕДНІ ТА ІРОНІЧНІ ---
    {"text": "Якщо ви думаєте, що ви занадто малі, щоб щось змінити, спробуйте заснути в кімнаті з комарем. — Далай-лама"},
    {"text": "Молодий я був дурний. Зараз я вже дорослий, досвідчений дурень."},
    {"text": "Я не лінивий. Я перебуваю в режимі енергозбереження."},
    {"text": "Інтуїція — це здатність голови чути дупу."},
    {"text": "Все йде добре, просто повз."},
    {"text": "Якщо робота не вовк, то чому вона так виє в понеділок зранку?"},
    {"text": "Гроші не приносять щастя, але плакати в лімузині набагато комфортніше, ніж в автобусі."},

    # --- ГЕЙМЕРСЬКІ ТА MINECRAFT СТИЛЬ ---
    {"text": "Не копай прямо під себе. Це перше правило виживання."},
    {"text": "Життя — це гра."}
]
@app.route('/info')
def info():
    # 4. Вирівняно відступи та виправлено назви змінної на "quote"
    quote = random.choice(quotes)
    return render_template('info.html', quote=quote)





# --- ЗАПУСК ДОДАТКА ---

if __name__ == '__main__':
    # create_db()
    app.run(debug=True)
