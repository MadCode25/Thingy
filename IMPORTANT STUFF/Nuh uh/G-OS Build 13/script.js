// JavaScript for G-OS Build 13 - 15
// Developed by AmadOS (with only one person me, MadCode25, some from ChatGPT, tbh)
// Welp, no collaborators here to help me :(
// Change it, if you want to, and make ur own fan version of G-OS <3
// WARNING: DO NOT STEAL MY CODE, UNLESS YOU GIVE CHANGES, THX :D

// inits for the elements, (IMPORTANT!!!!)
const input = document.getElementById("password");
const textLogin = document.getElementById("loggingIn");
const parag = document.getElementById("passHint");
const welcome = document.getElementById("welcome");
const button = document.getElementById("login");
const gs = document.getElementById("getStarted");
const ts = document.getElementById("timeSeperator");
const tsk = document.getElementById("taskbar");
const menu = document.getElementById("menu");
const tskm = document.getElementById("taskManagerWindow");
const settingsWindow = document.getElementById("settings");
const winwtvdownloader = document.getElementById("windowsWTVWindow");
const OSS = document.getElementById("osStore");
const wwtvd = document.getElementById("WWTVD");
let gsOpenOnStartup = true;
let settingsOpenOnStartup = false;
const gsc = document.getElementById('getStartedCheckbox').checked = true;
const swn = document.getElementById('settingsWin').checked = false;
const savedStartup = localStorage.getItem("startupWindows");
const ose = document.getElementById("osStore");
const tsko = document.getElementById("taskbarOptions");
// Objects to keep track of opened G-OS apps, and much (maybe) more.
let lastOpenedApps = [];
let startupWindows = [];
if (savedStartup) {
  startupWindows = JSON.parse(savedStartup);

  // Set checkboxes based on saved startupWindows
  document.getElementById('getStartedCheckbox').checked = startupWindows.includes("Get_Started");
  document.getElementById('settingsWin').checked = startupWindows.includes("Settings");
}

wwtvd.style.display = "none";


// Function to show the current time
function showTime() {
	document.getElementById('currentTime').innerHTML = new Date().toUTCString();
}
showTime();
setInterval(function () {
	showTime();
}, 1000);

// Basically matches the password :D
function matchPassword() {
  if (input.value === "MadCode25" || input.value === "M4") {
    textLogin.innerHTML = "Logging in...";
    // After 2 seconds, hide login elements and show main UI, to log in ofc c:
    setTimeout(function() {
      textLogin.style.display = "none";
      input.style.display = "none"
      parag.style.display = "none";
      welcome.style.display = "none";
      button.style.display = "none";
      if (startupWindows.includes("Get_Started")) {
        gs.style.display = "block";
        lastOpenedApps.push("getstarted.exe");
        makeDraggable(gs);
        centerElement(gs);
      } else {
        gs.style.display = "none";
      }

      if (startupWindows.includes("Settings")) {
        settingsWindow.style.display = "block";
        lastOpenedApps.push("settings.exe");
        makeDraggable(settingsWindow);
        centerElement(settingsWindow);
      } else {
        settingsWindow.style.display = "none";
      }
      ts.style.display = "none";
      tsk.style.display = "block";
      makeDraggable(gs);
    }, 2000);
  } // Job Easter Egg 🥀 ;-;
  else if(input.value === "job" || input.value === "Job" || input.value === "jobs" || input.value === "Jobs") {
    textLogin.innerHTML = "Nahh bro 😭";
    setTimeout(function(){
      textLogin.innerHTML = "You tryna' give me fears or something? 💀"
    }, 2000)
    setTimeout(function(){
      textLogin.innerHTML = "Anyways, password is incorrect, womp womp. 😂"
    }, 4000)
  }
  else { // If password is incorrect
    textLogin.innerHTML = "Password is incorrect.";
  }
}
// Function to make an element draggable, kinda complex ngl (from ChatGPT, thats why, also added tiny changes)
function makeDraggable(el) {
      let offsetX = 0, offsetY = 0, isDown = false;

      el.addEventListener("mousedown", (e) => {
        isDown = true;
        offsetX = e.clientX - el.offsetLeft;
        offsetY = e.clientY - el.offsetTop;
        document.addEventListener("mousemove", mouseMove);
        document.addEventListener("mouseup", mouseUp);
      });

      function mouseMove(e) {
        if (!isDown) return;
        el.style.left = (e.clientX - offsetX) + "px";
        el.style.top = (e.clientY - offsetY) + "px";
      }

      function mouseUp() {
        isDown = false;
        document.removeEventListener("mousemove", mouseMove);
        document.removeEventListener("mouseup", mouseUp);
      }
    }
  // Function to center an element in the viewport (i meant the tiny changes were here, still from ChatGPT)
