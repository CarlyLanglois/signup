import webapp2


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

class MainHandler(webapp2.RequestHandler):
    """ Handles requests coming in to '/' (the root of our site)
        e.g. www.signup.com/
    """

    def get(self):

        signup_form = """
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
                    </tr>
                    <tr>
                        <td>
                            <label for="password">Password</label>
                        </td>
                        <td>
                            <input name="password" type="password">
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <label for="verify">Verify Password</label>
                        </td>
                        <td>
                            <input name="verify" type="password">
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <label for="email">Email (optional)</label>
                        </td>
                        <td>
                            <input name="email" type="email">
                        </td>
                    </tr>
                </tbody>
            </table>
            <input type="submit">
        </form>
        """
        # if we have an error, make a <p> to display it
        err = self.request.get("err")
        err_element = "<p class= 'err'>" + err + "</p>" if err else ""

        # combine all the pieces to build the content of our signup page
        signup_content = page_header + signup_form + err_element + page_footer
        self.response.write(signup_content)

class Welcome (webapp2.RequestHandler):
    """ Handles requests coming in to '/welcome' (after successful signup)
        e.g. www.signup.com/welcome
    """

    def post(self):
        # look inside the request to figure out what the user typed
        username = self.request.get("username")

        if username == "":
            no_name = "Please specify a username."
            self.redirect('/?err={}'.format(no_name))

        #build response content
        welcome_message = "Welcome, " + username + "!"
        welcome_content = page_header + welcome_message + page_footer
        self.response.write(welcome_content)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', Welcome)
], debug=True)
