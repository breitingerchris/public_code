import re
import mechanize
import cookielib


cj = cookielib.LWPCookieJar()
br = mechanize.Browser()
br.set_cookiejar(cj)
br.set_handle_equiv(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
br.open("https://live.xbox.com/")
assert br.viewing_html()
links = br.links(url_regex='Signin\?returnUrl')
br.open(links[1])
br.select_form(name="f1")
br["login"] = ["woxxy123@hotmail.com"]
br["passwd"] = ["playtime2"]
response2 = br.submit()

# print currently selected form (don't call .submit() on this, use br.submit())
print br.form