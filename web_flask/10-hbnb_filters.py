#!/usr/bin/python3
"""A python script that starts a Web Flask App plus extra tweaks
"""


from flask import Flask
app = Flask(__name__)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
