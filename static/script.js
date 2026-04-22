// ================= REGISTER =================
function register() {
  fetch("http://127.0.0.1:5000/register", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      username: document.getElementById("ruser").value,
      email: document.getElementById("remail").value,
      phone: document.getElementById("rphone").value,
      password: document.getElementById("rpass").value
    })
  })
  .then(res => res.json())
  .then(data => {
    alert(data.message);
    window.location.href = "/";
  });
}
async function sendMessage() {
  let input = document.getElementById("chatInput");
  let msg = input.value;

  if (!msg) return;

  let chatBox = document.getElementById("chatMessages");

  chatBox.innerHTML += `<p><b>You:</b> ${msg}</p>`;

  let res = await fetch("/chat", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ message: msg })
  });

  let data = await res.json();

  chatBox.innerHTML += `<p><b>AI:</b> ${data.reply}</p>`;
  input.value = "";
}

// ================= LOGIN =================
async function login() {
  let data = {
    email: document.getElementById("lemail").value,
    password: document.getElementById("lpass").value
  };

  let res = await fetch("/login", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify(data)
  });

  let result = await res.json();

  if (res.ok) {
    localStorage.setItem("email", data.email);
    window.location.href = "/dashboard";
  } else {
    alert(result.message);
  }
}


// ================= LOAD USER =================
function loadUser() {
  let email = localStorage.getItem("email");

  if (!email) {
    window.location.href = "/";
    return;
  }

  fetch(`/get-user/${email}`)
    .then(res => res.json())
    .then(user => {
      document.getElementById("helloText").innerText = "Hello, " + user.username;
      document.getElementById("pname").innerText = user.username;
      document.getElementById("pemail").innerText = user.email;
      document.getElementById("pphone").innerText = user.phone;
    });
}


// ================= SIDEBAR =================
function toggleSidebar() {
  document.getElementById("sidebar").classList.add("active");
  document.getElementById("overlay").style.display = "block";
}

function closeSidebar() {
  document.getElementById("sidebar").classList.remove("active");
  document.getElementById("overlay").style.display = "none";
}


// ================= PROFILE =================
function toggleProfile() {
  let p = document.getElementById("profileBox");
  let overlay = document.getElementById("overlay");

  p.classList.toggle("active");
  overlay.style.display = p.classList.contains("active") ? "block" : "none";
}
function closeProfile() {
  document.getElementById("profileBox").classList.remove("active");
  document.getElementById("overlay").style.display = "none";
}

// ================= LOGOUT =================
function logout() {
  localStorage.removeItem("email");
  window.location.href = "/";
}


// ================= LOAD PAGE =================
function loadPage(name) {
  let main = document.getElementById("contentArea");

  main.innerHTML = `
    <div class="hero">
      <h1>${name}</h1>
      <p>Prediction module coming soon...</p>
    </div>
  `;
}


// ================= HISTORY (FIXED 🔥) =================
function openHistory() {
  window.location.href = "/history";   // ✅ THIS IS THE MAIN FIX
}


// ================= SAVE HISTORY =================
function saveHistory(action) {
  let history = JSON.parse(localStorage.getItem("history")) || [];
  history.push(action + " (" + new Date().toLocaleTimeString() + ")");
  localStorage.setItem("history", JSON.stringify(history));
}


// ================= PREDICT =================
async function predictDisease() {

  let allSymptoms = [
    "weight_loss","fatigue","lump","pain","bleeding",
    "chest_pain","shortness_of_breath","sweating","nausea",
    "arm_pain","weakness","confusion","trouble_speaking",
    "dizziness","headache","memory_loss","difficulty_thinking",
    "mood_changes","swelling","frequent_urination"
  ];

  let selected = document.querySelectorAll("input[name='symptom']:checked");

  let selectedValues = Array.from(selected).map(s => s.value);

  let input = allSymptoms.map(sym =>
    selectedValues.includes(sym) ? 1 : 0
  );

  let email = localStorage.getItem("email");

  let res = await fetch("/predict", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      symptoms: input,
      email: email
    })
  });

  let data = await res.json();

  console.log(data);
}