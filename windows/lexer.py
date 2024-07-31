#  lexer.py
import ply.lex as lex

# Lista de tokens
tokens = (
    'COMMAND',
    'ARG',
    'PIPE',
    'REDIRECT_OUT',
    'REDIRECT_IN',
    'REDIRECT_APPEND',
    'BACKGROUND',
    'OPTION'
)

# Reglas simples para tokens
t_PIPE = r'\|'
t_REDIRECT_OUT = r'>'
t_REDIRECT_IN = r'<'
t_REDIRECT_APPEND = r'>>'
t_BACKGROUND = r'&'

# Caracteres a ignorar (espacios y tabulaciones)
t_ignore = ' \t'

# Diccionario de comandos y sus descripciones
# cambio: Se cambiaron algunos comandos que no 
# funcionaban por como realmente se usan en Windows CMD
commands = {
    'dir': 'Lista el contenido de un directorio.',
    'cd': 'Cambia el directorio actual.',
    'tree': 'Muestra el directorio actual.',
    'copy': 'Copia uno o más archivos en la dirección que tu elijas.',
    'move': 'Mueve el archivo concreto que quieras del lugar o carpeta en el que está a otra dirección que le digas. Es como copiar, pero sin dejar el archivo en su ubicación original.',
    'del': 'Elimina archivos o directorios.',
    'type': 'Te permite crear un archivo desde la propia ventana de comandos. Esto quiere decir que no sólo vas a crear un archivo, sino que también podrás escribir el texto que quieras en su interior.',
    'rename': 'Te permite cambiarle el nombre al archivo que consideres oportuno, e incluso incluyendo su extensión también puedes cambiarla. Aunque será un cambio como el que haces en la interfaz principal de Windows, sin conversión y sin que implique que va a funcionar bien con la nueva extensión.',
    'md': 'Crea una carpeta con el nombre que le asignes en la dirección en la que te encuentres en ese momento.',
    'cat': 'Concatena y muestra el contenido de archivos.',
    'echo': 'Muestra una línea de texto.',
    'find': 'Busca archivos en un directorio.',
    'grep': 'Busca patrones en el contenido de archivos.',
    'chmod': 'Cambia los permisos de archivos o directorios.',
    'chown': 'Cambia el propietario de archivos o directorios.',
}

# Regla para comandos
def t_COMMAND(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in commands:
        t.value = (t.value, commands[t.value])
    else:
        t.type = 'ARG'
    return t

# Regla para opciones de comandos
def t_OPTION(t):
    r'-[a-zA-Z0-9_]+'
    return t

# Regla para argumentos (incluyendo rutas y opciones)
def t_ARG(t):
    r'[^\s|><&]+'
    return t

# Regla para manejar saltos de línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Regla para manejar errores
def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}'")
    t.lexer.skip(1)

# Crear el lexer
lexer = lex.lex()

# Función para tokenizar una cadena de entrada
def tokenize(data):
    lexer.input(data)
    return list(lexer)
