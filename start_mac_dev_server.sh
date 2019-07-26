#!/bin/sh

# First Terminal for running the django dev server
osascript -e 'tell app "Terminal"
  do script "
    source /Library/Frameworks/Python.framework/Versions/3.6/bin/virtualenvwrapper.sh &&
      workon hint &&
      cd PycharmProjects/hint &&
      python manage.py runserver
  "
end tell'

# Second Terminal to start watching front end for code changes and automatic
# re-compilation
osascript -e 'tell app "Terminal"
  do script "
    cd PycharmProjects/hint/frontend &&
      ng build --watch=true --outputPath=/Users/MTH/PycharmProjects/hint/backend/static/ang
  "
end tell'
