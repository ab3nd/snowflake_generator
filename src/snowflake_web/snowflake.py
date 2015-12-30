from flask import Flask
import re
import flake_generator

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"
    
@app.route("/png/<user_string>")
def genSVG(user_string):
    #Strip out everything that's not a letter
    user_string = user_string.lower()
    user_string = re.sub("[^a-z]", "", user_string)
    #Cut off all but the first 10 characters
    user_string = user_string[:10]
    #Generate the snowflake
    flake_generator.single_flake_png("./flakes/", user_string)   
    #Get the url to it
    #pic_url = url_for('flakes', filename='{0}.png'.format(user_string))
    #return "<html><head></head><body><img src=\"{0}\" alt=\"A snowflake\"></body></html>".format(pic_url)
    
    
if __name__ == "__main__":
    app.run(debug=True)
