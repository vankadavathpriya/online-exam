from flask import Flask, request, session, redirect, url_for, render_template_string
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText

app = Flask(__name__)
app.secret_key = "exam_secret_key"
app.permanent_session_lifetime = timedelta(minutes=30)

# ---------------- QUESTIONS ----------------
questions = {

"Python":[
{"q":"Who created Python?","options":["James Gosling","Guido van Rossum","Dennis Ritchie","Bjarne"],"answer":"Guido van Rossum"},
{"q":"Which keyword defines a function?","options":["function","func","define","def"],"answer":"def"},
{"q":"Which data type is mutable?","options":["tuple","string","list","int"],"answer":"list"},
{"q":"Which symbol is used for comments?","options":["#","//","--","/* */"],"answer":"#"},
{"q":"Which function prints output?","options":["echo()","print()","log()","show()"],"answer":"print()"},
{"q":"Python is?","options":["Compiled","Machine","Interpreted","Assembly"],"answer":"Interpreted"},
{"q":"Python file extension?","options":[".js",".java",".c",".py"],"answer":".py"},
{"q":"Which loop exists in Python?","options":["for","repeat","iterate","loop"],"answer":"for"},
{"q":"Which keyword handles exceptions?","options":["handle","catch","try","error"],"answer":"try"},
{"q":"Which library is used for math?","options":["calc","math","number","arithmetic"],"answer":"math"}
],

"DBMS":[
{"q":"DBMS stands for?","options":["Data Backup System","Database Management System","Database Monitoring System","Data Managing Server"],"answer":"Database Management System"},
{"q":"Which SQL statement fetches data?","options":["SELECT","REMOVE","FETCHALL","GET"],"answer":"SELECT"},
{"q":"Which command creates a table?","options":["NEW","BUILD","MAKE","CREATE"],"answer":"CREATE"},
{"q":"Which clause filters records?","options":["SORT","GROUP BY","ORDER BY","WHERE"],"answer":"WHERE"},
{"q":"Which command deletes a table?","options":["REMOVE","DELETE","DROP","CLEAR"],"answer":"DROP"},
{"q":"Which SQL command updates data?","options":["UPDATE","MODIFY","CHANGE","SET"],"answer":"UPDATE"},
{"q":"Primary key must be?","options":["Null","Duplicate","Unique","Optional"],"answer":"Unique"},
{"q":"Which command removes all records?","options":["TRUNCATE","DELETE","DROP","REMOVE"],"answer":"TRUNCATE"},
{"q":"Which joins tables?","options":["JOIN","MERGE","CONNECT","LINK"],"answer":"JOIN"},
{"q":"Which normal form removes redundancy?","options":["2NF","1NF","3NF","BCNF"],"answer":"3NF"}
],

"Java":[
{"q":"Who developed Java?","options":["James Gosling","Dennis Ritchie","Guido","Linus"],"answer":"James Gosling"},
{"q":"Java is?","options":["Compiled","Interpreted","Both","None"],"answer":"Both"},
{"q":"Extension of Java file?","options":[".java",".class",".j",".jav"],"answer":".java"},
{"q":"Java uses?","options":["Node","CLR","Python","JVM"],"answer":"JVM"},
{"q":"Java supports?","options":["Functional","Procedural","OOP","None"],"answer":"OOP"},
{"q":"Main method syntax?","options":["public static void main()","main()","start()","run()"],"answer":"public static void main()"},
{"q":"Java released in?","options":["1990","2000","1995","1985"],"answer":"1995"},
{"q":"Which keyword defines class?","options":["define","Class","object","struct"],"answer":"class"},
{"q":"Which symbol ends statement?","options":[";",".",":",","],"answer":";"},
{"q":"Java platform is?","options":["Dependent","Independent","Windows only","Linux only"],"answer":"Independent"}
],

"Operating System":[
{"q":"OS stands for?","options":["Operating System","Open Software","Operating Service","Online System"],"answer":"Operating System"},
{"q":"Which is an example of OS?","options":["HTML","Python","Oracle","Windows"],"answer":"Windows"},
{"q":"Which OS is open source?","options":["MacOS","Windows","Linux","DOS"],"answer":"Linux"},
{"q":"Which manages hardware resources?","options":["Error","Compiler","Database","Operating system"],"answer":"Operating System"},
{"q":"Process scheduling is done by?","options":["CPU Scheduler","Memory Manager","File System","Compiler"],"answer":"CPU Scheduler"},
{"q":"Which memory is fastest?","options":["ROM","RAM","Cache","Disk"],"answer":"Cache"},
{"q":"Which OS allows multiple users?","options":["Multi-user OS","Single-user OS","Batch OS","Embedded OS"],"answer":"Multi-user OS"},
{"q":"Which OS used in smartphones?","options":["linux","Windows","Android","DOS"],"answer":"Android"},
{"q":"Which technique avoids deadlock?","options":["Banker's Algorithm","Round Robin","FCFS","FIFO"],"answer":"Banker's Algorithm"},
{"q":"Which scheduling algorithm uses time slice?","options":["SJF","FCFS","Round Robin","Priority"],"answer":"Round Robin"}
],

"Computer Networks":[
{"q":"Full form of LAN?","options":["Long Area Network","Large Area Network","Local Area Network","Logical Area Network"],"answer":"Local Area Network"},
{"q":"Which device connects networks?","options":["Hub","Switch","Router","Bridge"],"answer":"Router"},
{"q":"IP stands for?","options":["Interface Protocol","Internal Process","Internet Process","Internet Protocol"],"answer":"Internet Protocol"},
{"q":"Which layer is responsible for routing?","options":["Transport","Network","Data Link","Session"],"answer":"Network"},
{"q":"HTTP stands for?","options":["Hyperlink Transfer Protocol","High Text Transfer Protocol","Hyper Text Transfer Protocol","Home Transfer Protocol"],"answer":"Hyper Text Transfer Protocol"},
{"q":"Which topology uses a central hub?","options":["Star","Ring","Bus","Mesh"],"answer":"Star"},
{"q":"Which protocol is used for email?","options":["TCP","FTP","HTTP","SMTP"],"answer":"SMTP"},
{"q":"Which layer ensures reliable delivery?","options":["Session","Network","Transport","Application"],"answer":"Transport"},
{"q":"Which device forwards data using MAC address?","options":["Switch","Router","Gateway","Modem"],"answer":"Switch"},
{"q":"Which protocol transfers files?","options":["SMTP","HTTP","FTP","POP3"],"answer":"FTP"}
]

}

