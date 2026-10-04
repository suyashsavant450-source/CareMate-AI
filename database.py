import sqlite3
import os
import hashlib
import secrets


DB_PATH = os.path.join("data", "caremate.db")


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_connection():

    os.makedirs("data", exist_ok=True)

    connection = sqlite3.connect(
        DB_PATH,
        check_same_thread=False
    )

    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


# =========================================================
# PASSWORD SECURITY
# =========================================================

def hash_password(password):

    salt = secrets.token_hex(16)

    password_hash = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        100000
    ).hex()

    return f"{salt}${password_hash}"


def verify_password(password, stored_password):

    try:

        salt, stored_hash = stored_password.split("$")

        password_hash = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt.encode("utf-8"),
            100000
        ).hex()

        return secrets.compare_digest(
            password_hash,
            stored_hash
        )

    except Exception:

        return False


# =========================================================
# DATABASE MIGRATION HELPER
# =========================================================

def add_missing_columns(cursor, table_name, columns):

    cursor.execute(
        f"PRAGMA table_info({table_name})"
    )

    existing_columns = {
        row["name"]
        for row in cursor.fetchall()
    }

    for column_name, column_type in columns.items():

        if column_name not in existing_columns:

            cursor.execute(
                f"""
                ALTER TABLE {table_name}
                ADD COLUMN {column_name} {column_type}
                """
            )


# =========================================================
# INITIALIZE DATABASE
# =========================================================

def init_database():

    connection = get_connection()
    cursor = connection.cursor()

    # =====================================================
    # USERS
    # =====================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    add_missing_columns(
        cursor,
        "users",
        {
            "phone": "TEXT",
            "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
            "date_of_birth": "TEXT",
            "gender": "TEXT",
            "blood_group": "TEXT",
            "height": "REAL",
            "weight": "REAL",
            "allergies": "TEXT",
            "health_conditions": "TEXT",
            "emergency_contact_name": "TEXT",
            "emergency_contact_phone": "TEXT"
        }
    )

    # =====================================================
    # MEDICAL REPORTS
    # =====================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medical_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            file_name TEXT,
            report_text TEXT,
            simplified_report TEXT,
            uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(user_id)
            REFERENCES users(id)
            ON DELETE CASCADE
        )
    """)

    add_missing_columns(
        cursor,
        "medical_reports",
        {
            "file_name": "TEXT",
            "report_text": "TEXT",
            "simplified_report": "TEXT",
            "uploaded_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
        }
    )

    # =====================================================
    # MEDICINES
    # =====================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medicines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            medicine_name TEXT NOT NULL,
            dosage TEXT,
            reminder_time TEXT,
            frequency TEXT,
            notes TEXT,
            active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(user_id)
            REFERENCES users(id)
            ON DELETE CASCADE
        )
    """)

    add_missing_columns(
        cursor,
        "medicines",
        {
            "dosage": "TEXT",
            "reminder_time": "TEXT",
            "frequency": "TEXT",
            "notes": "TEXT",
            "active": "INTEGER DEFAULT 1",
            "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
        }
    )

    # =====================================================
    # REMINDERS
    # =====================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            reminder_type TEXT NOT NULL,
            title TEXT NOT NULL,
            message TEXT,
            reminder_time TEXT,
            repeat_type TEXT,
            related_medicine_id INTEGER,
            sender_id INTEGER,
            active INTEGER DEFAULT 1,
            is_read INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(user_id)
            REFERENCES users(id)
            ON DELETE CASCADE
        )
    """)

    add_missing_columns(
        cursor,
        "reminders",
        {
            "reminder_type": "TEXT",
            "title": "TEXT",
            "message": "TEXT",
            "reminder_time": "TEXT",
            "repeat_type": "TEXT",
            "related_medicine_id": "INTEGER",
            "sender_id": "INTEGER",
            "active": "INTEGER DEFAULT 1",
            "is_read": "INTEGER DEFAULT 0",
            "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
        }
    )

    # =====================================================
    # MEDICINE LOGS
    # =====================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS medicine_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            medicine_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            scheduled_time TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            taken_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(medicine_id)
            REFERENCES medicines(id)
            ON DELETE CASCADE,

            FOREIGN KEY(user_id)
            REFERENCES users(id)
            ON DELETE CASCADE
        )
    """)

    add_missing_columns(
        cursor,
        "medicine_logs",
        {
            "scheduled_time": "TEXT",
            "status": "TEXT DEFAULT 'pending'",
            "taken_at": "TIMESTAMP",
            "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
        }
    )

    # =====================================================
    # HEALTH TRACKING
    # =====================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS health_tracking (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            water_intake REAL DEFAULT 0,
            sleep_hours REAL DEFAULT 0,
            exercise_minutes INTEGER DEFAULT 0,
            tracking_date TEXT,

            FOREIGN KEY(user_id)
            REFERENCES users(id)
            ON DELETE CASCADE
        )
    """)

    add_missing_columns(
        cursor,
        "health_tracking",
        {
            "water_intake": "REAL DEFAULT 0",
            "sleep_hours": "REAL DEFAULT 0",
            "exercise_minutes": "INTEGER DEFAULT 0",
            "tracking_date": "TEXT"
        }
    )

    # =====================================================
    # CAREGIVERS
    # =====================================================

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS caregivers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            patient_id INTEGER NOT NULL,
            caregiver_user_id INTEGER,

            caregiver_name TEXT,
            caregiver_phone TEXT,
            caregiver_email TEXT,
            relationship TEXT,

            can_view_reports INTEGER DEFAULT 1,
            can_view_medicines INTEGER DEFAULT 1,
            can_view_progress INTEGER DEFAULT 1,
            can_view_alerts INTEGER DEFAULT 1,
            can_send_reminders INTEGER DEFAULT 1,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(patient_id)
            REFERENCES users(id)
            ON DELETE CASCADE,

            FOREIGN KEY(caregiver_user_id)
            REFERENCES users(id)
            ON DELETE CASCADE
        )
    """)

    add_missing_columns(
        cursor,
        "caregivers",
        {
            "caregiver_user_id": "INTEGER",
            "caregiver_name": "TEXT",
            "caregiver_phone": "TEXT",
            "caregiver_email": "TEXT",
            "relationship": "TEXT",
            "can_view_reports": "INTEGER DEFAULT 1",
            "can_view_medicines": "INTEGER DEFAULT 1",
            "can_view_progress": "INTEGER DEFAULT 1",
            "can_view_alerts": "INTEGER DEFAULT 1",
            "can_send_reminders": "INTEGER DEFAULT 1",
            "created_at": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
        }
    )

    connection.commit()
    connection.close()


