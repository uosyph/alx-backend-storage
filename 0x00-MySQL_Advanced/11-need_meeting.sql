-- Creates a view 'need_meeting' that displays all students
-- with a score below 80 (strict) and either no 'last_meeting' or a gap of more than 1 month

DROP VIEW IF EXISTS need_meeting;
CREATE VIEW need_meeting AS
SELECT name FROM students 
WHERE score < 80
AND (last_meeting IS NULL OR last_meeting < DATE_SUB(NOW(), INTERVAL 1 MONTH));
