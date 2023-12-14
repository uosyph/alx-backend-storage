-- Creates an index 'idx_name_first' on the 'names' table
-- for optimizing searches based on the first letter of the 'name' column

CREATE INDEX idx_name_first
ON names(name(1));
