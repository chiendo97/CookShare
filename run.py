# run.py

import os
import logging

from app import create_app

config_name = 'development'
app = create_app(config_name)

if __name__ == '__main__':
    app.run()