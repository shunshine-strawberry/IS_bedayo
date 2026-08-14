function triangular(x, a, b, c) {
                /*(b,1)
                /\
                /  \
            (a,0)   (c,0)*/
            
    // Outside the triangle
    if (x <= a || x >= c) {
        return 0;
    }

    // Peak
    if (x === b) {
        return 1;
    }

    // Rising side
    if (x > a && x < b) {
        return (x - a) / (b - a);
    }

    // Falling side
    if (x > b && x < c) {
        return (c - x) / (c - b);
    }

    return 0;
}


function Difficulty(value) {

    return {
        easy: triangular(value, 1, 1, 5),
        medium: triangular(value, 3, 5, 7),
        hard: triangular(value, 5, 10, 10)
    };
}



function Knowledge(value) {

    return {
        low: triangular(value, 0, 0, 5),
        medium: triangular(value, 3, 5, 8),
        high: triangular(value, 6, 10, 10)
    };
}


function Days(value) {

    return {
        highRisk: triangular(value, 0, 0, 3),
        lowRisk: triangular(value, 1, 4, 7),
        fewDays: triangular(value, 5, 8, 12),
        many: triangular(value, 10, 31, 31)
    };
}



function Mood(value) {

    return {
        underWeather: triangular(value, 1, 1, 4),
        neutral: triangular(value, 2, 5, 7),
        happy: triangular(value, 5, 7, 9),
        exceptional: triangular(value, 8, 10, 10)
    };
}

function FuzzyRule(difficultyValue, knowledgeValue, daysValue, moodValue) {

    const difficulty = Difficulty(difficultyValue);
    const knowledge = Knowledge(knowledgeValue);
    const days = Days(daysValue);
    const mood = Mood(moodValue);


   

    const rule1 = Math.min(
        difficulty.hard,
        knowledge.low,
        days.highRisk
    );


   
    const rule2 = Math.min(
        difficulty.hard,
        knowledge.medium
    );



    const rule3 = Math.min(
        difficulty.hard,
        knowledge.low
    );




    const rule4 = Math.min(
        difficulty.easy,
        knowledge.high
    );


  

    const rule5 = Math.min(
        difficulty.easy,
        knowledge.medium
    );


    
    const rule6 = difficulty.medium;

    const rule7 = days.highRisk;

    const critical = rule1;

    const high = Math.max(
        rule2,
        rule3,
        rule7
    );

    const low = Math.max(
        rule4,
        rule5
    );

    const normal = rule6;

    let level;
    let hours;
    let reasons;
    let ways;


    if (
        critical >= high &&
        critical >= low &&
        critical >= normal
    ) {

        level = "Critical";
        hours = 6;

        reasons =
            "Hard subject, little knowledge, and the deadline is very close.";

        ways =
            "Break the subject into smaller topics and study immediately.";
    }


    else if (
        high >= low &&
        high >= normal
    ) {

        level = "High";
        hours = 5;

        reasons =
            "The subject needs more attention and preparation.";

        ways =
            "Review your notes first, then solve practice problems.";
    }


    else if (low >= normal) {

        level = "Low";
        hours = 1;

        reasons =
            "You already have a good understanding of the subject.";

        ways =
            "Do a quick review and answer a few practice questions.";
    }


    else {

        level = "Normal";
        hours = 3;

        reasons =
            "The subject has a moderate level of difficulty.";

        ways =
            "Review your notes and practice the important concepts.";
    }

    if (mood.underWeather > 0) {

        ways +=
            " Take a 10-minute break, drink water, and start with an easy task.";
    }


    if (
        mood.happy > 0 ||
        mood.exceptional > 0
    ) {

        ways +=
            " You're in a good mood—start with the most challenging topic.";
    }


   
    return {
        hours: hours,
        level: level,
        reasons: reasons,
        ways: ways,

        membership: {
            difficulty: difficulty,
            knowledge: knowledge,
            days: days,
            mood: mood
        },

        rules: {
            rule1: rule1,
            rule2: rule2,
            rule3: rule3,
            rule4: rule4,
            rule5: rule5,
            rule6: rule6,
            rule7: rule7
        }
    };
}


const difficultyInput =
    document.getElementById("difficulty");

const knowledgeInput =
    document.getElementById("knowledge");

const daysInput =
    document.getElementById("days");

const moodInput =
    document.getElementById("mood");

const resultBtn =
    document.getElementById("resultBtn");

const output =
    document.getElementById("output");


resultBtn.addEventListener("click", function () {

    // Check required inputs
    if (
        difficultyInput.value === "" ||
        knowledgeInput.value === "" ||
        daysInput.value === ""
    ) {

        output.innerHTML =
            "⚠️ Please answer all the questions first.";

        return;
    }


    // Convert input to numbers
    const difficultyValue =
        Number(difficultyInput.value);

    const knowledgeValue =
        Number(knowledgeInput.value);

    const daysValue =
        Number(daysInput.value);

    const moodValue =
        Number(moodInput.value);

    const result = FuzzyRule(
        difficultyValue,
        knowledgeValue,
        daysValue,
        moodValue
    );


    output.innerHTML = `
        <strong>${result.level}</strong>

        <br><br>

        ⏰ <strong>Study Time:</strong>
        ${result.hours} hours

        <br><br>

        📚 <strong>Reason:</strong>
        ${result.reasons}

        <br><br>

        💡 <strong>Tip:</strong>
        ${result.ways}
    `;

    console.log("Membership Values:");
    console.log(result.membership);

    console.log("Rule Strengths:");
    console.log(result.rules);
});