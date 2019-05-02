#!/bin/sh

python manage.py migrate
npm install --dev
npm run dev
