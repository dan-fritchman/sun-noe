
.PHONY: push

push:
	# Mostly, remember to set ENV vars on Heroku
	bash envs.sh heroku
	git push heroku master
	git push github master


