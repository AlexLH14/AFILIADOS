import sqlite3

DB_PATH = "Afiliados.db"

def inicializar_db():
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS video_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id TEXT UNIQUE NOT NULL,
            timestamp DATETIME DEFAULT (datetime('now', 'localtime'))
        )
    ''')

    # Crear tabla de categorías
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS categorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT UNIQUE NOT NULL
            )
        ''')

    # Crear tabla de variantes de búsqueda
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS variantes_busqueda (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                variante TEXT NOT NULL,
                categoria_id INTEGER NOT NULL,
                FOREIGN KEY (categoria_id) REFERENCES categorias(id)
            )
        ''')

    # Crear tabla de productos
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                link TEXT UNIQUE NOT NULL,
                categoria_id INTEGER NOT NULL,
                FOREIGN KEY (categoria_id) REFERENCES categorias(id)
            )
        ''')

    # Crear tabla de comentarios
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS comentarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                comentario TEXT NOT NULL,
                producto_id INTEGER NOT NULL,
                video_log_id INTEGER NOT NULL,
                categoria_id INTEGER NOT NULL,
                timestamp DATETIME DEFAULT (datetime('now', 'localtime')),
                FOREIGN KEY (producto_id) REFERENCES productos(id),
                FOREIGN KEY (video_log_id) REFERENCES video_logs(id),
                FOREIGN KEY (categoria_id) REFERENCES categorias(id)
            )
        ''')



    conexion.commit()
    conexion.close()

def cargar_registro():
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()
    cursor.execute('SELECT video_id FROM video_logs')
    registros = [fila[0] for fila in cursor.fetchall()]
    conexion.close()
    return registros

def guardar_registro(video_id):
    """
    Guarda un video_id en la tabla video_logs y devuelve su ID de registro.
    """
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()
    try:
        cursor.execute('INSERT INTO video_logs (video_id) VALUES (?)', (video_id,))
        conexion.commit()
        log_id = cursor.lastrowid  # Obtiene el ID autoincremental del registro insertado
    except sqlite3.IntegrityError:
        # Si ya existe, obtenemos el ID del registro existente
        cursor.execute('SELECT id FROM video_logs WHERE video_id = ?', (video_id,))
        log_id = cursor.fetchone()[0]
    conexion.close()
    return log_id


def insertar_comentario(comentario, producto_id, video_log_id, categoria_id):
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()
    cursor.execute('''
        INSERT INTO comentarios (comentario, producto_id, video_log_id, categoria_id)
        VALUES (?, ?, ?, ?)
    ''', (comentario, producto_id, video_log_id, categoria_id))
    conexion.commit()
    conexion.close()


def obtener_comentarios():
    """
    Devuelve todos los comentarios registrados en la base de datos.
    """
    conexion = sqlite3.connect(DB_PATH)
    cursor = conexion.cursor()
    cursor.execute('''
        SELECT comentarios.id, comentarios.comentario, productos.link, categorias.nombre, video_logs.video_id, comentarios.timestamp
        FROM comentarios
        JOIN productos ON comentarios.producto_id = productos.id
        JOIN categorias ON comentarios.categoria_id = categorias.id
        JOIN video_logs ON comentarios.video_log_id = video_logs.id
    ''')
    comentarios = cursor.fetchall()
    conexion.close()
    return comentarios