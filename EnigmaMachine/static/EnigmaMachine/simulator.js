// Sending the message
function sendMessage(isPublic=true,recipient=""){
    const rotors = `${document.querySelector("#rotor1").value},${document.querySelector("#rotor2").value},${document.querySelector("#rotor3").value}`
    const rotorPositions = document.querySelector("#rotorsPosition").value
    const plugBoardSetting = document.querySelector("#plugSetting").value
    const encryptedMessage = document.querySelector("#encryptedText").innerHTML

    fetch('/Enigma/sendMessage', {
        method: "POST",
        body: JSON.stringify({
            isPublic: isPublic,
            recipient: recipient,
            rotors : rotors,
            rotorPositions : rotorPositions,
            plugSetting : plugBoardSetting,
            content : encryptedMessage,
        })
    })
    .then(response => response.json())
    .then(message => {
        // If the request failed
        if (message["error"] !== undefined){
            document.querySelector("#windowAlertMessage").innerHTML = `
            <div class="alert alert-danger alert-dismissible fade show" role="alert">
                <strong>${message["error"]}</strong>
                <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>
            `
        }
        //Alert if the message got sent successfully
        else{
            document.querySelector("#windowAlertMessage").innerHTML = `
            <div class="alert alert-success alert-dismissible fade show" role="alert">
                <strong>${message["message"]}</strong>
                <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                    <span aria-hidden="true">&times;</span>
                </button>
            </div>
            `
        }
    })
    .catch(error => console.log(error))
    .finally(() => {
        setTimeout(document.querySelector("#selectMessageGroup").dispatchEvent(new Event("change")),10);
    })

}


// Function to remove message
function removeMessage(messageID){
    return new Promise((resolve, reject) => {
        fetch(`/Enigma/message/remove/${messageID}`, {method:"POST"})
        .then(res => res.json())
        .then(message => {
            if (message["error"] !== undefined){
                document.querySelector("#messageSectionAlert").innerHTML = `
                <div class="alert alert-danger alert-dismissible fade show" role="alert">
                    <strong>${message["error"]}</strong>
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                `
                window.location.href = "#messageSectionAlert"
                resolve(false)
            }
            else{
                document.querySelector("#messageSectionAlert").innerHTML = `
                <div class="alert alert-success alert-dismissible fade show" role="alert">
                    <strong>${message["message"]}</strong>
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                        <span aria-hidden="true">&times;</span>
                    </button>
                </div>
                `
                window.location.href = "#messageSectionAlert"
                resolve(true)
            }
        })
    })
}


// Render all the public messages
// function loadMessages(group){
//     document.querySelector("#messagesList").innerHTML = "";

//     fetch(`messages/${group}`)
//     .then(response => response.json())
//     .then(messages => messages.forEach(message => {
//         //Rendering each message
//         const element = document.createElement('div')
//         element.className = "list-group-item list-group-item-action flex-column align-items-start"

//         element.innerHTML = `
//         <h5>${message["content"]}</h5><br>
//         <small>${message["timestamp"]}</small><br>
//         <p>Sender: ${message["sender"]}</p>
//         <button type="button" class="m-2 ms-auto btn btn-outline-primary" onclick = "decrypt(${message["id"]})">Decrypt</button>
//         `

//         document.querySelector("#messagesList").append(element)
//     }))

// }


// Toggle sections
function toggleEncryptingSection(){
    document.querySelector('#messagesSection').classList.remove("active");
    document.querySelector('#encryptingSection').classList.add("active");
    document.querySelector("#nav-link-encrypt").classList.add("active", "show");
    document.querySelector('#nav-link-message').classList.remove("active", "show");
}


function toggleMessagesSection(){
    document.querySelector('#encryptingSection').classList.remove("active");
    document.querySelector('#messagesSection').classList.add("active");
    document.querySelector("#nav-link-message").classList.add("active", "show");
    document.querySelector('#nav-link-encrypt').classList.remove("active", "show");
}



