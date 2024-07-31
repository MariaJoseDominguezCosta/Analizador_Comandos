# parserpy.py
import ply.yacc as yacc
from lexer import tokens, commands
import subprocess
import os

def p_command_list(p):
    '''command_list : command
                    | command_list PIPE command'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + [('PIPE', '|')] + p[3]

def p_command(p):
    '''command : COMMAND
                | COMMAND options
                | COMMAND options args
                | COMMAND args'''
    p[0] = [('COMMAND', p[1])]
    if len(p) > 2:
        p[0].extend(p[2])
    if len(p) > 3:
        p[0].extend(p[3])

def p_options(p):
    '''options : OPTION
                | options OPTION'''
    if len(p) == 2:
        p[0] = [('OPTION', p[1])]
    else:
        p[0] = p[1] + [('OPTION', p[2])]

def p_args(p):
    '''args : ARG
            | args ARG'''
    if len(p) == 2:
        p[0] = [('ARG', p[1])]
    else:
        p[0] = p[1] + [('ARG', p[2])]

def p_redirects(p):
    '''redirects : redirect
                | redirects redirect'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_redirect(p):
    '''redirect : REDIRECT_OUT ARG
                | REDIRECT_IN ARG
                | REDIRECT_APPEND ARG'''
    p[0] = (p[1], p[2])

def p_error(p):
    print(f"Syntax error at '{p.value}'")

parser = yacc.yacc()

# Function to execute commands with the current directory context
def execute_command(command):
    global current_directory
    try:
        result = subprocess.run(command, capture_output=True, text=True, shell=True, cwd=current_directory)
        return result.stdout + result.stderr
    except Exception as e:
        return str(e)
# Function to handle help command
def show_help():
    help_message = "Lista de comandos disponibles:\n"
    for command, description in commands.items():
        help_message += f"{command}: {description}\n"
    return help_message

# Modification in parse_and_execute to include 'help' and 'cd'
def parse_and_execute(input_string):
    global current_directory

    if input_string.strip() == 'help':
        return show_help()

    parsed = parser.parse(input_string)
    if not parsed:
        return "Error: No se pudo analizar el comando."

    if parsed[0][0] == 'COMMAND' and parsed[0][1][0] == 'cd':
        # Execute the 'cd' command
        path = parsed[1][1] if len(parsed) > 1 else None
        if path:
            return change_directory(path)
        else:
            return "Error: Falta el argumento para el comando 'cd'."

    commands = []
    current_command = []
    for token in parsed:
        if token[0] == 'PIPE':
            commands.append(' '.join(current_command))
            current_command = []
        else:
            if isinstance(token[1], tuple):
                current_command.append(token[1][0])
            else:
                current_command.append(token[1])
    commands.append(' '.join(current_command))

    output = ""
    for command in commands:
        output += f"$ {command}\n"
        output += execute_command(command)
        output += "\n"

    return output.strip()

# Function to change the directory and update the global state
def change_directory(path):
    global current_directory
    try:
        os.chdir(path)
        current_directory = os.getcwd()
        return f"Directorio cambiado a: {current_directory}"
    except FileNotFoundError:
        return f"Error: No se encontró el directorio: {path}"
    except NotADirectoryError:
        return f"Error: No es un directorio: {path}"
    except PermissionError:
        return f"Error: Permiso denegado para acceder a: {path}"
    except Exception as e:
        return f"Error: {str(e)}"
