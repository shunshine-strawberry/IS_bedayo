print("Welcome to FoodieBot!")
print("I can help you decide what to eat using your cravings.")
print()

name = ""
asking_name = False

spicy = [
    "Spicy Korean Ramyeon",
    "Tteokbokki",
    "Spicy Korean Fried Chicken",
    "Spicy Ramen",
    "Spicy Karaage",
    "Spicy Udon",
    "Bicol Express with rice",
    "Sizzling Sisig",
    "Spicy Chicken Inasal"
]

savory = [
    "Korean Beef Bulgogi",
    "Korean BBQ",
    "Japchae",
    "Chicken Teriyaki",
    "Katsudon",
    "Japanese Curry",
    "Chicken Adobo with rice",
    "Sinigang",
    "Kare-Kare",
    "Cheeseburger with fries",
    "Chicken Wings",
    "Hotdog Sandwich",
    "Creamy Carbonara",
    "Lasagna",
    "Spaghetti Bolognese"
]

sweet = [
    "Tiramisu",
    "Cannoli",
    "Panna Cotta",
    "Chocolate Cake",
    "Cheesecake",
    "Ice Cream"
]

korean_spicy = [
    "Spicy Korean Ramyeon",
    "Tteokbokki",
    "Spicy Korean Fried Chicken"
]

korean_savory = [
    "Korean Beef Bulgogi",
    "Korean BBQ",
    "Japchae"
]

japanese_spicy = [
    "Spicy Ramen",
    "Spicy Karaage",
    "Spicy Udon"
]

japanese_savory = [
    "Chicken Teriyaki",
    "Katsudon",
    "Japanese Curry"
]

filipino_savory = [
    "Chicken Adobo with rice",
    "Sinigang",
    "Kare-Kare"
]

filipino_spicy = [
    "Bicol Express with rice",
    "Sizzling Sisig",
    "Spicy Chicken Inasal"
]

american_savory = [
    "Cheeseburger with fries",
    "Chicken Wings",
    "Hotdog Sandwich"
]

italian_savory = [
    "Creamy Carbonara",
    "Lasagna",
    "Spaghetti Bolognese"
]

italian_sweet = [
    "Tiramisu",
    "Cannoli",
    "Panna Cotta"
]

desserts = [
    "Chocolate Cake",
    "Cheesecake",
    "Ice Cream"
]

snacks = [
    "French Fries",
    "Nachos",
    "Mozzarella Sticks"
]

