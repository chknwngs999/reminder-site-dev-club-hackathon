from flask import Flask, render_template, request
import pickle

app = Flask(__name__)

currentuser = ""
#multiple people using at once?
#duplication bug - same name elements not filtered, no way to change design/background stuff, login not secure, can't delete users?

file = open("save", "rb")
elementsByUser = pickle.load(file)
file.close()

@app.errorhandler(404)
def page_not_found(error):
  return render_template('error404.html'), 404

@app.route('/')
def home():
  global currentuser, elementsByUser
  
  file = open("save", "rb")
  elementsByUser = pickle.load(file)
  file.close()

  return render_template('main.html', elementsByUser=elementsByUser, currentuser=currentuser)
@app.route('/login/', methods=["get", "post"])
def login():
  global currentuser, elementsByUser
  
  file = open("save", "rb")
  elementsByUser = pickle.load(file)
  file.close()

  message = ''
  if request.method == 'POST':
    username = request.form.get('username')
    password = request.form.get('password')
    if username in elementsByUser:
      if elementsByUser[username]["password"] == password:
        currentuser = username
        message = "Successfully logged in!"
      else:
        message = "Incorrect password."
    else:
      message = "Username does not exist."

  return render_template('formlogin.html', message=message, currentuser=currentuser)
@app.route('/signup/', methods=["get", "post"])
def signup():
  global currentuser, elementsByUser

  message = ''
  if request.method == "POST":
    newuser = request.form.get("username")
    newpassword = request.form.get("password")
    if newuser in elementsByUser.keys():
      message = "This username is taken. Please try a different username or login "
    else:
      elementsByUser[newuser] = {
        "password": newpassword,
        "l0l": [], 
        "l1l": [],
        "l2l": []
      }
      message = "You have successfully signed up! Try logging in "
    file = open("save", "wb")
    pickle.dump(elementsByUser, file)
    file.close()

  file = open("save", "rb")
  elementsByUser = pickle.load(file)
  file.close()

  return render_template('formsignup.html', elementsByUser=elementsByUser, currentuser=currentuser, message=message)
@app.route('/logout')
def logout():
  global currentuser

  currentuser = ""

  return render_template("logout.html", currentuser=currentuser)

@app.route('/formadd/', methods=["get", "post"])
def formadd():
  global currentuser, elementsByUser

  message = ''
  if request.method == 'POST':
    location = request.form.get('level')
    newName = request.form.get('elementname')
    if location[0] == "0":
      location = location[1:]
      if location not in elementsByUser[currentuser]["l0l"]:
        elementsByUser[currentuser]["l0l"].append(newName)
        elementsByUser[currentuser]["l1l"].append([])
        elementsByUser[currentuser]["l2l"].append([[]])
        message = "Element successfully added."
      else:
        message = "You already have an element with the same name."
    elif location[0] == "1":
      location = location[1:]
      dex = elementsByUser[currentuser]["l0l"].index(location)
      if location not in elementsByUser[currentuser]["l1l"][dex]:
        elementsByUser[currentuser]["l1l"][dex].append(newName)
        elementsByUser[currentuser]["l2l"][dex].append([])
        message = "Element successfully added."
      else:
        message = "You already have an element with the same name."
    elif location[0] == "2":
      location = location[1:]
      for i in range(len(location)):
        if location[i:i+2] == "%%":
          zeroloc = int(location[:i])
          location = location[i+2:]
          break
      for j in range(len(elementsByUser[currentuser]["l1l"][zeroloc])):
        if elementsByUser[currentuser]["l1l"][zeroloc][j] == location:
          if location not in elementsByUser[currentuser]["l2l"][zeroloc][j]:
            elementsByUser[currentuser]["l2l"][zeroloc][j].append(newName)
          else:
            message = "You already have an element with the same name."
      message = "Element successfully added."
    file = open("save", "wb")
    pickle.dump(elementsByUser, file)
    file.close()
  
  file = open("save", "rb")
  elementsByUser = pickle.load(file)
  file.close()

  return render_template('formadd.html', elementsByUser=elementsByUser, currentuser=currentuser, message=message)
@app.route('/formdelete/', methods=["get", "post"])
def formdelete():
  global currentuser, elementsByUser

  message = ''
  if request.method == "POST":
    location = request.form.get('level')
    if location[0] == "0":
      location = location[1:]
      dex = elementsByUser[currentuser]["l0l"].index(location)
      elementsByUser[currentuser]["l0l"].remove(location)
      del elementsByUser[currentuser]["l1l"][dex]
      if elementsByUser[currentuser]["l2l"][dex]:
        del elementsByUser[currentuser]["l2l"][dex]
      message = "Element and all contained sub-elements have been deleted."
    elif location[0] == "1":
      location = location[1:]
      for i in range(len(location)):
        if location[i:i+2] == "%%":
          zeroloc = int(location[:i])
          location = location[i+2:]
          break
      dex = elementsByUser[currentuser]["l1l"][zeroloc].index(location)
      elementsByUser[currentuser]["l1l"][zeroloc].remove(location)
      if elementsByUser[currentuser]["l2l"][zeroloc][dex]:
        del elementsByUser[currentuser]["l2l"][zeroloc][dex]
      message = "Element and all contained sub-elements have been deleted."
    elif location[0] == "2":
      location = location[1:]
      for i in range(len(location)):
        if location[i:i+2] == "%%":
          zeroloc = int(location[:i])
          location = location[i+2:]
          break
      for j in range(len(location)):
        if location[j:j+2] == "%%":
          oneloc = int(location[:j])
          location = location[j+2:]
          break
      elementsByUser[currentuser]["l2l"][zeroloc][oneloc].remove(location)
      message = "Element has been deleted."
      
    file = open("save", "wb")
    pickle.dump(elementsByUser, file)
    file.close()

  file = open("save", "rb")
  elementsByUser = pickle.load(file)
  file.close()

  return render_template('formdelete.html', elementsByUser=elementsByUser, currentuser=currentuser, message=message)

# start the server with the 'run()' method
if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0')

#styling? - color settings if time allows

#sessions, color/background/text settings, fix login?https://hackersandslackers.com/flask-login-user-authentication/

#https://flask.palletsprojects.com/en/1.1.x/
#popup screen like gamepress.gg/grandorder/4-star-tier-li

#radio buttons: https://html5-tutorial.net/forms/radiobuttons/, https://html-shark.com/HTML/RadioButtons.htm, https://stackoverflow.com/questions/38258011/dynamic-radio-buttons-from-database-query-using-flask-and-wtforms
#Forms/WTForms: https://gist.github.com/doobeh/4667330, https://stackoverflow.com/questions/11556958/sending-data-from-html-form-to-a-python-script-in-flask, https://overiq.com/flask-101/form-handling-in-flask/
#html stuff: popup - https://www.w3schools.com/js/js_popup.asp; dropdown - https://www.w3schools.com/howto/howto_js_dropdown.asp
#pickle - https://stackoverflow.com/questions/31891286/keeping-the-data-of-a-variable-between-runs-of-code, https://www.datacamp.com/community/tutorials/pickle-python-tutorial#whatfor, https://www.geeksforgeeks.org/save-a-dictionary-to-a-file/#:~:text=Text%20Files,the%20dictionary%20into%20a%20string

#future - login fix, description, due date, calendar view/schedule based on importance, set themes/backgrounds