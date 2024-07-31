
import os
import subprocess
from flask import Flask, request, render_template
from parserpy import parser, execute_command, p_command, parse_and_execute
# Initialize Flask app
app = Flask(__name__)

# Global variable to track the current directory
current_directory = os.getcwd()


# Route for the Flask app
@app.route('/', methods=['GET', 'POST'])
def index():
    output = ''
    error = ''
    if request.method == 'POST':
        commands = request.form['commands']
        if not commands.strip():
            error = "Error: La cadena de comandos está vacía."
        else:
            try:
                output = parse_and_execute(commands)
            except Exception as e:
                error = f"Error: {str(e)}"
    return render_template('index.html', output=output, error=error)

if __name__ == '__main__':
    app.run(debug=True)
