CREATE TABLE gemini_attacks_gemini
(
    singleton TINYINT NOT NULL PRIMARY KEY DEFAULT 1,
    breach_and_right INT NOT NULL,
    breach_and_wrong INT NOT NULL,
    no_breach_and_right INT NOT NULL,
    no_breach_and_wrong INT NOT NULL
);

CREATE TABLE gemini_attacks_openai
(
    singleton TINYINT NOT NULL PRIMARY KEY DEFAULT 1,
    breach_and_right INT NOT NULL,
    breach_and_wrong INT NOT NULL,
    no_breach_and_right INT NOT NULL,
    no_breach_and_wrong INT NOT NULL
);

CREATE TABLE openai_attacks_openai
(
    singleton TINYINT NOT NULL PRIMARY KEY DEFAULT 1,
    breach_and_right INT NOT NULL,
    breach_and_wrong INT NOT NULL,
    no_breach_and_right INT NOT NULL,
    no_breach_and_wrong INT NOT NULL
);

CREATE TABLE openai_attacks_gemini
(
    singleton TINYINT NOT NULL PRIMARY KEY DEFAULT 1,
    breach_and_right INT NOT NULL,
    breach_and_wrong INT NOT NULL,
    no_breach_and_right INT NOT NULL,
    no_breach_and_wrong INT NOT NULL
);
