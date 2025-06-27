CREATE TABLE IF NOT EXISTS financelive.users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(100) NOT NULL UNIQUE,
    name_ VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    birth_date DATE NOT NULL,
    password_ VARCHAR(255) NOT NULL,
    income DECIMAL(10, 2) NOT NULL,  -- Ingreso mensual
    income_type VARCHAR(50) NOT NULL,  -- Tipo de ingreso (empleo, freelance, etc.)
    risk_profile VARCHAR(50) NOT NULL,  -- Perfil de riesgo (conservador, moderado, agresivo)
    country VARCHAR(50) NOT NULL,  -- País de residencia
    financial_goals TEXT,  -- Lista de metas financieras en formato JSON o string
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS financelive.transactions (
    transaction_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    transaction_type VARCHAR(50) NOT NULL,  -- Ingreso o gasto
    category VARCHAR(50),  -- Ejemplo: 'alimentación', 'transporte', etc.
    transaction_status VARCHAR(50) NOT NULL,  -- Estado de la transacción (pendiente, completada, cancelada)
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description VARCHAR(255),
    is_periodic BOOLEAN DEFAULT FALSE,  -- Si es ingreso periódico
    period_end_date DATE,  -- Fecha final del ingreso periódico (si aplica)
    CONSTRAINT fk_transactions_user FOREIGN KEY (user_id) REFERENCES financelive.users(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS financelive.financial_items (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    description_ VARCHAR(255) NOT NULL,
    interest_rate DECIMAL(5, 2),
    total_payment DECIMAL(10, 2),
    current_payment DECIMAL(10, 2),
    payment_date DATE,
    status_ BOOLEAN NOT NULL,  -- Si está pagado o activo
    item_type VARCHAR(50) NOT NULL,  -- 'deuda' o 'inversión'
    goal_date DATE,  -- Solo para inversiones
    final_amount DECIMAL(10, 2),  -- Solo para inversiones
    transaction_type VARCHAR(50) NOT NULL,  -- Ingreso o gasto
    category VARCHAR(50),  -- Ejemplo: 'alimentación', 'transporte', etc.
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  -- Fecha de la transacción
    description VARCHAR(255),  -- Descripción de la transacción
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_financial_items_user FOREIGN KEY (user_id) REFERENCES financelive.users(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS financelive.platforms (
    platform_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,  -- Nombre de la plataforma (e.g., Revolut, Binance)
    type VARCHAR(50) NOT NULL,  -- Tipo de plataforma (e.g., financiera, criptomonedas)
    available_in_countries TEXT,  -- Países donde está disponible (lista o JSON)
    api_integrations BOOLEAN NOT NULL,  -- Si aplica integración con API
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
CREATE TABLE IF NOT EXISTS financelive.notifications (
    notification_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    notification_type VARCHAR(50) NOT NULL,  -- Tipo de notificación (pago de cuenta, recordatorio)
    payment_type VARCHAR(50),  -- Tipo de pago (alquiler, servicios, suscripciones)
    amount DECIMAL(10, 2) NOT NULL,  -- Monto a pagar
    due_date DATE NOT NULL,  -- Fecha de vencimiento del pago
    reminder_date DATE NOT NULL,  -- Fecha del recordatorio (3 días antes)
    status VARCHAR(50) NOT NULL,  -- Estado de la notificación (enviado, pendiente)
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_notifications_user FOREIGN KEY (user_id) REFERENCES financelive.users(id) ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS financelive.investments (
    investment_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    investment_type VARCHAR(50) NOT NULL,  -- Ejemplo: 'acciones', 'bonos', 'ETF', 'criptomonedas'
    amount_invested DECIMAL(10, 2) NOT NULL,  -- Monto invertido
    investment_date DATE NOT NULL,  -- Fecha de la inversión
    current_value DECIMAL(10, 2),  -- Valor actual de la inversión
    predicted_value DECIMAL(10, 2),  -- Valor estimado según simulaciones
    platform VARCHAR(100),  -- Plataforma de inversión (e.g., Binance, eToro)
    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_investments_user FOREIGN KEY (user_id) REFERENCES financelive.users(id) ON DELETE CASCADE
);