# =========================================================
# USER FUNCTIONS
# =========================================================

def create_user(name, email, phone, password):

    connection = get_connection()
    cursor = connection.cursor()

    password_hash = hash_password(password)

    try:

        cursor.execute("""
            INSERT INTO users
            (name, email, phone, password_hash)
            VALUES (?, ?, ?, ?)
        """, (
            name.strip(),
            email.strip().lower(),
            phone.strip(),
            password_hash
        ))

        connection.commit()

        user_id = cursor.lastrowid

        connection.close()

        return (
            True,
            user_id,
            "Account created successfully."
        )

    except sqlite3.IntegrityError as error:

        connection.close()

        message = str(error).lower()

        if "email" in message:
            return False, None, "Email already registered."

        if "phone" in message:
            return False, None, "Phone number already registered."

        return False, None, "Account could not be created."


def authenticate_user(email, password):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email = ?",
        (email.strip().lower(),)
    )

    user = cursor.fetchone()

    connection.close()

    if user is None:
        return None

    if verify_password(
        password,
        user["password_hash"]
    ):
        return dict(user)

    return None


# =========================================================
# GET USER
# =========================================================

def get_user_by_id(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            name,
            email,
            phone,
            date_of_birth,
            gender,
            blood_group,
            height,
            weight,
            allergies,
            health_conditions,
            emergency_contact_name,
            emergency_contact_phone,
            created_at
        FROM users
        WHERE id = ?
    """, (user_id,))

    user = cursor.fetchone()

    connection.close()

    return dict(user) if user else None


def find_user_by_email_or_phone(identifier):

    connection = get_connection()
    cursor = connection.cursor()

    identifier = identifier.strip()

    cursor.execute("""
        SELECT id, name, email, phone
        FROM users
        WHERE email = ?
           OR phone = ?
    """, (
        identifier.lower(),
        identifier
    ))

    user = cursor.fetchone()

    connection.close()

    return dict(user) if user else None


# =========================================================
# UPDATE USER PROFILE
# =========================================================

def update_user_profile(
    user_id,
    name,
    email,
    phone,
    date_of_birth="",
    gender="",
    blood_group="",
    height=None,
    weight=None,
    allergies="",
    health_conditions="",
    emergency_contact_name="",
    emergency_contact_phone=""
):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute("""
            UPDATE users
            SET
                name = ?,
                email = ?,
                phone = ?,
                date_of_birth = ?,
                gender = ?,
                blood_group = ?,
                height = ?,
                weight = ?,
                allergies = ?,
                health_conditions = ?,
                emergency_contact_name = ?,
                emergency_contact_phone = ?
            WHERE id = ?
        """, (
            name.strip(),
            email.strip().lower(),
            phone.strip(),
            date_of_birth.strip(),
            gender.strip(),
            blood_group.strip(),
            height,
            weight,
            allergies.strip(),
            health_conditions.strip(),
            emergency_contact_name.strip(),
            emergency_contact_phone.strip(),
            user_id
        ))

        connection.commit()

        return True, "Profile updated successfully."

    except sqlite3.IntegrityError as error:

        connection.rollback()

        message = str(error).lower()

        if "email" in message:
            return False, "Email already registered."

        if "phone" in message:
            return False, "Phone number already registered."

        return False, "Profile could not be updated."

    except Exception as error:

        connection.rollback()

        return False, f"Profile update failed: {error}"

    finally:

        connection.close()


# =========================================================
# FORGOT PASSWORD
# =========================================================

def reset_password(email, phone, new_password):

    email = email.strip().lower()
    phone = phone.strip()

    if not email or not phone:
        return False, "Email and phone number are required."

    if not new_password:
        return False, "New password is required."

    if len(new_password) < 6:
        return False, "Password must contain at least 6 characters."

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute("""
            SELECT id
            FROM users
            WHERE email = ?
              AND phone = ?
        """, (
            email,
            phone
        ))

        user = cursor.fetchone()

        if user is None:
            return (
                False,
                "Email and phone number do not match."
            )

        password_hash = hash_password(
            new_password
        )

        cursor.execute("""
            UPDATE users
            SET password_hash = ?
            WHERE id = ?
        """, (
            password_hash,
            user["id"]
        ))

        connection.commit()

        return True, "Password reset successfully."

    except Exception as error:

        connection.rollback()

        return False, f"Password reset failed: {error}"

    finally:

        connection.close()


# =========================================================
# CHANGE PASSWORD
# =========================================================

def change_password(
    user_id,
    current_password,
    new_password
):

    if not current_password:
        return False, "Current password is required."

    if not new_password:
        return False, "New password is required."

    if len(new_password) < 6:
        return (
            False,
            "New password must contain at least 6 characters."
        )

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute("""
            SELECT password_hash
            FROM users
            WHERE id = ?
        """, (user_id,))

        user = cursor.fetchone()

        if user is None:
            return False, "User account not found."

        if not verify_password(
            current_password,
            user["password_hash"]
        ):
            return False, "Current password is incorrect."

        new_password_hash = hash_password(
            new_password
        )

        cursor.execute("""
            UPDATE users
            SET password_hash = ?
            WHERE id = ?
        """, (
            new_password_hash,
            user_id
        ))

        connection.commit()

        return True, "Password changed successfully."

    except Exception as error:

        connection.rollback()

        return False, f"Password change failed: {error}"

    finally:

        connection.close()


# =========================================================
# MEDICAL REPORTS
# =========================================================

def save_medical_report(
    user_id,
    file_name,
    report_text,
    simplified_report
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO medical_reports
        (
            user_id,
            file_name,
            report_text,
            simplified_report
        )
        VALUES (?, ?, ?, ?)
    """, (
        user_id,
        file_name,
        report_text,
        simplified_report
    ))

    connection.commit()

    report_id = cursor.lastrowid

    connection.close()

    return report_id


