-- Create a 'users' table with a column for country using the ENUM data type

CREATE TABLE IF NOT EXISTS users (
    id int NOT NULL AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255),
    PRIMARY KEY (id),
    country ENUM('US', 'CO', 'TN') DEFAULT 'US' NOT NULL
);
