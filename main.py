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

# define a valid password
PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

#define a valid email
EMAIL_RE = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)


class MainHandler(webapp2.RequestHandler):
    """ Handles requests coming in to '/' (the root of our site)
        e.g. www.signup.com/
    """
    def get(self):
        # if we have an error, display it
        err = self.request.get("err")
        err_element = "<td class='err'>" + err + "</td>" if err else ""

        err2 = self.request.get("err2")
        err_element2 = "<td class='err'>" + err2 + "</td>" if err2 else ""

        err3 = self.request.get("err3")
        err_element3 = "<td class='err'>" + err3 + "</td>" if err3 else ""

        err4 = self.request.get("err4")
        err_element4 = "<td class='err'>" + err4 + "</td>" if err4 else ""

        username_form = """
        <form action="/welcome" method="post">
            <table>
                <tbody>
                    <tr>
                        <td>
                            <label for="username">Username</label>
                        </td>
                        <td>
                            <input name="username" type="text" value="%(username)s">
                        </td>
                        {}
                    </tr>""".format(err_element)

        password_form = """
            <tr>
                <td>
                    <label for="password">Password</label>
                </td>
                <td>
                    <input name="password" type="password">
                </td>
                {}
            </tr>""".format(err_element2)

        verify_form = """
            <tr>
                <td>
                    <label for="verify">Verify</label>
                </td>
                <td>
                    <input name="verify" type="password">
                </td>
                {}
            </tr>""".format(err_element3)

        email_form = """
            <tr>
                <td>
                    <label for="email">Email</label>
                </td>
                <td>
                    <input name="email" type="email">
                </td>
                {}
            </tr>
                </tbody>
            </table>
            <input type="submit">
        </form>""".format(err_element4)

        username = self.request.get("username")

        # combine all the pieces to build the content of our signup page
        signup_form = username_form + password_form + verify_form + email_form

        signup_content = page_header + signup_form + page_footer
    
        self.response.out.write(signup_content % {"username": username})



class Welcome (webapp2.RequestHandler):
    """ Handles requests coming in to '/welcome' (after successful signup)
        e.g. www.signup.com/welcome
    """

    def post(self):

        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        name_err = "Please enter a valid username"
        pass_err = "Please enter a valid password"
        ver_err = "Passwords don't match"
        eml_err = "Your email is not valid"

        welcome_message = "Welcome, " + username + "!"
        welcome_content = page_header + welcome_message + page_footer

        if not valid_username(username):
            if not valid_password(password):
                if not valid_email(email):
                    self.redirect('/?err={0}&err2={1}&err4={2}'.format(name_err, pass_err, eml_err))
                if valid_email(email):
                    self.redirect('/?err={0}&err2={1}'.format(name_err, pass_err))
            elif ((valid_password(password)) and (password != verify)):
                if not valid_email(email):
                    self.redirect('/?err={0}&err3={1}&err4={2}'.format(name_err, ver_err, eml_err))
                if valid_email(email):
                    self.redirect('/?err={0}&err3={1}'.format(name_err, ver_err))
            elif ((valid_password(password)) and (password == verify)):
                if not valid_email(email):
                    self.redirect('/?err={0}&err4={1}'.format(name_err, eml_err))
                if valid_email(email):
                    self.redirect('/?err={}'.format(name_err))
        elif valid_username(username):
            if not valid_password(password):
                if not valid_email(email):
                    self.redirect('/?err2={0}&err4={1}'.format(pass_err, eml_err))
                if valid_email(email):
                    self.redirect('/?err2={}'.format(pass_err))
            elif ((valid_password(password)) and (password != verify)):
                if not valid_email(email):
                    self.redirect('/?err3={0}&err4={1}'.format(ver_err, eml_err))
                if valid_email(email):
                    self.redirect('/?err3={}'.format(ver_err))
            elif ((valid_password(password)) and (password == verify)):
                if not valid_email(email):
                    self.redirect('/?err4={}'.format(eml_err))
                if valid_email(email):
                    self.response.write(welcome_content)





app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', Welcome)
], debug=True)
