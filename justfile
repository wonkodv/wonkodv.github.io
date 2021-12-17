serve:
    kitty zola serve &>/dev/null &
    sleep 1
    firefox http://127.0.0.1:1111 &>/dev/null &

new:
    python new.py

build:
    zola build

push: build
    git add .
    git commit -m 'update'
    git push
