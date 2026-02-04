import psycopg2
from psycopg2 import sql

# Conexión con la base de datos
conn = psycopg2.connect(
    dbname="financelive", user="your_username", password="your_password", host="localhost", port="5432"
)
cursor = conn.cursor()
#Recoger Información del Usuario
def obtener_perfil_usuario(user_id):
    # Pedir información básica del usuario
    name = input("¿Cuál es tu nombre completo? ")
    last_name = input("¿Cuál es tu apellido? ")
    email = input("¿Cuál es tu correo electrónico? ")
    birth_date = input("¿Cuál es tu fecha de nacimiento? (YYYY-MM-DD) ")
    country = input("¿En qué país vives? ")
    income = float(input("¿Cuál es tu ingreso mensual? "))
    income_type = input("¿De qué tipo es tu ingreso? (empleo, freelance, etc.) ")
    risk_profile = input("¿Cuál es tu perfil de riesgo? (conservador, moderado, agresivo) ")
    financial_goals = input("¿Cuáles son tus metas financieras? (Ejemplo: comprar casa, generar ingresos pasivos) ")

    # Insertar los datos en la base de datos
    query = """
    INSERT INTO financelive.users (name_, last_name, email, birth_date, country, income, income_type, risk_profile, financial_goals)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    RETURNING id;
    """
    cursor.execute(query, (name, last_name, email, birth_date, country, income, income_type, risk_profile, financial_goals))
    user_id = cursor.fetchone()[0]
    conn.commit()
    
    print(f"Perfil creado para {name} {last_name}. ID de usuario: {user_id}")
    return user_id
#Función para Registrar Transacciones (Ingresos y Gastos)
def registrar_transaccion(user_id):
    transaction_type = input("¿Es un ingreso o un gasto? ").lower()
    category = input("¿En qué categoría entra? (Ejemplo: alimentación, transporte) ")
    amount = float(input("¿Cuánto es el monto de la transacción? "))
    description = input("Describe la transacción: ")

    # Registrar la transacción en la base de datos
    query = """
    INSERT INTO financelive.transactions (user_id, amount, transaction_type, category, description)
    VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(query, (user_id, amount, transaction_type, category, description))
    conn.commit()

    print("Transacción registrada con éxito.")
#Función para Calcular Intereses (Simulación de Rendimiento)def calcular_intereses(principal, rate, time, compound=False):
    if compound:
        # Cálculo de interés compuesto
        amount = principal * (1 + rate / 100) ** time
    else:
        # Cálculo de interés simple
        amount = principal * (1 + rate / 100 * time)

    return amount
#Función para Gestionar Inversiones y Planes de Inversión
def registrar_inversion(user_id):
    investment_type = input("¿Qué tipo de inversión es? (acciones, bonos, ETF, criptomonedas) ")
    amount_invested = float(input("¿Cuánto invertirás? "))
    investment_date = input("¿En qué fecha realizarás la inversión? (YYYY-MM-DD) ")
    interest_rate = float(input("¿Cuál es la tasa de interés estimada? "))
    goal_date = input("¿Cuál es la fecha de objetivo para tu inversión? (YYYY-MM-DD) ")

    # Insertar inversión en la base de datos
    query = """
    INSERT INTO financelive.investments (user_id, investment_type, amount_invested, investment_date, interest_rate, goal_date)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (user_id, investment_type, amount_invested, investment_date, interest_rate, goal_date))
    conn.commit()

    print(f"Inversión de {investment_type} registrada con éxito.")
#Función de Notificaciones de Pago y Recordatorios
def registrar_notificacion(user_id):
    payment_type = input("¿De qué tipo es el pago? (alquiler, servicios, etc.) ")
    amount = float(input("¿Cuál es el monto a pagar? "))
    due_date = input("¿Cuál es la fecha de vencimiento del pago? (YYYY-MM-DD) ")
    reminder_date = input("¿Cuántos días antes del vencimiento quieres que te recuerde? ")

    # Insertar notificación
    query = """
    INSERT INTO financelive.notifications (user_id, notification_type, payment_type, amount, due_date, reminder_date, status)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(query, (user_id, 'recordatorio de pago', payment_type, amount, due_date, reminder_date, 'pendiente'))
    conn.commit()

    print("Notificación de pago registrada con éxito.")
#Función para Consultar Información Financiera y Sugerencias de Inversión
def consultar_inversiones(user_id):
    query = """
    SELECT investment_type, amount_invested, interest_rate, goal_date FROM financelive.investments
    WHERE user_id = %s;
    """
    cursor.execute(query, (user_id,))
    inversiones = cursor.fetchall()

    print("Tus inversiones actuales son:")
    for inversion in inversiones:
        print(f"Tipo: {inversion[0]}, Monto invertido: {inversion[1]}, Tasa de interés: {inversion[2]}, Fecha de objetivo: {inversion[3]}")
#Función Principal del Asistente
def asistente_financiero():
    user_id = obtener_perfil_usuario(None)  # Crear perfil de usuario
    while True:
        print("\n¿Qué te gustaría hacer?")
        print("1. Registrar una transacción")
        print("2. Calcular el rendimiento de una inversión")
        print("3. Registrar una inversión")
        print("4. Ver mis inversiones")
        print("5. Registrar una notificación de pago")
        print("6. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            registrar_transaccion(user_id)
        elif opcion == '2':
            principal = float(input("Monto invertido: "))
            rate = float(input("Tasa de interés: "))
            time = int(input("Tiempo en años: "))
            print("Interés simple:", calcular_intereses(principal, rate, time))
            print("Interés compuesto:", calcular_intereses(principal, rate, time, compound=True))
        elif opcion == '3':
            registrar_inversion(user_id)
        elif opcion == '4':
            consultar_inversiones(user_id)
        elif opcion == '5':
            registrar_notificacion(user_id)
        elif opcion == '6':
            break
        else:
            print("Opción no válida.")
