uwsgi -s 127.0.0.1:4242 --module server --mount /=web:app
