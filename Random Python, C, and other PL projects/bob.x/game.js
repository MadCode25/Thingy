// --- 1. GAME VARIABLES ---
let camera, scene, renderer;
let playerVelocity = new THREE.Vector3();
let pitchObject, yawObject;
const objects = [];      // Platforms
const killBricks = [];   // Lava
const touchParts = [];   // Checkpoints/Buttons
const username = document.getElementById("username").value

let isLocked = false;
let moveForward = false, moveBackward = false, moveLeft = false, moveRight = false;
let canJump = false;
let bv = document.getElementById("bobux_val").value

let currentStage = 1;
let spawnPoint = new THREE.Vector3(0, 5, 0);

// --- 2. UI ELEMENTS ---
const chatInput = document.querySelector('.chat-input');
const chatHistory = document.getElementById('chat');
const stageDisplay = document.getElementById('stage-display');

// --- 3. INITIALIZATION ---
init();
animate();

function init() {
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x87CEEB);
    scene.fog = new THREE.Fog(0x87CEEB, 10, 80);

    camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    
    pitchObject = new THREE.Object3D();
    pitchObject.add(camera);
    
    yawObject = new THREE.Object3D();
    yawObject.position.y = 10;
    yawObject.add(pitchObject);
    scene.add(yawObject);

    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.body.appendChild(renderer.domElement);

    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
    scene.add(ambientLight);
    const dirLight = new THREE.DirectionalLight(0xffffff, 0.6);
    dirLight.position.set(10, 20, 10);
    scene.add(dirLight);

    buildLevel();

    // Event Listeners
    document.addEventListener('keydown', onKeyDown);
    document.addEventListener('keyup', onKeyUp);
    document.addEventListener('mousemove', onMouseMove);
    window.addEventListener('resize', onWindowResize);

    const startScreen = document.getElementById('start-screen');
    startScreen.addEventListener('click', () => {
        document.body.requestPointerLock();
    });

    document.addEventListener('pointerlockchange', () => {
        isLocked = (document.pointerLockElement === document.body);
        startScreen.style.display = isLocked ? 'none' : 'block';
        if (!isLocked) startScreen.innerHTML = "<h1>PAUSED</h1><p>Click to Resume</p>";
    });
}

// --- 4. CHAT SYSTEM ---
function sendMessage() {
    const text = chatInput.value.trim();
    if (text !== "") {
        const msg = document.createElement('div');
        msg.innerHTML = `<span style="color: #8ec07c">[${username}]:</span> ${text}`;
        chatHistory.appendChild(msg);
        chatHistory.scrollTop = chatHistory.scrollHeight;
        chatInput.value = "";
        chatInput.blur();
        document.body.requestPointerLock();
    }
}

// --- 5. CONTROLS ---
function onKeyDown(event) {
    // Chat Shortcut
    if (event.code === 'Slash' && isLocked) {
        event.preventDefault();
        chatInput.focus();
        return;
    }
    if (event.code === 'Enter') {
        if (document.activeElement === chatInput) sendMessage();
        else chatInput.focus();
        return;
    }

    // Movement (Skip if typing)
    if (document.activeElement === chatInput) return;

    switch (event.code) {
        case 'KeyW': moveForward = true; break;
        case 'KeyS': moveBackward = true; break;
        case 'KeyA': moveLeft = true; break; // Fixed
        case 'KeyD': moveRight = true; break; // Fixed
        case 'Space': 
            if (canJump) {
                playerVelocity.y += 15;
                canJump = false;
            }
            break;
    }
}

function onKeyUp(event) {
    switch (event.code) {
        case 'KeyW': moveForward = false; break;
        case 'KeyS': moveBackward = false; break;
        case 'KeyA': moveLeft = false; break;
        case 'KeyD': moveRight = false; break;
    }
}

