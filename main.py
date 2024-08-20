from flask import Flask #Flask is a class inside flask module
app = Flask(__name__)#main app instance


@app.route("/")  #it is the default route for an app
def home():
    return 'Hello User'

app.run(debug= True)  # python app wil not run if you don't write this
# And writing debug = True ..the compiler will automaticaly load the changes So you don't need to run the app again and agian.
#Just save the file and reload the brouser