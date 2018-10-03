

.PHONY: push remotes 

remotes:
	# Maybe not necessary to push to Heroku anymore;
	# It has a GitHub web trigger set up. 
	git remote add github git@github.com:dfritchman/sun-noe.git
	git remote add heroku https://git.heroku.com/sun-noe.git
	
push:
	# Mostly, remember to set ENV vars on Heroku
	bash envs.sh heroku
	git push github master


