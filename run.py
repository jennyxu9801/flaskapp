# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 18:55:37 2020

@author: x5021
"""

from flaskapp import create_app

app= create_app()

if __name__ == '__main__':
    app.run(debug=True)