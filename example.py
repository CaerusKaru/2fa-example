'''
example.py -- use case for two-factor authentication (2FA), demonstrated in Python
              This script is a CGI-script, meant to be run on a webserver
              Necessary dependencies: pyotp (can be retrieved using pip)
              Credit: Patrick Nielsen for much of the startup code and creators of
                      pyotp for making this process so dead simple
Created by: Adam Plumer
Date created: Dec 12, 2016
'''

'''
Discussion:
This script demonstrates the ease of use in adopting a two-factor authentication system
in Python. The fact that it took an undergraduate roughly two hours to create something,
although not production-ready, shows that it should be feasible for corporations to 
invest more in secure technologies, especially given that Google has done most of the
grunt work in creating the sustainable ecosystem for the QR codes

This also shows that the algorithms used in the packages here (the OTP generation) is
not limited to the six digits as in the case of Google. This is done because for 2FA,
six digits is sufficient for added security. For primary security, it's possible to
adapt this method to produce a more complex string of digits/characters

Finally, this example is in Python, but there are numerous examples and libraries
available in other languages as well
'''

import cgi,sys,os  # pull in necessary dependencies
import cgitb       # for debugging purposes
import pyotp       # for generating one-time passwords


cgitb.enable()  # for debugging in browser

SECRET_KEY = 'ALLYOURBASEAREBELONGTOUS'  # the secret key, in a more advanced paradigm would change
                                         # for all users, but this script does not assume a DB
                                         # kind of akin to JWT (Javascript Web Token)


'''
check_code -- checks to see if a given code actually conforms to the OTP
              Returns: True/False
'''
def check_code(code, username):
    totp = pyotp.TOTP(SECRET_KEY+username)
    return totp.verify(code)


'''
main -- main loop retrieves any parameters and processes them
        Returns: None
        Routes:
        - getSecret: returns an <iframe> with a Google-generated QR code
                     for use in the Google Authenticator app
        - checkSecret: checks that for a given username, a code is correct
                       based on OTP generation
'''
def main():
    form = cgi.FieldStorage()  # retrieve any parameters in the URL path

    request = form.getvalue('request')
    request = request if request is not None else ''

    sys.stdout.write('Status: 200 OK\r\n')
    sys.stdout.write('Content-Type: application/html')
    sys.stdout.write('\n')
    sys.stdout.write('\n')

    # app.route('/getSecret') or in this case ?request=getSecret&username=mchow01
    if request == 'getSecret':
        username = form.getvalue('username')
        username = username if username is not None else ''
        qr_url = 'https://www.google.com/chart?chs=200x200&chld=M|0&cht=qr&chl=otpauth://totp/{0}%20-%20{1}%3Fsecret%3D{2}'.format(username, '2fa_example', SECRET_KEY+username)
        print ('<p>Scan the following QR code using Google Authenticator</p>')
        print ('<iframe src="'+qr_url+'"></iframe>')

    # app.route('/checkSecret') or in this case ?request=checkSecret&username=mchow01&code=123456
    elif request == 'checkSecret':
        username = form.getvalue('username')
        username = username if username is not None else ''
        code = form.getvalue('code')
        code = code if code is not None else ''
        
        if check_code(code, username):
            print ('<p>Code confirmed, the base belong to you</p>')
        else:
            print ('<p>Code could not be confirmed at this time. The FBI have been alerted. You have 10 seconds.</p>')

    else:
        print ('<p>Request type not supported</p>')

    return


if __name__ == '__main__':
    main()
