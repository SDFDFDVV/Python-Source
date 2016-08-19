ver="1.0"
if [ "$1" = "--help" ]; then
  echo -e "
       \033[01;31m Cyber Telegram Bot \033[0m 
        \033[01;33m By\033[0m \033[01;30m@ThisIsPouria \033[0m
        \033[01;34m --help : Show This Msg \033[0m
        \033[01;34m --about : Show Bot Information \033[0m
        \033[01;34m --Update : Sync Bot With Master Repo \033[0m"


elif [ "$1" = "--about" ]; then
  echo -e "
         \033[01;31m Cyber Telegram Bot \033[0m 
        \033[01;33m By\033[0m \033[01;34m@ThisIsPouria \033[0m
              \033[01;30m $ver \033[0m
\033[01;31m A Fun Telegram Bot Written In Python\033[0m"



elif [ "$1" = "install" ]; then
  sudo pip install pyTelegramBotAPI
  sudo pip install telebot
  sudo pip install logging
  sudo apt-get install python2.7
  git clone https://github.com/PouriaDev/python-telegram-bot.git
  cd python-telegram-bot


elif [ "$1" = "fix" ]; then
  cd $HOME
  sudo pip install pyTelegramBotAPI
  git clone https://github.com/eternnoir/pyTelegramBotAPI.git
  cd pyTelegramBotAPI
  sudo python setup.py install
  sudo pip install pytelegrambotapi --upgrade
  cd $HOME
  cd python-telegram-bot


elif [ "$1" = "--Update" ]; then
  git pull
  echo -e "\033[01;31m Bot Successful Update \033[0m"
else
  echo -e "
        \033[01;31m Cyber Telegram Bot \033[0m 
        \033[01;33m By\033[0m \033[01;34m@ThisIsPouria \033[0m
              \033[01;30m $ver \033[0m"

  while true; do
	nohup python2.7 bot.py
	sleep 0.5
  done
fi