function centerElement(el) {
      // get viewport size (height and width (: )
      const winW = window.innerWidth;
      const winH = window.innerHeight;
      // get element size
      const elW = el.offsetWidth;
      const elH = el.offsetHeight;
      // place in center
      el.style.left = (winW / 3.9 - elW / 3.9) + "px";
      el.style.top = (winH / 3 - elH / 3) + "px";
}





centerElement(gs);
// Teeny tiny functions :3
// Simple function to close a window <3
function closeWindow(elem) {
  elem.style.display = "none";
}
//Open the start menu function, so tiny :3
function startMenu() {
  menu.style.display = "block";
  menu.style.top = "302" + "px";
    
}
// Tiny, but kinda complex functions ¯\_(ツ)_/¯
function shutdown() {
  body = document.body; // <-- Body element (IMPORTANT TO CHANGE STUFF IN WEBSITE, AND BROWSER)
  body.innerHTML = '<div class="shutdown-screen"><h1>Shutting Down...</h1></div>'; // Told ya, the "body" thing is changed here using this
  body.style.backgroundColor = "black"; // You know what this does, right? 8)
  setTimeout(function() {
    window.location.href = "about::blank"; // Redirecting u in a blank after 3 seconds
    window.close(); // Then closes the window (or website, idrk, but ig it should work ¯\_(ツ)_/¯)
  }, 3000)
}
// Settings function, with a slightly annoying warning alert >:)
function settings() {
  settingsWindow.style.display = "block"; // <-- Shows the settings window, obviously...
  lastOpenedApps.push("settings.exe"); // <-- Adds settings.exe to the last opened apps list, kinda informative if you ask me, ig XD
  centerElement(settingsWindow);
  makeDraggable(settingsWindow);
  alert("Warning: Settings is still in development, some settings may not work as intended. Press 'OK' to proceed."); // <-- Here it is, the annoying warning, which breaks the OS-ish style of G-OS, might remove it soon (maybe in build 15 or later builds)
}
// Some important functions for the buttons in the taskbar, <: (some from ChatGPT, some made by me)
function downloadWindowsWTV(){
  winwtvdownloader.innerHTML = `
  <h1>Windows WTV Downloader</h1>
  <h3>Are you sure to download this OS?</h3>
  <p>You are downloading Windows WTV in a browser, which makes your browser technically a Virtualbox</p>
  <button onclick="downloadWindowsWTV()">Yes</button>
  <button onclick="closeWindow(windowsWTVWindow)">Nope</button>
  `
}
// Function to add a button to the taskbar, and prevent duplicates :3
function addTaskbarButton(id, label, onClick) {
  // avoid duplicate buttons '
  // ' ' ' ' ' ' ' ' ' ' ' ' '
  // VVVVVVVVVVVVVVVVVVVVVVVVV
  if (document.getElementById('taskbtn-' + id)) return; // Idk what this really does, but ChatGPT said that this part gets a variable (or object, i forgot...) that a button uses
  const btn = document.createElement('button'); // Creates the button element, as chatgpt said so
  btn.id = 'taskbtn-' + id; // Ik what this does, it gives the button an id, so it can be identified later, which what the code at the top of me important
  btn.className = 'taskbar-button'; // Gives the button a class name, so it can be styled with CSS
  btn.textContent = label;
  btn.onclick = onClick || (() => { // This part is a bit complex ngl, but ig it gives the button an onclick function, which is either the onClick parameter, or a default function that toggles the window's visibility, C O M P L E X I T Y (*__*)
    const win = document.getElementById(id);
    if (!win) return;
    win.style.display = (win.style.display === 'none' || win.style.display === '') ? 'block' : 'none';
    centerElement(win);
  });
  tsk.appendChild(btn);
}