function onMouseMove(event) {
    if (isLocked && document.activeElement !== chatInput) {
        const movementX = event.movementX || 0;
        const movementY = event.movementY || 0;
        yawObject.rotation.y -= movementX * 0.002;
        pitchObject.rotation.x -= movementY * 0.002;
        pitchObject.rotation.x = Math.max(-Math.PI / 2, Math.min(Math.PI / 2, pitchObject.rotation.x));
    }
}

function checkCollisions(delta) {
    // 1. Create the Player's Hitbox (This handles X and Z sides)
    const playerBox = new THREE.Box3().setFromCenterAndSize(
        yawObject.position, 
        new THREE.Vector3(1.5, 3.8, 1.5) // Your width, height, and depth
    );

    // 2. CHECK LAVA FIRST (Sides & Bottom)
    for (let lava of killBricks) {
        const lavaBox = new THREE.Box3().setFromObject(lava);
        if (playerBox.intersectsBox(lavaBox)) {
            resetPlayer();
            return; // Stop everything else, we're dead!
        }
    }

    // 3. CHECK FLOOR (Y Axis)
    const floorRay = new THREE.Raycaster(yawObject.position, new THREE.Vector3(0, -1, 0), 0, 2.1);
    const floorHits = floorRay.intersectObjects(objects);

    if (floorHits.length > 0) {
        if (playerVelocity.y < 0) playerVelocity.y = 0;
        yawObject.position.y = floorHits[0].point.y + 2; 
        canJump = true;
    } else {
        canJump = false;
    }

    // 4. CHECK TOUCH PARTS (Events/Checkpoints)
    touchParts.forEach((part) => {
        const partBox = new THREE.Box3().setFromObject(part);
        if (playerBox.intersectsBox(partBox) && !part.userData.touched) {
            // Your checkpoint/message logic here
            part.userData.touched = true;
        }
    });
}

