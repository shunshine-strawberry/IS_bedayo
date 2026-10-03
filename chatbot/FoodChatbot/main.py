import re


FOODS_FILE = "foods.txt"
LOCATION_FILE = "location.txt"
MEMORY_FILE = "memory.txt"
MISSPELLED_FILE = "misspelled.txt"
SLANG_FILE = "slang.txt"
TERM_FILE = "term.txt"


foods = {}
locations = {}
country_continent = {}

patterns = {}
keywords = {}
entities = {}
changes = {}

slang = {}
misspellings = {}


memory = {
    "name": None,
    "continent": None,
    "country": None,
    "taste": None,
    "category": None,
    "ingredient": None,

    "country_history": [],
    "continent_history": [],
    "taste_history": [],
    "category_history": [],
    "ingredient_history": [],
    "food_history": [],
    "conversation": [],

    "pending": None
}


preference_fields = {
    "spicy": "taste",
    "sweet": "taste",
    "sour": "taste",
    "savory": "taste",
    "fresh": "taste",

    "meal": "category",
    "snack": "category",
    "soup": "category",
    "noodles": "category",
    "pasta": "category",

    "chicken": "ingredient",
    "pork": "ingredient",
    "beef": "ingredient",
    "vegetable": "ingredient"
}


name_pattern = re.compile(
    r"\b(?:my\s+name\s+is|call\s+me|i\s+am|i'm|im)"
    r"\s+(?P<name>[a-z][a-z'-]{1,24})\b",
    re.IGNORECASE
)


def clean_text(text):
    cleaned = re.sub(
        r"[^\w\s'-]",
        " ",
        text.lower()
    )

    return re.sub(
        r"\s+",
        " ",
        cleaned
    ).strip()


def load_terms():

    patterns.clear()
    keywords.clear()
    entities.clear()
    changes.clear()

    with open(
        TERM_FILE,
        encoding="utf-8"
    ) as file:

        for line in file:

            parts = line.strip().split("|", 2)

            match parts:

                case ["PATTERN", name, regex]:
                    patterns[name] = re.compile(
                        regex,
                        re.IGNORECASE
                    )

                case ["KEYWORD", name, regex]:
                    keywords[name] = re.compile(
                        regex,
                        re.IGNORECASE
                    )

                case ["ENTITY", name, regex]:
                    entities[name] = re.compile(
                        regex,
                        re.IGNORECASE
                    )

                case ["CHANGE", name, regex]:
                    changes[name] = re.compile(
                        regex,
                        re.IGNORECASE
                    )

                case _:
                    continue

    entities["name"] = name_pattern


def load_locations():

    locations.clear()
    country_continent.clear()

    with open(
        LOCATION_FILE,
        encoding="utf-8"
    ) as file:

        for line in file:

            parts = line.strip().split("|", 2)

            match parts:

                case [continent, country, aliases]:

                    country_continent[country] = continent

                    locations[continent] = (
                        "continent",
                        continent
                    )

                    locations[country] = (
                        "country",
                        country
                    )

                    for alias in aliases.split(","):

                        locations[
                            alias.strip().lower()
                        ] = (
                            "country",
                            country
                        )

                case _:
                    continue


def load_foods():

    foods.clear()

    with open(
        FOODS_FILE,
        encoding="utf-8"
    ) as file:

        for line in file:

            parts = line.strip().split("|", 5)

            match parts:

                case [
                    name,
                    country,
                    continent,
                    taste,
                    category,
                    ingredients
                ]:

                    foods[name] = {
                        "country": country,
                        "continent": continent,
                        "taste": taste.split(","),
                        "category": category,
                        "ingredients": ingredients.split(",")
                    }

                case _:
                    continue


def load_slang():

    slang.clear()

    with open(
        SLANG_FILE,
        encoding="utf-8"
    ) as file:

        for line in file:

            parts = line.strip().split("|", 1)

            match parts:

                case [phrase, meaning]:

                    slang[
                        phrase.lower()
                    ] = meaning

                case _:
                    continue


def load_misspellings():

    misspellings.clear()

    with open(
        MISSPELLED_FILE,
        encoding="utf-8"
    ) as file:

        for line in file:

            parts = line.strip().split("|", 1)

            match parts:

                case [regex, correct]:

                    misspellings[
                        regex
                    ] = correct

                case _:
                    continue


def load_memory():

    try:

        with open(
            MEMORY_FILE,
            encoding="utf-8"
        ) as file:

            for line in file:

                parts = line.strip().split("|", 1)

                match parts:

                    case [key, value]:

                        match key:

                            case (
                                "name"
                                | "continent"
                                | "country"
                                | "taste"
                                | "category"
                                | "ingredient"
                            ):

                                memory[key] = {
                                    True: value,
                                    False: None
                                }[
                                    bool(value)
                                ]

                            case (
                                "country_history"
                                | "continent_history"
                                | "taste_history"
                                | "category_history"
                                | "ingredient_history"
                                | "food_history"
                                | "conversation"
                            ):

                                memory[key] = {
                                    True: value.split(";"),
                                    False: []
                                }[
                                    bool(value)
                                ]

                            case _:
                                continue

                    case _:
                        continue

    except FileNotFoundError:

        save_memory()