# ---------------- CSS ----------------
style = """
body{font-family:Arial;background:#f2f2f2;text-align:center}
.container{background:white;padding:30px;margin:auto;width:400px;margin-top:60px;border-radius:10px;box-shadow:0 0 10px gray}
button{padding:10px 20px;background:#3498db;color:white;border:none;border-radius:5px;cursor:pointer}
.timer{font-size:22px;color:red;font-weight:bold}
.navbar{background:#2c3e50;color:white;padding:15px}
"""

# ---------------- ROUTES ----------------

@app.route("/")
def portal():
    return render_template_string("""
<style>{{style}}</style>
<div class="navbar"><h2>SmartExam Portal</h2></div>
<div class="container">
<h1>Online Examination System</h1>
<a href="/login"><button>Start Exam</button></a>
</div>
""",style=style)

@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":
        session["user"]=request.form["username"]
        return redirect("/home")

    return render_template_string("""
<style>{{style}}</style>
<div class="container">
<h2>Student Login</h2>
<form method="POST">
<input name="username" required>
<br><br>
<button type="submit">Continue</button>
</form>
</div>
""",style=style)

@app.route("/home",methods=["GET","POST"])
def home():
    if request.method=="POST":
        session["topic"]=request.form["topic"]
        session["q_index"]=0
        session["answers"]={}
        session["end_time"]=(datetime.now()+timedelta(seconds=60)).timestamp()
        return redirect("/exam")

    return render_template_string("""
<style>{{style}}</style>
<div class="container">
<h2>Welcome {{session['user']}}</h2>
<form method="POST">
<select name="topic">
{% for s in questions %}
<option>{{s}}</option>
{% endfor %}
</select>
<br><br>
<button>Start Test</button>
</form>
</div>
""",questions=questions,style=style)

@app.route("/exam",methods=["GET","POST"])
def exam():
    topic=session["topic"]
    q_index=session["q_index"]
    exam_questions=questions[topic]

    remaining=int(session["end_time"]-datetime.now().timestamp())

    if remaining<=0:
        return redirect("/result")

    if request.method=="POST":
        ans=request.form.get("answer")
        if ans:
            session["answers"][str(q_index)]=ans

        action=request.form.get("action")
        if action=="next":
            session["q_index"]+=1
        elif action=="prev" and q_index>0:
            session["q_index"]-=1

        if session["q_index"]>=len(exam_questions):
            return redirect("/result")

        return redirect("/exam")

    q=exam_questions[q_index]

    return render_template_string("""
<style>{{style}}</style>
<div class="container">

<h3>{{topic}} ({{i}}/{{t}})</h3>

<div class="timer">Time: <span id="time">{{time}}</span></div>

<form method="POST">

<p><b>{{q.q}}</b></p>

{% for o in q.options %}
<input type="radio" name="answer" value="{{o}}"> {{o}}<br>
{% endfor %}

<br>
<button name="action" value="prev">Prev</button>
<button name="action" value="next">Next</button>

</form>

</div>

<script>
let t={{time}};
setInterval(()=>{
document.getElementById("time").innerHTML=t;
t--;
if(t<0){window.location="/result";}
},1000);
</script>
""",q=q,i=q_index+1,t=len(exam_questions),topic=topic,style=style,time=remaining)