function resetPlayer() {
    const oof = document.getElementById('oof-screen');
    oof.style.opacity = 0.5;
    setTimeout(() => { oof.style.opacity = 0; }, 200);
    yawObject.position.copy(spawnPoint);
    playerVelocity.set(0, 0, 0)
    
    const msg = document.createElement('div');
    msg.innerHTML = "<span style='color:red'>[System]: OOF! You died.</span>";
    chatHistory.appendChild(msg);
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

// --- 7. LEVEL BUILDER ---
function createBlock(x, y, z, w, h, d, color, isKiller = false, isTouch = false) {
    const block = new THREE.Mesh(
        new THREE.BoxGeometry(w, h, d),
        new THREE.MeshLambertMaterial({ color: color })
    );
    block.position.set(x, y, z);
    scene.add(block);

    if (isKiller) {
        killBricks.push(block);
        block.material.emissive = new THREE.Color(0xff0000);
        block.material.emissiveIntensity = 0.5;
    } else {
        objects.push(block);
    }
    if (isTouch) touchParts.push(block);

    // --- NEW: Method Chaining Logic ---
    return {
        mesh: block,
        moveTo: function(targetX, targetY, targetZ, speed = 0.02) {
            block.userData.isMoving = true;
            block.userData.startPos = block.position.clone();
            block.userData.endPos = new THREE.Vector3(targetX, targetY, targetZ);
            block.userData.speed = speed;
            block.userData.alpha = 0; // Movement progress (0 to 1)
            return block; 
        }
    };
}

function buildLevel() {
    createBlock(0, 0, 0, 10, 1, 10, 0x00FF00); // Spawn
    createBlock(0, 0, -12, 4, 1, 4, 0xDDDDDD);
    createBlock(0, 1, -20, 4, 1, 4, 0xDDDDDD);
    createBlock(0, 2, -28, 4, 1, 4, 0xDDDDDD);
    
    const checkpoint = createBlock(0, 2, -40, 10, 1, 10, 0xFFFF00, false, true);
    checkpoint.mesh.userData.message = "Checkpoint reached!"; // Note: we use .mesh here because createBlock returns an object
    
    createBlock(0, 2, -55, 4, 1, 10, 0x333333);
    createBlock(0, 2.6, -55, 4, 0.2, 2, 0xFF0000, true, false); // Lava
    createBlock(0, 3, -70, 4, 1, 10, 0x333333);
    
    // Fixed the color here (0xFF0000 instead of 0xFF000)
    createBlock(0, 0, -73, 4, 1, 4, 0xFF0000).moveTo(0, 10, -73, 0.01);
    
    createBlock(0, 9.7, -93, 6, 1, 30, 0xFF0120, false, true).mesh.userData.message = "Speedway!";
    const speedway_spd = 0.03
    createBlock(3, 11, -83, 1, 3, 5, 0xFF0129, true, false).moveTo(-6, 11, -83, speedway_spd);
    createBlock(-6, 11, -90, 1, 3, 5, 0xFF0129, true, false).moveTo(3, 11, -90, speedway_spd);
    createBlock(0, 11, -109, 0.7,3, 3, 0xfffff, true, false). moveTo(0, 11, -80, speedway_spd);
    createBlock(0, 8, -116, 7, 1, 7, 0xffFFF);
    createBlock(0, 8, -134, 7, 1, 7, 0xAAa12, false, true).mesh.userData.message = "You completed Stage 1: Received 20 Bobux!";
    bv = "Bobux: 20";
}

// --- 8. MAIN LOOP ---
function animate() {
    requestAnimationFrame(animate);

    if (document.activeElement === chatInput) {
        renderer.render(scene, camera);
        return;
    }

    if (isLocked) {
        const delta = 0.015;

        playerVelocity.x -= playerVelocity.x * 10.0 * delta;
        playerVelocity.z -= playerVelocity.z * 10.0 * delta;
        playerVelocity.y -= 30.0 * delta;

        const direction = new THREE.Vector3();
        direction.z = Number(moveForward) - Number(moveBackward);
        direction.x = Number(moveLeft) - Number(moveRight);
        direction.normalize();

        if (moveForward || moveBackward) playerVelocity.z -= direction.z * 150.0 * delta;
        if (moveLeft || moveRight) playerVelocity.x -= direction.x * 150.0 * delta;

        yawObject.translateX(playerVelocity.x * delta);
        yawObject.translateZ(playerVelocity.z * delta);
        yawObject.position.y += playerVelocity.y * delta;

        checkCollisions(delta);
    // --- UPDATE MOVING PLATFORMS ---
scene.traverse((obj) => {
    if (obj.userData.isMoving) {
        // Ping-pong math (moves back and forth)
        obj.userData.alpha += obj.userData.speed;
        
        // Use a Sine wave to make the movement smooth
        const t = (Math.sin(obj.userData.alpha) + 1) / 2;
        
        obj.position.lerpVectors(
            obj.userData.startPos, 
            obj.userData.endPos, 
            t
        );
    }
});

// --- TOUCH DETECTION ---
touchParts.forEach((part) => {
    const partBox = new THREE.Box3().setFromObject(part);
    const playerBox = new THREE.Box3().setFromCenterAndSize(
        yawObject.position, 
        new THREE.Vector3(2, 4, 2)
    );

    if (playerBox.intersectsBox(partBox)) {
        if (!part.userData.touched) {
            part.material.color.set(0xff00ff);
            
            if (part.userData.message) {
                const msg = document.createElement('div');
                // Use .includes() to check for the word Checkpoint
                const isCheckpoint = part.userData.message.includes("Checkpoint");
                const color = isCheckpoint ? "yellow" : "green";
                
                msg.innerHTML = `<span style="color:${color}">[System]: ${part.userData.message}</span>`;
                chatHistory.appendChild(msg);
                chatHistory.scrollTop = chatHistory.scrollHeight;
                
            }
            part.userData.touched = true;
        }
    }
});

        if (yawObject.position.y < -20) resetPlayer();
    }

    renderer.render(scene, camera);
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}