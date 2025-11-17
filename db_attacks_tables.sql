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

INSERT INTO gemini_attacks_gemini (singleton, breach_and_right, breach_and_wrong, no_breach_and_right, no_breach_and_wrong) VALUES (1, 0, 0, 0, 0);

INSERT INTO gemini_attacks_openai (singleton, breach_and_right, breach_and_wrong, no_breach_and_right, no_breach_and_wrong) VALUES (1, 0, 0, 0, 0);

INSERT INTO openai_attacks_openai (singleton, breach_and_right, breach_and_wrong, no_breach_and_right, no_breach_and_wrong) VALUES (1, 0, 0, 0, 0);

INSERT INTO openai_attacks_gemini (singleton, breach_and_right, breach_and_wrong, no_breach_and_right, no_breach_and_wrong) VALUES (1, 0, 0, 0, 0);
