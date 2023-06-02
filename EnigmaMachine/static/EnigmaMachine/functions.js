// The function to encrypt messages
function encrypt(){
    const rotors = `${document.querySelector("#rotor1").value},${document.querySelector("#rotor2").value},${document.querySelector("#rotor3").value}`
    const position = document.querySelector("#rotorsPosition").value
    const plugSetting = document.querySelector("#plugSetting").value
    const plainText = document.querySelector("#plainText").value


    fetch('/Enigma/encryptor', {
        method:"POST",
        body: JSON.stringify({
            rotors : rotors,
            position : position,
            plainText : plainText,
            plugBoard : plugSetting
        })
    })
    .then(response => response.json())
    .then(message => {
        // If the request failed
        if (message["error"] !== undefined){
            console.log(message["error"])
        }
        //Get the cipher text
        else{
            document.querySelector("#encryptedText").innerHTML = message["cipherText"]
        }
    })
    .catch(error => console.log(error))
}



// The function to decrypt messages
function decrypt(messageID){
    toggleEncryptingSection()

    // Scroll down
    window.location.href = "#plainText"

    fetch(`message/${messageID}`)
    .then(response => response.json())
    .then(message => {
        if(message["error"]!==undefined){
            console.log(message["error"])
            }

        // getting all the keys to decrypt the message
        const rotors = message["rotors"].split(",")
        const rotorPositions = message["position"]
        const plugBoardSetting = message["plugSetting"]
        const encryptedMessage = message["content"]

        // Setting the Machine to decrypted message
        document.querySelector("#rotor1").value = rotors[0]
        document.querySelector("#rotor2").value = rotors[1]
        document.querySelector("#rotor3").value = rotors[2]
        document.querySelector("#rotorsPosition").value = rotorPositions
        document.querySelector("#plugSetting").value = plugBoardSetting
        document.querySelector("#plainText").value = encryptedMessage

        encrypt();
        const textArea = document.querySelector("#encryptedText")
        const originalText = document.querySelector("#encryptedText").innerHTML
    })
}




// Get random element from an array
function getRandomElement(array){
    return array[Math.floor(Math.random()*array.length)];
}



// Randomize the setting
function randomizeSetting(){
    const rotors = ["I","II","III","IV","V"]
    const alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


    let plugLength
    do{
        plugLength = Math.floor(Math.random()*26)
    }
    while ((plugLength % 2 !== 0) || plugLength < 2);


    // getting the Plug Setting
    let plugSetting = ""

    for(let i = 0; i<plugLength; i++){
        let character = getRandomElement(alphabet)
        do{
            character = getRandomElement(alphabet)
        } while(plugSetting.includes(character))

        plugSetting += character
    }


    // get the rotor position
    let rotorPosition = ""
    for(let i =0;i<3;i++){
        rotorPosition += getRandomElement(alphabet)
    }

    // Assign the randomize settings
    document.querySelector("#rotor1").value = getRandomElement(rotors)
    document.querySelector("#rotor2").value = getRandomElement(rotors)
    document.querySelector("#rotor3").value = getRandomElement(rotors)
    document.querySelector("#rotorsPosition").value = rotorPosition
    document.querySelector("#plugSetting").value = plugSetting

    document.querySelector("#plugSetting").dispatchEvent(new Event("input"));
    validateAllSettings();
    encrypt();
}