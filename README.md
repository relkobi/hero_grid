python -m dung.game


pyinstaller --onefile --noconsole --name GridHero --add-data "dung/assets;dung/assets" dung/game.py
