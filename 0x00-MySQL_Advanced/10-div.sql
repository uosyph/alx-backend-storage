-- Defines a function 'SafeDiv' that divides the first number by the second,
-- returning the result or 0 if the second number is 0

DELIMITER $$
DROP FUNCTION IF EXISTS SafeDiv;
CREATE FUNCTION SafeDiv(a INT, b INT)
RETURNS FLOAT
BEGIN
    RETURN (IF (b = 0, 0, a / b));
END
$$
DELIMITER ;