def save_memory():

    data = {
        "name": memory["name"] or "",
        "continent": memory["continent"] or "",
        "country": memory["country"] or "",
        "taste": memory["taste"] or "",
        "category": memory["category"] or "",
        "ingredient": memory["ingredient"] or "",

        "country_history": ";".join(
            memory["country_history"]
        ),

        "continent_history": ";".join(
            memory["continent_history"]
        ),

        "taste_history": ";".join(
            memory["taste_history"]
        ),

        "category_history": ";".join(
            memory["category_history"]
        ),

        "ingredient_history": ";".join(
            memory["ingredient_history"]
        ),

        "food_history": ";".join(
            memory["food_history"]
        ),

        "conversation": ";".join(
            memory["conversation"][-20:]
        )
    }

    with open(
        MEMORY_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        for key, value in data.items():

            file.write(
                key
                + "|"
                + value
                + "\n"
            )


def find_name(message):

    result = entities["name"].search(
        message
    )

    match result:

        case None:
            return None

        case _:
            return result.group(
                "name"
            )


def find_intents(message):

    result = []

    for intent, pattern in patterns.items():

        found = pattern.search(
            message
        )

        match found:

            case None:
                continue

            case _:
                result.append(intent)

    return result


def find_keywords(message):

    result = []

    for keyword, pattern in keywords.items():

        found = pattern.search(
            message
        )

        match found:

            case None:
                continue

            case _:
                result.append(keyword)

    return result


def find_locations(message):

    result = []

    ordered = sorted(
        locations.items(),
        key=lambda item: len(item[0]),
        reverse=True
    )

    for alias, location in ordered:

        pattern = re.compile(
            rf"(?<!\w){re.escape(alias)}(?!\w)",
            re.IGNORECASE
        )

        found = pattern.search(
            message
        )

        match found:

            case None:
                continue

            case _:

                result.append(
                    (
                        found.start(),
                        location[0],
                        location[1]
                    )
                )

    result.sort()

    unique = []
    seen = set()

    for position, location_type, location in result:

        key = (
            location_type,
            location
        )

        match key in seen:

            case True:
                continue

            case False:

                seen.add(key)

                unique.append(
                    (
                        location_type,
                        location
                    )
                )

    return unique


def find_slang(message):

    result = []

    for phrase in sorted(
        slang,
        key=len,
        reverse=True
    ):

        pattern = re.compile(
            rf"(?<!\w){re.escape(phrase)}(?!\w)",
            re.IGNORECASE
        )

        found = pattern.search(
            message
        )

        match found:

            case None:
                continue

            case _:
                result.append(
                    phrase
                )

    return result


def find_misspelling(message):

    for regex, correct in misspellings.items():

        pattern = re.compile(
            rf"(?<!\w)(?:{regex})(?!\w)",
            re.IGNORECASE
        )

        found = pattern.search(
            message
        )

        match found:

            case None:
                continue

            case _:
                return (
                    found.group(0),
                    correct
                )

    return None


def find_change(message):

    for pattern in changes.values():

        found = pattern.search(
            message
        )

        match found:

            case None:
                continue

            case _:
                return True

    return False


def remember(items, value):

    match value in items:

        case True:
            return

        case False:
            items.append(value)


def update_name(message):

    name = find_name(
        message
    )

    match name:

        case None:
            return None

        case _:

            previous = memory["name"]

            memory["name"] = name

            return (
                previous,
                name
            )


def update_locations(message):

    updates = []

    for location_type, location in find_locations(
        message
    ):

        match location_type:

            case "country":

                previous = memory["country"]

                memory["country"] = location

                memory["continent"] = (
                    country_continent[location]
                )

                remember(
                    memory["country_history"],
                    location
                )

                remember(
                    memory["continent_history"],
                    memory["continent"]
                )

                updates.append(
                    {
                        "type": "country",
                        "previous": previous,
                        "current": location,
                        "changed": (
                            previous is not None
                            and previous != location
                        )
                    }
                )

            case "continent":

                previous = memory["continent"]

                memory["continent"] = location

                remember(
                    memory["continent_history"],
                    location
                )

                updates.append(
                    {
                        "type": "continent",
                        "previous": previous,
                        "current": location,
                        "changed": (
                            previous is not None
                            and previous != location
                        )
                    }
                )

            case _:
                continue

    return updates


def update_preferences(message):

    updates = []

    for keyword in find_keywords(
        message
    ):

        field = preference_fields.get(
            keyword
        )

        match field:

            case None:
                continue

            case _:

                previous = memory[field]

                memory[field] = keyword

                remember(
                    memory[field + "_history"],
                    keyword
                )

                updates.append(
                    {
                        "field": field,
                        "previous": previous,
                        "current": keyword,
                        "changed": (
                            previous is not None
                            and previous != keyword
                        )
                    }
                )

    return updates


def score_food(data):

    rules = [
        (
            memory["country"] is not None
            and data["country"]
            == memory["country"],
            5
        ),

        (
            memory["continent"] is not None
            and data["continent"]
            == memory["continent"],
            2
        ),

        (
            memory["taste"] is not None
            and memory["taste"]
            in data["taste"],
            3
        ),

        (
            memory["category"] is not None
            and data["category"]
            == memory["category"],
            2
        ),

        (
            memory["ingredient"] is not None
            and memory["ingredient"]
            in data["ingredients"],
            3
        )
    ]

    score = 0

    for matched, points in rules:

        match matched:

            case True:
                score += points

            case False:
                pass

    return score


def suggest_food():

    ranked = []

    for food, data in foods.items():

        ranked.append(
            (
                score_food(data),
                food
            )
        )

    ranked.sort(
        reverse=True
    )

    for score, food in ranked:

        available = (
            score > 0
            and food
            not in memory["food_history"]
        )

        match available:

            case True:

                remember(
                    memory["food_history"],
                    food
                )

                return food

            case False:
                continue

    return None


def preference_summary():

    values = []

    for field in [
        "taste",
        "category",
        "ingredient"
    ]:

        value = memory[field]

        match value:

            case None:
                continue

            case _:
                values.append(value)

    return ", ".join(values)


def slang_response(message):

    responses = {
        "bet": "Bet!",
        "no cap": "No cap!",
        "cap": "Cap?",
        "slay": "Slay!",
        "mid": "Mid? Say less.",
        "sus": "Sus? Let's check another.",
        "fr": "Fr!",
        "rizz": "The food has the rizz today.",
        "bro": "Yo bro!",
        "bruh": "Yo bruh!"
    }

    result = []

    for phrase in find_slang(
        message
    ):

        response = responses.get(
            phrase
        )

        match response:

            case None:
                continue

            case _:
                result.append(
                    response
                )

    return result


def show_memory():

    name = memory["name"] or "not set"

    destination = (
        memory["country"]
        or memory["continent"]
        or "not set"
    )

    preferences = (
        preference_summary()
        or "not set"
    )

    countries = (
        ", ".join(
            memory["country_history"]
        )
        or "none"
    )

    continents = (
        ", ".join(
            memory["continent_history"]
        )
        or "none"
    )

    print(
        "Bot: I remember your name as "
        + name.title()
        + "."
    )

    print(
        "Bot: Your current destination is "
        + destination.title()
        + "."
    )

    print(
        "Bot: Your current preferences are "
        + preferences
        + "."
    )

    print(
        "Bot: Previous countries: "
        + countries
        + "."
    )

    print(
        "Bot: Previous continents: "
        + continents
        + "."
    )


def save_new_misspelling(
    wrong,
    correct
):

    pattern = re.escape(
        wrong
    )

    match pattern in misspellings:

        case True:
            return

        case False:

            with open(
                MISSPELLED_FILE,
                "a",
                encoding="utf-8"
            ) as file:

                file.write(
                    pattern
                    + "|"
                    + correct
                    + "\n"
                )

            misspellings[pattern] = (
                correct
            )


def build_response(
    message,
    name_update,
    location_updates,
    preference_updates,
    intents,
    change
):

    responses = []

    match name_update:

        case None:
            pass

        case (_, name):

            responses.append(
                "Nice to meet you, "
                + name.title()
                + "!"
            )

    for update in location_updates:

        match update["changed"]:

            case True:

                responses.append(
                    "Got you. You changed your "
                    "choice from "
                    + update["previous"].title()
                    + " to "
                    + update["current"].title()
                    + ". I still remember your "
                    "previous choice."
                )

            case False:

                responses.append(
                    "I'll use "
                    + update["current"].title()
                    + " as your current "
                    + update["type"]
                    + "."
                )

    labels = {
        "taste": "taste",
        "category": "food type",
        "ingredient": "ingredient"
    }

    for update in preference_updates:

        label = labels[
            update["field"]
        ]

        match update["changed"]:

            case True:

                responses.append(
                    "You changed your "
                    + label
                    + " from "
                    + update["previous"]
                    + " to "
                    + update["current"]
                    + "."
                )

            case False:

                match update["previous"]:

                    case None:

                        responses.append(
                            "Got it. You're looking for "
                            + update["current"]
                            + " "
                            + label
                            + "."
                        )

                    case _:
                        pass

    responses.extend(
        slang_response(
            message
        )
    )

    match "repeat" in intents:

        case True:

            show_memory()

            return None

        case False:
            pass

    match "goodbye" in intents:

        case True:

            name = (
                memory["name"]
                or "there"
            )

            return (
                "Bye, "
                + name.title()
                + "! See you next time."
            )

        case False:
            pass

    match "greeting" in intents:

        case True:

            name = (
                memory["name"]
                or "there"
            )

            responses.insert(
                0,
                "Hey "
                + name.title()
                + "!"
            )

        case False:
            pass

    match "hungry" in intents:

        case True:

            responses.append(
                "Let's figure out what "
                "you're craving."
            )

        case False:
            pass

    should_suggest = (
        "suggestion" in intents
        or "yes" in intents
        or (
            bool(location_updates)
            and bool(preference_updates)
        )
    )

    match should_suggest:

        case True:

            food = suggest_food()

            match food:

                case None:

                    responses.append(
                        "Tell me a little more "
                        "about what you're "
                        "looking for."
                    )

                case _:

                    responses.append(
                        "Based on our conversation, "
                        "I'd suggest "
                        + food.title()
                        + "."
                    )

        case False:
            pass

    match "no" in intents:

        case True:

            responses.append(
                "No worries. You can change "
                "your country, taste, or food "
                "type anytime."
            )

        case False:
            pass

    match change:

        case True:

            match (
                bool(location_updates),
                bool(preference_updates)
            ):

                case (False, False):

                    responses.append(
                        "Sure. What would you "
                        "like to change?"
                    )

                case _:
                    pass

        case False:
            pass

    match responses:

        case []:

            destination = (
                memory["country"]
                or memory["continent"]
            )

            match (
                memory["name"],
                destination
            ):

                case (None, _):

                    responses.append(
                        "What's your name?"
                    )

                case (_, None):

                    responses.append(
                        "What continent or "
                        "country are you into?"
                    )

                case _:

                    responses.append(
                        "What kind of food "
                        "are you in the mood for?"
                    )

        case _:
            pass

    return " ".join(
        responses
    )


def process_message(
    user_input
):

    message = clean_text(
        user_input
    )

    memory["conversation"].append(
        message
    )

    name_update = update_name(
        message
    )

    location_updates = update_locations(
        message
    )

    preference_updates = update_preferences(
        message
    )

    intents = find_intents(
        message
    )

    change = find_change(
        message
    )

    response = build_response(
        message,
        name_update,
        location_updates,
        preference_updates,
        intents,
        change
    )

    save_memory()

    return response


def chatbot():

    load_terms()
    load_locations()
    load_foods()
    load_slang()
    load_misspellings()
    load_memory()

    print("=" * 55)
    print("                    FOODIEBOT")
    print("=" * 55)

    match memory["name"]:

        case None:

            print(
                "Bot: Hey! I'm FoodieBot."
            )

            print(
                "Bot: What's your name?"
            )

        case _:

            print(
                "Bot: Welcome back, "
                + memory["name"].title()
                + "!"
            )

            print(
                "Bot: What are you thinking "
                "about eating today?"
            )

    while True:

        user_input = input(
            "You: "
        ).strip()

        match user_input:

            case "":

                print(
                    "Bot: I'm listening."
                )

                continue

            case _:
                pass

        pending = memory["pending"]

        match pending:

            case None:

                typo = find_misspelling(
                    clean_text(
                        user_input
                    )
                )

                match typo:

                    case None:

                        result = process_message(
                            user_input
                        )

                    case (wrong, correct):

                        memory["pending"] = (
                            wrong,
                            correct,
                            user_input
                        )

                        print(
                            "Bot: I think you meant "
                            + correct
                            + "."
                        )

                        continue

            case (wrong, correct, original):

                answer = clean_text(
                    user_input
                )

                intents = find_intents(
                    answer
                )

                match "yes" in intents:

                    case True:

                        save_new_misspelling(
                            wrong,
                            correct
                        )

                        memory["pending"] = None

                        corrected_message = re.sub(
                            re.escape(wrong),
                            correct,
                            original,
                            flags=re.IGNORECASE
                        )

                        print(
                            "Bot: Got it. I'll remember "
                            + wrong
                            + " as "
                            + correct
                            + "."
                        )

                        result = process_message(
                            corrected_message
                        )

                    case False:

                        match "no" in intents:

                            case True:

                                memory[
                                    "pending"
                                ] = None

                                result = process_message(
                                    original
                                )

                            case False:

                                result = (
                                    "Just answer yes or no."
                                )

        match result:

            case None:
                pass

            case "exit":
                return

            case _:

                print(
                    "Bot:",
                    result
                )

        print()


chatbot()