function openWindowsWTVDownloader() {
  winwtvdownloader.style.display = "block";
  lastOpenedApps.push("WindowsWTV_Downloader.exe");
  centerElement(winwtvdownloader);
  makeDraggable(winwtvdownloader);

  // add a taskbar button for the WWTVD window (toggle the window, not the taskbar button)
  addTaskbarButton('windowsWTVWindow', 'WWTVD', () => {
    const win = document.getElementById('windowsWTVWindow');
    if (!win) return;
    win.style.display = (win.style.display === 'none' || win.style.display === '') ? 'block' : 'none';
    centerElement(win);
  });
}
// Basically downloads an app, with some fake loading messages >:)
function downloadApp(appName) {
  if (appName === "WindowsWTV") {
    OSS.innerHTML = "Starting download for Windows WTV Downloader...";
    setTimeout(function() {OSS.innerHTML = "<h1>Checking info...</h1>";}, 4000);
    setTimeout(function() {OSS.innerHTML = "<h1>Preparing files...</h1>"}, 8000);
    setTimeout(function() {OSS.innerHTML = "<h1>Download finished! We're opening the downloader...</h1>"}, 12000);
    setTimeout(function() {
      openWindowsWTVDownloader();
      // ensure the window is shown (openWindowsWTVDownloader already sets this)
      document.getElementById('windowsWTVWindow').style.display = "block";
      closeWindow(OSS);
    }, 16000);
  }
}
// Basically checks the startup options, and saves them to localStorage, kind of like  a box that contains stuff, for example, cookies :3
function checkStartupOptions() {
  // Get checkbox states at the moment the function is called
  const getStartedChecked = document.getElementById('getStartedCheckbox').checked; // <-- Fixed variable name here
  const settingsChecked = document.getElementById('settingsWin').checked;

  // Update startupWindows array based on checkboxes
  startupWindows = [];
  if (getStartedChecked) startupWindows.push("Get_Started");
  if (settingsChecked) startupWindows.push("Settings");

  // Save to localStorage for persistence
  localStorage.setItem("startupWindows", JSON.stringify(startupWindows));

  

  alert("Startup options saved!");
}



// Opens G-OS Store (: (Ig this function is supposed to be part of the "Functions that are small, but complex" group lol)
function GOSStore() {
  ose.style.display = "block";
  centerElement(ose);
  makeDraggable(ose);
  lastOpenedApps.push("G-OS_Store.exe");
  lastOpenedApps.push("G-OS_Store_Download.exe");
}




tsk.addEventListener('contextmenu', function(event) {
  event.preventDefault(); // Prevents the default context menu
  tsko.style.display = "block";
  tsko.style.left = event.clientX + "px";
  tsko.style.top = "500" + "px";
});

// GAASSP! TASK MANAGER?? WOWWEEEEE (: (mostly by me, some from ChatGPT)
function taskManager() {
  tskm.style.display = "block";
  centerElement(tskm);
  makeDraggable(tskm);
  tskm.innerHTML = "<p>Recently Opened Applications:</p><ul>" + lastOpenedApps.map(app => `<li>${app}</li>`).join('') + '</ul><br><br><button onclick="closeWindow(tskm)">Close</button>';
}