def get_user_reports(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM medical_reports
        WHERE user_id = ?
        ORDER BY uploaded_at DESC
    """, (user_id,))

    reports = cursor.fetchall()

    connection.close()

    return [dict(row) for row in reports]


def get_patient_reports(patient_id):

    return get_user_reports(patient_id)


# =========================================================
# MEDICINES
# =========================================================

def add_medicine(
    user_id,
    medicine_name,
    dosage="",
    reminder_time=None,
    frequency="Once daily",
    notes=""
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO medicines
        (
            user_id,
            medicine_name,
            dosage,
            reminder_time,
            frequency,
            notes
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        medicine_name.strip(),
        dosage.strip(),
        reminder_time,
        frequency,
        notes.strip()
    ))

    connection.commit()

    medicine_id = cursor.lastrowid

    connection.close()

    return medicine_id


def get_user_medicines(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM medicines
        WHERE user_id = ?
          AND active = 1
        ORDER BY reminder_time
    """, (user_id,))

    medicines = cursor.fetchall()

    connection.close()

    return [dict(row) for row in medicines]


def get_patient_medicines(patient_id):

    return get_user_medicines(patient_id)


def deactivate_medicine(medicine_id, user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE medicines
        SET active = 0
        WHERE id = ?
          AND user_id = ?
    """, (
        medicine_id,
        user_id
    ))

    connection.commit()
    connection.close()


# =========================================================
# MEDICINE LOGS
# =========================================================

def create_medicine_log(
    medicine_id,
    user_id,
    scheduled_time
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO medicine_logs
        (
            medicine_id,
            user_id,
            scheduled_time
        )
        VALUES (?, ?, ?)
    """, (
        medicine_id,
        user_id,
        scheduled_time
    ))

    connection.commit()

    log_id = cursor.lastrowid

    connection.close()

    return log_id