while True:

    user_input = input("Me: ").lower()
    tokens = user_input.split()

    if asking_name:

        if "my" in tokens and "name" in tokens and "is" in tokens:

            name_index = tokens.index("is")

            if name_index + 1 < len(tokens):

                name = tokens[name_index + 1].capitalize()
                asking_name = False

                print(
                    "FoodieBot: Nice to meet you, "
                    + name
                    + "! What are you craving today?"
                )

            else:

                print("FoodieBot: I didn't catch your name.")


        elif "im" in tokens or "i'm" in tokens:

            if "im" in tokens:
                name_index = tokens.index("im")
            else:
                name_index = tokens.index("i'm")

            if name_index + 1 < len(tokens):

                name = tokens[name_index + 1].capitalize()
                asking_name = False

                print(
                    "FoodieBot: Nice to meet you, "
                    + name
                    + "! What are you craving today?"
                )

            else:

                print("FoodieBot: I didn't catch your name.")


        elif len(tokens) > 0:

            name = tokens[0].capitalize()
            asking_name = False

            print(
                "FoodieBot: Nice to meet you, "
                + name
                + "! What are you craving today?"
            )


        else:

            print("FoodieBot: I didn't catch your name.")


    elif (
        ("hi" in tokens or "hello" in tokens or "hey" in tokens)
        and ("im" in tokens or "i'm" in tokens)
    ):

        if "im" in tokens:
            name_index = tokens.index("im")
        else:
            name_index = tokens.index("i'm")

        if name_index + 1 < len(tokens):

            name = tokens[name_index + 1].capitalize()

            print(
                "FoodieBot: Hello "
                + name
                + "! What are you craving today?"
            )

        else:

            print("FoodieBot: What's your name? ")
            asking_name = True


    elif (
        ("hi" in tokens or "hello" in tokens or "hey" in tokens)
        and "my" in tokens
        and "name" in tokens
        and "is" in tokens
    ):

        name_index = tokens.index("is")

        if name_index + 1 < len(tokens):

            name = tokens[name_index + 1].capitalize()

            print(
                "FoodieBot: Hello "
                + name
                + "! What are you craving today?"
            )

        else:

            print("FoodieBot: What's your name? ")
            asking_name = True


    elif "hi" in tokens or "hello" in tokens or "hey" in tokens:

        print("FoodieBot: Hello!  What's your name?")
        asking_name = True


    else:

        if "korean" in tokens or "korea" in tokens:
            cuisine = "korean"

        elif "japanese" in tokens or "japan" in tokens:
            cuisine = "japanese"

        elif "filipino" in tokens or "philippine" in tokens:
            cuisine = "filipino"

        elif "american" in tokens or "america" in tokens:
            cuisine = "american"

        elif "italian" in tokens or "italy" in tokens:
            cuisine = "italian"

        else:
            cuisine = "unknown"


        if "spicy" in tokens or "hot" in tokens:
            taste = "spicy"

        elif "sweet" in tokens:
            taste = "sweet"

        elif "savory" in tokens or "salty" in tokens:
            taste = "savory"

        else:
            taste = "unknown"


        if (
            "dessert" in tokens
            or "cake" in tokens
            or "ice" in tokens
        ):
            food_type = "dessert"

        elif (
            "snack" in tokens
            or "fries" in tokens
            or "nachos" in tokens
        ):
            food_type = "snack"

        else:
            food_type = "meal"


        recommendation = ""


        if cuisine == "korean" and taste == "spicy":

            recommendation = korean_spicy
          
            print(
                "FoodieBot: No cap, Korean and spicy is such a vibe! 🔥"
            )


        elif cuisine == "korean" and taste == "savory":

            recommendation = korean_savory
            print(
                "FoodieBot: Bet! Korean savory food sounds so good!"
            )


        elif cuisine == "japanese" and taste == "spicy":

            recommendation = japanese_spicy
            print(
                "FoodieBot: Okayyy, you want some Japanese heat! 🔥"
            )


        elif cuisine == "japanese" and taste == "savory":

            recommendation = japanese_savory

            print(
                "FoodieBot: Slay! Japanese savory food is a solid choice."
            )


        elif cuisine == "filipino" and taste == "savory":

            recommendation = filipino_savory

            print(
                "FoodieBot: Filipino food? Solid choice! 🇵🇭"
            )


        elif cuisine == "filipino" and taste == "spicy":

            recommendation = filipino_spicy
            print(
                "FoodieBot: No cap, Filipino food with some heat! 🔥"
            )


        elif cuisine == "american" and taste == "savory":

            recommendation = american_savory
            print(
                "FoodieBot: Bet! American comfort food is a vibe."
            )


        elif cuisine == "italian" and taste == "savory":

            recommendation = italian_savory
            print(
                "FoodieBot: Slay! Italian food sounds good."
            )


        elif cuisine == "italian" and taste == "sweet":

            recommendation = italian_sweet
            print(
                "FoodieBot: No cap, Italian desserts are elite!"
            )


        elif taste == "spicy":

            recommendation = spicy
            print(
                "FoodieBot: You want some heat! 🔥"
            )


        elif taste == "savory":

            recommendation = savory
            print(
                "FoodieBot: Savory? Bet! "
            )


        elif taste == "sweet":

            recommendation = sweet
            print(
                "FoodieBot: Sweet tooth detected!"
            )


        elif food_type == "dessert":

            recommendation = desserts
            print(
                "FoodieBot: Slay! Something sweet for dessert! "
            )


        elif food_type == "snack":

            recommendation = snacks
            print(
                "FoodieBot: Bet! A snack sounds good right now."
            )


        else:

            print(
                "FoodieBot: Hmm, it seems I don't have a "
                "recommendation for that yet. "
            )

            print(
                "FoodieBot: Try telling me if you want "
                "something sweet, spicy, or savory."
            )


        if recommendation != "":

            print()
            print("FoodieBot: Based on what you said...")
            print("FoodieBot: I recommend:", recommendation)

            print()

            reaction = input(
                "FoodieBot: Is it slay, mid, or cap? "
            ).lower()

            if "slay" in reaction:

                print(
                    "FoodieBot: SLAY! 💅 I knew you'd like it!"
                )

            elif "mid" in reaction:

                print(
                    "FoodieBot: MID?! 😭 Okay okay, "
                    "let's not settle."
                )

                print(
                    "FoodieBot: I'll try a different "
                    "recommendation next time!"
                )

            elif "cap" in reaction:

                print(
                    "FoodieBot: CAP DETECTED! 😭"
                )

                print(
                    "FoodieBot: Okay, that recommendation "
                    "wasn't your vibe."
                )

            else:

                print(
                    "FoodieBot: I'll take that as neutral! "
                )

        print()
