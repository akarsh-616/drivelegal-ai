// =====================================================
// SEND CHAT MESSAGE
// =====================================================

async function sendMessage() {

    let messageInput = document.getElementById("message");

    let message = messageInput.value.trim();

    if (message === "") {
        return;
    }

    let chatBox = document.getElementById("chat-box");

    // Show user message
    chatBox.innerHTML += `
        <div class="user-msg">
            <b>You:</b> ${message}
        </div>
    `;

    // Scroll down
    chatBox.scrollTop = chatBox.scrollHeight;

    try {

        const response = await fetch("/chat", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                message: message
            })
        });

        const data = await response.json();

        // Show bot response
        chatBox.innerHTML += `
            <div class="bot-msg">
                <b>DriveLegal AI:</b><br>
                ${data.reply.replace(/\n/g, "<br>")}
            </div>
        `;

    } catch (error) {

        chatBox.innerHTML += `
            <div class="bot-msg">
                <b>Error:</b> Server not responding.
            </div>
        `;
    }

    // Clear input
    messageInput.value = "";

    // Auto scroll
    chatBox.scrollTop = chatBox.scrollHeight;
}

// =====================================================
// ENTER KEY SUPPORT
// =====================================================

document.addEventListener("DOMContentLoaded", function () {

    document.getElementById("message")
    .addEventListener("keypress", function(event) {

        if (event.key === "Enter") {

            sendMessage();
        }
    });

});

// =====================================================
// DETECT GPS LOCATION
// =====================================================

function detectLocation() {

    if (!navigator.geolocation) {

        alert("Geolocation is not supported on this device.");

        return;
    }

    navigator.geolocation.getCurrentPosition(

        async function(position) {

            let latitude = position.coords.latitude;
            let longitude = position.coords.longitude;

            // Show coordinates
            document.getElementById("latitude").innerText =
                latitude;

            document.getElementById("longitude").innerText =
                longitude;

            try {

                const response = await fetch("/location", {

                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        latitude: latitude,
                        longitude: longitude
                    })
                });

                const data = await response.json();

                document.getElementById("city").innerText =
                    data.city;

                document.getElementById("state").innerText =
                    data.state;

                document.getElementById("country").innerText =
                    data.country;

            } catch (error) {

                alert("Unable to fetch location details.");
            }

        },

        function(error) {

            console.log(error);

            alert("Location permission denied.");
        }
    );
}

// =====================================================
// OCR IMAGE UPLOAD
// =====================================================

async function uploadImage() {

    let imageInput = document.getElementById("imageInput");

    let file = imageInput.files[0];

    if (!file) {

        alert("Please select an image.");

        return;
    }

    let formData = new FormData();

    formData.append("image", file);

    try {

        const response = await fetch("/ocr", {

            method: "POST",

            body: formData
        });

        const data = await response.json();

        document.getElementById("ocr-result").innerHTML =
            `<b>OCR Text:</b><br>${data.text}`;

    } catch (error) {

        document.getElementById("ocr-result").innerHTML =
            "OCR Failed.";
    }
}

// =====================================================
// VOICE INPUT
// =====================================================

function startVoice() {

    if (!('webkitSpeechRecognition' in window)) {

        alert("Voice recognition not supported.");

        return;
    }

    const recognition = new webkitSpeechRecognition();

    recognition.lang = "en-IN";

    recognition.continuous = false;

    recognition.interimResults = false;

    recognition.start();

    recognition.onresult = function(event) {

        let transcript =
            event.results[0][0].transcript;

        document.getElementById("message").value =
            transcript;
    };

    recognition.onerror = function(event) {

        console.log(event);

        alert("Voice recognition failed.");
    };
}