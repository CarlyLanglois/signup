import webapp2
import re


# html boilerplate for the top of every page
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>Carly's Signup</title>
    <style type="text/css">
        .err {
            color: red;
        }
    </style>
</head>
<body>
    <h1>Signup for Carly</h1>
"""

# html boilerplate for the bottom of every page
page_footer = """
</body>
</html>
"""

# define a valid username
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)


class MainHandler(webapp2.RequestHandler):
    """ Handles requests coming in to '/' (the root of our site)
        e.g. www.signup.com/
    """

    def get(self):
        # if we have an error, make a <p> to display it
        err = self.request.get("err")
        err_element = "<p class='err'>" + err + "</p>" if err else ""

        username_form = """
        <form action="/welcome" method="post">
            <table>
                <tbody>
                    <tr>
                        <td>
                            <label for="username">Username</label>
                        </td>
                        <td>
                            <input name="username" type="text">
                        </td>
                        <td class="err">{}</td>
                    </tr>
                </tbody>
            </table>
            <input type="submit">
        </form>""".format(err_element)


        # combine all the pieces to build the content of our signup page
        signup_form = username_form

        signup_content = page_header + signup_form + page_footer
        self.response.write(signup_content)


    def post(self):
        # look inside the request to figure out what the user typed
        username = self.request.get("username")



        # if the user's username is not valid
        # TODO - invalid username

        # if the user's password and password-confirmation do not match
        # TODO - passwords dont match

        # if the user provides an email, but it's not a valid email.
        # TODO - invalid email


class Welcome (webapp2.RequestHandler):
    """ Handles requests coming in to '/welcome' (after successful signup)
        e.g. www.signup.com/welcome
    """

    def post(self):

        username = self.request.get("username")

        if not valid_username(username):
            name_err = "Please enter a valid username"
            self.redirect('/?err={}'.format(name_err))

        #build response content
        welcome_message = "Welcome, " + username + "!"
        welcome_content = page_header + welcome_message + page_footer
        self.response.write(welcome_content)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', Welcome)
], debug=True)
