# cappillen.com

# enhancements
  - ~~https://stackoverflow.com/questions/45731445/particles-js-how-to-change-background-color-between-lines~~
  - https://codepen.io/metagrapher/pen/tgcLl
  - https://www.gradient-animator.com/
  - use cloudflare for cdn (net to the moon)

# Heroku cli
move to branch that we want to deploy to heroku
```bash
$ git checkout branch-to-deploy
```
use heroku to add a remote location to deploy our app
```bash
$ heroku git:remote -a app-name
```
push git repo normally but we will send to our heroku remote.
```bash
$ git push heroku branch-to-deploy:main
```
