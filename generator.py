import json
import os
from subprocess import Popen, PIPE

profile = {}
blogs = []
contacts = []

mailSVG = '''<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none"
                stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                class="feather feather-mail">
                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
                <polyline points="22,6 12,13 2,6"></polyline>
            </svg>'''
twitterSVG = '''<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none"
                stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                class="feather feather-twitter">
                <path d="M23 3a10.9 10.9 0 0 1-3.14 1.53 4.48 4.48 0 0 0-7.86 3v1A10.66 10.66 0 0 1 3 4s-4 9 5 13a11.64 11.64 0 0 1-7 2c9 5 20 0 20-11.5a4.5 4.5 0 0 0-.08-.83A7.72 7.72 0 0 0 23 3z">
                </path>
            </svg>'''
githubSVG = '''<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 24 24" fill="none"
                stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"
                class="feather feather-github">
                <path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22">
                </path>
            </svg>'''

js = '<script>const stylesheet=document.documentElement.style;const toggle=document.querySelector(".switch__input[data-theme-toggle]");toggle.addEventListener("click",()=>{const lightBg=getComputedStyle(document.documentElement).getPropertyValue("--light-bg");const lightAccent=getComputedStyle(document.documentElement).getPropertyValue("--light-accent");const lightAccent2=getComputedStyle(document.documentElement).getPropertyValue("--light-accent-2");const darkBg=getComputedStyle(document.documentElement).getPropertyValue("--dark-bg");const darkAccent=getComputedStyle(document.documentElement).getPropertyValue("--dark-accent");const darkAccent2=getComputedStyle(document.documentElement).getPropertyValue("--dark-accent-2");stylesheet.setProperty("--dark-bg",lightBg);stylesheet.setProperty("--dark-accent",lightAccent);stylesheet.setProperty("--dark-accent-2",lightAccent2);stylesheet.setProperty("--light-bg",darkBg);stylesheet.setProperty("--light-accent",darkAccent);stylesheet.setProperty("--light-accent-2",darkAccent2)});</script>'

with open('profile.json', 'r') as file:
    profile = json.loads(''.join(file.readlines()))

for blog in profile["blogs"]:
    name = blog["name"]
    link = blog["link"]
    blogs.append("<a href='"+link+"'> <li>"+name+"</li></a>")

if(profile["github"] != ""):
    contacts.append("<a href='"+profile["github"]+"'>"+githubSVG+"</a>")
if(profile["twitter"] != ""):
    contacts.append("<a href='"+profile["twitter"]+"'>"+twitterSVG+"</a>")
if(profile["mail"] != ""):
    contacts.append("<a href='"+profile["mail"]+"'>"+mailSVG+"</a>")

indexHTML = [
    '''<!DOCTYPE html><html><head><meta charset="utf-8">
    <link rel="stylesheet" href="../css/index.css"><meta name="viewport" content="width=device-width, initial-scale=1">
    <title>''', profile["name"], '''</title></head>
    <body>
    <h1 style="display: inline-block; padding-right: 20px;">''', profile["name"], '''</h1>
    <label class="switch">THEME<input class="switch__input" type="submit" data-theme-toggle></label>
    <hr>
    <div class="profile">
        <img src="../pfp.png"
            width="150" height="150" style="float:left; margin-right: 15px; margin-top: 5px;">
        <p>''',profile["description"],'''</p>
    </div>
    <br><br><h2>BLOGS</h2><hr>
    <div class="project">
        <ul>''', ''.join(blogs), '''</ul>
    </div>
    <br><h2>CONTACTS</h2><hr>
    <div class="contact">''', ''.join(contacts), '''</div>
    ''',js,'''
    </body></html>
    '''
]

try:
    os.mkdir("docs")
except:
    x = 0

with open('docs/index.html', 'w') as file:
    file.writelines(indexHTML)

# Blogs


blogBtns = '''<a class="home" href="index.html">HOME</a>
<label class="switch">THEME<input class="switch__input" type="submit" data-theme-toggle></label>  

---

'''

def createBlogs():
    with os.scandir('blogs/') as entries:
        for entry in entries:
            if ".md" in entry.name:
                blogContents = []
                blogContents.append(blogBtns)
                with open('blogs/'+entry.name, 'r') as file:
                    blogContents.append(''.join(file.readlines()))
                blogContents.append('\n<script src="../js/highlight.min.js"></script><script>hljs.highlightAll();</script>')
                blogContents.append(js)
                with open('docs/'+entry.name, 'w') as file:
                    file.writelines(blogContents)
                md_to_html(entry.name)
                os.remove('docs/'+entry.name)

def md_to_html(entry):
    process = Popen([
            'css/../pandoc', '--metadata', 'title='+profile["name"],'-s', '--no-highlight', '-c', '../css/blog.css', 
            'docs/'+entry, 
            '-o', 'docs/'+entry[:-3]+'.html'
        ], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    error = bytes.decode(stderr)
    if(error == ""):
        print('\033[32m '+entry+' successfully translated to html'+' \033[0m')
    else:
        print("\033[31m '"+error+"' \033[0m")

createBlogs()