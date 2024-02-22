const wrapper = document.querySelector(".wrapper"),
form = document.querySelector("form"),
fileInp = form.querySelector("input"),
infoText = form.querySelector("p"),
closeBtn = document.querySelector(".close"),
copyBtn = document.querySelector(".copy");

function fetchRequest(file, formData) {
    infoText.innerText = "Scanning QR Code...";

    fetch("http://api.qrserver.com/v1/read-qr-code/", {
        method: 'POST', body: formData
    }).then(res => res.json()).then(result => {
        let qrData = result[0].symbol[0].data;
        infoText.innerText = qrData ? "QR Code Scanned Successfully" : "Couldn't scan QR Code";
        if(!qrData) return;
        document.querySelector("textarea").innerText = qrData;
        form.querySelector("img").src = URL.createObjectURL(file);
        wrapper.classList.add("active");
        speakText(qrData);
    }).catch(() => {
        infoText.innerText = "Couldn't scan QR Code";
    });
}

fileInp.addEventListener("change", async e => {
    let file = e.target.files[0];
    if(!file) return;
    let formData = new FormData();
    formData.append('file', file);
    fetchRequest(file, formData);
});


copyBtn.addEventListener("click", () => {
    let textAreaContent = document.querySelector("textarea").innerText;
    if (textAreaContent) {
        speakText(textAreaContent); // Speak text when copy button is clicked
    }
});
copyBtn.addEventListener("click", () => {
    let textAreaContent = document.querySelector("textarea");
    if (textAreaContent.value) { // Ensure you are using .value for <textarea>
        navigator.clipboard.writeText(textAreaContent.value)
            .then(() => {
                // Optionally, inform the user that the text has been copied.
                console.log("Text copied to clipboard");
                // You can replace console.log with a more user-friendly notification if needed.
            })
            .catch(err => {
                console.error('Failed to copy text: ', err);
            });
    }
});

form.addEventListener("click", () => fileInp.click());
closeBtn.addEventListener("click", () => wrapper.classList.remove("active"));

// Function to speak text
function speakText(text) {
    if ("speechSynthesis" in window) {
        let msg = new SpeechSynthesisUtterance(text);
        speechSynthesis.speak(msg);
    }
}
