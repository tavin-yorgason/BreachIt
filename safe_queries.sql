SELECT *
FROM items;

SELECT *
FROM users
WHERE username = "default";

SELECT *
FROM users
  NATURAL JOIN transactions
  NATURAL JOIN transaction_items
WHERE username = "default";

SELECT *
FROM users
  NATURAL JOIN cart_items
WHERE username = "default";