@app.route("/result")
def result():
    topic=session["topic"]
    qs=questions[topic]
    score=0

    for i,q in enumerate(qs):
        if session["answers"].get(str(i))==q["answer"]:
            score+=1

    if score>=7:
        return redirect(url_for("certificate",score=score,total=len(qs),topic=topic))

    return f"<h2>Score: {score}/{len(qs)}</h2><a href='/home'>Retry</a>"

# ---------------- CERTIFICATE ----------------
@app.route("/certificate")
def certificate():

    name = session["user"]
    topic = request.args.get("topic")
    score = request.args.get("score")
    total = request.args.get("total")

    date = datetime.now().strftime("%d %B %Y")
    cert_id = "CERT-" + datetime.now().strftime("%Y%m%d%H%M%S")

    return render_template_string("""
    <style>
    body{background:#f4f1ea;font-family:Georgia;text-align:center;}
    .certificate{width:90%;margin:40px auto;padding:50px;background:white;border:12px solid gold;}
    .main-title{font-size:40px;color:goldenrod;}
    .name{font-size:35px;font-weight:bold;}
    .footer{display:flex;justify-content:space-between;margin-top:50px;}
    </style>

    <div class="certificate">
        <h3>ONLINE EXAMINATION</h3>
        <div class="main-title">Certificate of Achievement</div>
        <p>This is proudly presented to</p>
        <div class="name">{{name}}</div>
        <p>for successfully passing the <b>{{topic}}</b> Examination</p>
        <p>Score: {{score}} / {{total}}</p>
        <p>Date: {{date}}</p>
        <p>ID: {{cert_id}}</p>

        <div class="footer">
            <div>Instructor</div>
            <div>Director</div>
        </div>

        <button onclick="window.print()">Print</button>

        <hr>

        <form method="POST" action="/send_email">
        <input type="email" name="email" placeholder="Enter your email" required>
        <input type="hidden" name="topic" value="{{topic}}">
        <input type="hidden" name="score" value="{{score}}">
        <input type="hidden" name="total" value="{{total}}">
        <br><br>
        <button>Send Certificate</button>
        </form>
    </div>
    """,name=name,topic=topic,score=score,total=total,date=date,cert_id=cert_id)

# ---------------- EMAIL ----------------
@app.route("/send_email", methods=["POST"])
def send_email():

    sender = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")

    receiver = request.form["email"]

    name = session["user"]
    topic = request.form["topic"]
    score = request.form["score"]
    total = request.form["total"]

    date = datetime.now().strftime("%d %B %Y")

    html = f"""
    <html>
    <body style="background:#f4f1ea;font-family:Georgia;text-align:center;">

    <div style="width:90%;margin:auto;padding:50px;background:white;border:12px solid gold;">

        <h3>ONLINE EXAMINATION</h3>

        <h1 style="color:goldenrod;">Certificate of Achievement</h1>

        <p>This is proudly presented to</p>

        <h2 style="font-size:30px;">{name}</h2>

        <p>for successfully passing the <b>{topic}</b> Examination</p>

        <p><b>Score:</b> {score} / {total}</p>
        <p><b>Date:</b> {date}</p>

        <br><br>

        <div style="display:flex;justify-content:space-between;">
            <span>Instructor</span>
            <span>Director</span>
        </div>

    </div>

    </body>
    </html>
    """

    msg = MIMEText(html, "html")
    msg["Subject"] = "Your Exam Certificate 🎓"
    msg["From"] = sender
    msg["To"] = receiver

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587, timeout=10)
        server.ehlo()
        server.starttls()
        server.ehlo()

        server.login(sender, password)
        server.send_message(msg)
        server.quit()

        return "<h2>Certificate Sent Successfully ✅ Check your Mail</h2>"

    except Exception as e:
        print("EMAIL ERROR:", e)
        return f"<h2>Email Failed ❌</h2><p>{str(e)}</p>"
# ---------------- RUN ----------------
if __name__=="__main__":
    app.run(debug=True)
