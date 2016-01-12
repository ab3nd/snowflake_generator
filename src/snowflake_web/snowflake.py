from flask import Flask, url_for, render_template
import re
import flake_generator

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"
    
@app.route("/png/<user_string>")
def genPNG(user_string):
    #Strip out everything that's not a letter
    user_string = user_string.lower()
    user_string = re.sub("[^a-z]", "", user_string)
    #Cut off all but the first 20 characters
    user_string = user_string[:20]
    #Generate the snowflake
    flake_generator.single_flake_png("./static/", user_string)   
    #Get the url to it
    pic_url = url_for('static', filename='{0}.png'.format(user_string))
    return render_template('snowflake.html', img_path=pic_url, input_string=user_string)
    
if __name__ == "__main__":
    app.run(debug=True)
