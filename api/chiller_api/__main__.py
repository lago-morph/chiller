#!/usr/bin/env python3

import connexion
import os

from chiller_api import initialize_application

# This is run when we "execute" the module.
# For instance, when in the parent directory, we type 
#   python3 -m chiller_api

def main():
    conapp = initialize_application('./swagger/')
    conapp.run(port=8080)


if __name__ == '__main__':
    main()