def mark_medicine_taken(log_id, user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE medicine_logs
        SET
            status = 'taken',
            taken_at = CURRENT_TIMESTAMP
        WHERE id = ?
          AND user_id = ?
    """, (
        log_id,
        user_id
    ))

    connection.commit()
    connection.close()


def mark_medicine_missed(log_id, user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE medicine_logs
        SET status = 'missed'
        WHERE id = ?
          AND user_id = ?
    """, (
        log_id,
        user_id
    ))

    connection.commit()
    connection.close()


def get_medicine_logs(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            medicine_logs.*,
            medicines.medicine_name,
            medicines.dosage
        FROM medicine_logs
        JOIN medicines
          ON medicine_logs.medicine_id = medicines.id
        WHERE medicine_logs.user_id = ?
        ORDER BY medicine_logs.scheduled_time DESC
    """, (user_id,))

    logs = cursor.fetchall()

    connection.close()

    return [dict(row) for row in logs]


def get_patient_medicine_logs(patient_id):

    return get_medicine_logs(patient_id)


# =========================================================
# REMINDERS
# =========================================================

def create_reminder(
    user_id,
    reminder_type,
    title,
    message="",
    reminder_time=None,
    repeat_type=None,
    related_medicine_id=None,
    sender_id=None
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO reminders
        (
            user_id,
            reminder_type,
            title,
            message,
            reminder_time,
            repeat_type,
            related_medicine_id,
            sender_id
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        reminder_type,
        title,
        message,
        reminder_time,
        repeat_type,
        related_medicine_id,
        sender_id
    ))

    connection.commit()

    reminder_id = cursor.lastrowid

    connection.close()

    return reminder_id


def add_reminder(
    user_id,
    title,
    message="",
    reminder_type="general",
    reminder_time=None,
    repeat_type="Once",
    related_medicine_id=None,
    sender_id=None
):

    connection = get_connection()
    cursor = connection.cursor()

    try:

        cursor.execute("""
            INSERT INTO reminders
            (
                user_id,
                reminder_type,
                title,
                message,
                reminder_time,
                repeat_type,
                related_medicine_id,
                sender_id,
                active,
                is_read
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1, 0)
        """, (
            user_id,
            reminder_type,
            title.strip(),
            message.strip(),
            reminder_time,
            repeat_type,
            related_medicine_id,
            sender_id
        ))

        connection.commit()

        reminder_id = cursor.lastrowid

        return reminder_id

    except Exception:

        connection.rollback()
        raise

    finally:

        connection.close()


def get_user_reminders(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            reminders.*,
            sender.name AS sender_name,
            caregivers.relationship AS sender_relationship

        FROM reminders

        LEFT JOIN users AS sender
          ON reminders.sender_id = sender.id

        LEFT JOIN caregivers
          ON caregivers.patient_id = reminders.user_id
         AND caregivers.caregiver_user_id = reminders.sender_id

        WHERE reminders.user_id = ?
          AND reminders.active = 1

        ORDER BY reminders.created_at DESC
    """, (user_id,))

    reminders = cursor.fetchall()

    connection.close()

    return [dict(row) for row in reminders]


