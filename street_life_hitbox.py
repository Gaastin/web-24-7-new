from flask import Flask, request, jsonify, render_template_string
import json, os

ADMIN_PASSWORD = "2009241030"
DATA_FILE = "data.json"

app = Flask(__name__)

# ---------- DATA ----------
def load_data():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

# ---------- HTML ----------
HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{{data.title}}</title>
<link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@600&display=swap" rel="stylesheet">
<style>
body{
background:
repeating-linear-gradient(0deg,rgba(0,255,136,.05),rgba(0,255,136,.05) 1px,transparent 1px,transparent 3px),
radial-gradient(circle at top,#0b1a14,#020504);
color:#00ff88;
font-family:'Share Tech Mono';
text-align:center;
padding:30px;
}
h1{
font-family:'Orbitron';
font-size:3em;
text-shadow:0 0 20px #00ff88;
}
.status{
display:inline-block;
padding:6px 16px;
border:1px solid #00ff88;
border-radius:8px;
box-shadow:0 0 20px rgba(0,255,136,.5);
animation:pulse 2s infinite;
}
pre{
background:#000;
border:1px solid rgba(0,255,136,.3);
padding:15px;
text-align:left;
max-width:720px;
margin:20px auto;
box-shadow:inset 0 0 20px rgba(0,255,136,.2);
white-space:pre-wrap;
}
button{
background:black;
color:#00ff88;
border:1px solid #00ff88;
padding:10px 20px;
cursor:pointer;
font-family:'Orbitron';
margin:5px;
}
button:hover{
background:#00ff88;
color:black;
box-shadow:0 0 25px #00ff88;
}
#admin{
display:none;
margin-top:30px;
}
input,textarea{
width:80%;
background:black;
color:#00ff88;
border:1px solid #00ff88;
margin:6px;
padding:8px;
font-family:'Share Tech Mono';
}
@keyframes pulse{
0%{box-shadow:0 0 5px #00ff88;}
50%{box-shadow:0 0 30px #00ff88;}
100%{box-shadow:0 0 5px #00ff88;}
}
</style>
</head>
<body>

<h1>{{data.title}}</h1>
<p>Creator: {{data.creator}}</p>
<p>Status: <span class="status">{{data.status}}</span></p>

<pre id="script">{{data.script}}</pre>

<button onclick="copy()">COPY SCRIPT</button>
<button onclick="admin()">ADMIN</button>

<div id="admin">
<h2>🧾 Admin Panel</h2>
<input id="title" placeholder="Title">
<input id="creator" placeholder="Creator">
<input id="status" placeholder="Status">
<textarea id="scriptEdit" rows="8"></textarea>
<br>
<button onclick="save()">SAVE</button>
</div>

<script>
function copy(){
navigator.clipboard.writeText(document.getElementById("script").innerText);
alert("Copied");
}
function admin(){
let p = prompt("Password:");
if(p === "{{password}}"){
document.getElementById("admin").style.display="block";
title.value="{{data.title}}";
creator.value="{{data.creator}}";
status.value="{{data.status}}";
scriptEdit.value=`{{data.script}}`;
}else{
alert("Wrong password");
}
}
function save(){
fetch("/update",{
method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({
title:title.value,
creator:creator.value,
status:status.value,
script:scriptEdit.value
})
}).then(()=>location.reload());
}
</script>

</body>
</html>
"""

# ---------- ROUTES ----------
@app.route("/")
def index():
    return render_template_string(HTML, data=load_data(), password=ADMIN_PASSWORD)

@app.route("/update", methods=["POST"])
def update():
    data = load_data()
    data.update(request.json)
    save_data(data)
    return jsonify(success=True)

# ---------- RUN (RENDER READY) ----------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
