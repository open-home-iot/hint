#! /bin/zsh

# First Terminal for running the django dev server
osascript -e 'tell app "Terminal"
  do script "
    source ~/.pyenv/versions/3.9.0/bin/virtualenvwrapper.sh &&
      workon hint &&
      cd ~/repos/hint &&
      python manage.py runserver
  "
end tell'

# Second Terminal to start watching front end for code changes and automatic
# re-compilation
osascript -e 'tell app "Terminal"
  do script "
    cd ~/repos/hint/frontend &&
      ng build --watch=true --outputPath=/Users/mansthornvik/repos/hint/backend/static/ang
  "
end tell'

docker run -d -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
docker run -d -it --rm --name redis -p 6379:6379 redis