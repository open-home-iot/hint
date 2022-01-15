#!/usr/bin/env osascript
--
--osascript -e 'tell app "Terminal"
--  do script "cd ~/repos/hint; workon hint; ./manage.py runserver"
--  do script "cd ~/repos/hint/frontend; ng build --watch=true --outputPath=/Users/mansthornvik/repos/hint/backend/static/ang"
--end tell'

on run scriptpath
  tell application "Terminal"
    my makeTab()
    do script "cd " & scriptpath & "/.. && workon hint && ./manage.py runserver" in front window
    my makeTab()
    do script "cd " & scriptpath & "/../frontend && ng build --watch=true --outputPath=" & scriptpath & "/../backend/static/ang" in front window
  end tell
end run

on makeTab()
  tell application "System Events" to keystroke "t" using {command down}
end makeTab
