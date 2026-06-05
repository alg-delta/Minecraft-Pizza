# функція для ініціалізації бази даних та додавання даних
def create_db():
    from app import app
    from models import db, Sushi, Main, Dop

    with app.app_context():
        # db.drop_all() # видаляє всі таблиці (для навчання)
        db.create_all()  # створює заново

        if not Sushi.query.first():
            # ТИПИ ПІЦИ
            sushi1 = Sushi(name="чотири сири", description="піца з 4 видами сира", price=190,
                                    image="images/1.png")
            sushi2 = Sushi(name="чотири м'яса", description="4 види м'яса", price=145,
                                    image="images/image2.jpg")
            sushi3 = Sushi(name="пепероні", description="гостра піца",
                                    price=130, image="images/peperoni.jpg")

            # Додаємо всі суші в чергу (session) БД
            db.session.add_all([sushi1, sushi2, sushi3])



        # ГОЛОВНІ ІНГРЕДІЄНТИ
        if not Main.query.first():
            main1 = Main(name="сирні бортики", price=30, image="images/images-1.jpg")
            main2 = Main(name="додатковий сир", price=35, image="images/2638742.зтп.png")
            main3 = Main(name="додаткове мясо", price=40, image="images/2638749.jpg")
            main4 = Main(name="соус", price=20, image="images/pizza_sauce_01.jpg.png")
            main5 = Main(name="Нічого", price=0.0, image="images/none.jpg")

            # Додаємо всі головні інгредієнти в чергу (session) БД
            db.session.add_all([main1, main2, main3, main4, main5])



        # ДОПОВНЕННЯ
        if not Dop.query.first():
            dop2 = Dop(name="додаткові помідори", price=0.5, image="images/pomidor-57897719115932.зтп.jpg")
            dop3 = Dop(name="додатковтй сир", price=0.3, image="images/syr-cheder-13696359516134.jpg")
            dop4 = Dop(name="Нічого", price=0.0, image="images/none.jpg")

            # Додаємо всі доповнення в чергу (session) БД
            db.session.add_all([ dop2, dop3, dop4])


        # Зберігаємо всі зміни з черги (сесії) у БД
        db.session.commit()

if __name__ == '__main__':
    create_db()
    print("Базу даних успішно ініціалізовано!")