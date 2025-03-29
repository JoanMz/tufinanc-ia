CREATE SCHEMA IF NOT EXISTS financelive;

CREATE TABLE IF NOT EXISTS financelive.users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(100) NOT NULL UNIQUE,
    name_ VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    birth_date DATE NOT NULL,
    password_ VARCHAR(255) NOT NULL,
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS financelive.debts (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    description_ VARCHAR(255) NOT NULL,
    interest_rate DECIMAL(5, 2) NOT NULL,
    total_payment DECIMAL(10, 2) NOT NULL,
    current_payment DECIMAL(10, 2) NOT NULL,
    payment_date DATE NOT NULL,
    status_ BOOLEAN NOT NULL,
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_debts_user FOREIGN KEY (user_id) REFERENCES financelive.users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS financelive.investments (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    status_ BOOLEAN NOT NULL,
    description_ VARCHAR(255) NOT NULL,
    interest_rate DECIMAL(5, 2),
    goal_date DATE,
    final_amount DECIMAL(10, 2),
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_investments_user FOREIGN KEY (user_id) REFERENCES financelive.users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS financelive.incomes (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    description_ VARCHAR(255) NOT NULL,
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_incomes_user FOREIGN KEY (user_id) REFERENCES financelive.users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS financelive.periodic_incomes (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    description_ VARCHAR(255) NOT NULL,
    status_ BOOLEAN NOT NULL,
    date_period DATE NOT NULL,
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_periodic_incomes_user FOREIGN KEY (user_id) REFERENCES financelive.users(id) ON DELETE CASCADE
);