def mark_reminder_read(reminder_id, user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE reminders
        SET is_read = 1
        WHERE id = ?
          AND user_id = ?
    """, (
        reminder_id,
        user_id
    ))

    connection.commit()
    connection.close()


def delete_reminder(reminder_id, user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM reminders
        WHERE id = ?
          AND user_id = ?
    """, (
        reminder_id,
        user_id
    ))

    connection.commit()
    connection.close()


# =========================================================
# HEALTH TRACKING
# =========================================================

def save_health_tracking(
    user_id,
    water_intake,
    sleep_hours,
    exercise_minutes,
    tracking_date
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO health_tracking
        (
            user_id,
            water_intake,
            sleep_hours,
            exercise_minutes,
            tracking_date
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        user_id,
        water_intake,
        sleep_hours,
        exercise_minutes,
        tracking_date
    ))

    connection.commit()

    tracking_id = cursor.lastrowid

    connection.close()

    return tracking_id


def get_health_tracking(user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT *
        FROM health_tracking
        WHERE user_id = ?
        ORDER BY tracking_date DESC
    """, (user_id,))

    records = cursor.fetchall()

    connection.close()

    return [dict(row) for row in records]


def get_patient_health_tracking(patient_id):

    return get_health_tracking(patient_id)


# =========================================================
# CAREGIVER
# =========================================================

def add_caregiver(
    patient_id,
    caregiver_name="",
    caregiver_phone="",
    caregiver_email="",
    relationship="",
    caregiver_user_id=None,
    can_view_reports=True,
    can_view_medicines=True,
    can_view_progress=True,
    can_view_alerts=True,
    can_send_reminders=True
):

    connection = get_connection()
    cursor = connection.cursor()

    if caregiver_user_id is not None:

        cursor.execute("""
            SELECT id
            FROM caregivers
            WHERE patient_id = ?
              AND caregiver_user_id = ?
        """, (
            patient_id,
            caregiver_user_id
        ))

        existing = cursor.fetchone()

        if existing:

            connection.close()

            return existing["id"]

    cursor.execute("""
        INSERT INTO caregivers
        (
            patient_id,
            caregiver_user_id,
            caregiver_name,
            caregiver_phone,
            caregiver_email,
            relationship,
            can_view_reports,
            can_view_medicines,
            can_view_progress,
            can_view_alerts,
            can_send_reminders
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        patient_id,
        caregiver_user_id,
        caregiver_name.strip(),
        caregiver_phone.strip(),
        caregiver_email.strip(),
        relationship.strip(),
        int(can_view_reports),
        int(can_view_medicines),
        int(can_view_progress),
        int(can_view_alerts),
        int(can_send_reminders)
    ))

    connection.commit()

    caregiver_id = cursor.lastrowid

    connection.close()

    return caregiver_id


def get_caregivers(patient_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            caregivers.*,
            users.name AS caregiver_user_name,
            users.email AS caregiver_user_email,
            users.phone AS caregiver_user_phone

        FROM caregivers

        LEFT JOIN users
          ON caregivers.caregiver_user_id = users.id

        WHERE caregivers.patient_id = ?

        ORDER BY caregivers.created_at DESC
    """, (patient_id,))

    caregivers = cursor.fetchall()

    connection.close()

    return [dict(row) for row in caregivers]


def get_monitored_patients(caregiver_user_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            caregivers.*,

            users.id AS patient_user_id,
            users.name AS patient_name,
            users.email AS patient_email,
            users.phone AS patient_phone

        FROM caregivers

        JOIN users
          ON caregivers.patient_id = users.id

        WHERE caregivers.caregiver_user_id = ?

        ORDER BY users.name
    """, (caregiver_user_id,))

    patients = cursor.fetchall()

    connection.close()

    return [dict(row) for row in patients]