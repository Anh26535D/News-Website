#!/bin/bash

flask seed

gunicorn -w 8 -b 0.0.0.0 'wsgi:run()'