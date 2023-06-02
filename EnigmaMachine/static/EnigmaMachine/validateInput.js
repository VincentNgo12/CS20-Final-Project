// Function to format the Plug Setting input
function formatPlugSetting(event){
    const inputString = event.target.value.toUpperCase().replace(/[^A-Z]/gi, "");
    const formatedString = inputString
                            .replace(/([A-Z]{2})(?=[A-Z])/g, "$1 — ");

    event.target.value = formatedString;
}


// Function to format the Rotor Positions input
function formatRotorPosition(event){
    if (event.target.value.length <= 3){

        event.target.value = event.target.value.toUpperCase().replace(/[^A-Z]/gi, "");

    }
    else{
        event.target.value = event.target.value.slice(0,3)
        return false
    }
}


// Validate on input
document.querySelector("#plugSetting").oninput = () => formatPlugSetting(event);
document.querySelector("#rotorsPosition").oninput = () => formatRotorPosition(event);


// Validating inputs
let rotor1 = document.querySelector("#rotor1");
let rotor2 = document.querySelector("#rotor2");
let rotor3 = document.querySelector("#rotor3");
let plugSetting = document.querySelector("#plugSetting");
let rotorPosition = document.querySelector("#rotorsPosition");

function validateRotorSetting(){
    if(!rotor1.options[rotor1.selectedIndex].disabled && !rotor2.options[rotor2.selectedIndex].disabled && !rotor3.options[rotor3.selectedIndex].disabled){
        rotor1.classList.add("validationSuccess"); rotor2.classList.add("validationSuccess"); rotor3.classList.add("validationSuccess");
        rotor1.classList.remove("validationFailed"); rotor2.classList.remove("validationFailed"); rotor3.classList.remove("validationFailed");
        rotor1.parentElement.parentElement.querySelector(".validationErrorMessage").innerHTML = ""
        return true;
    }else{
        rotor1.classList.remove("validationSuccess"); rotor2.classList.remove("validationSuccess"); rotor3.classList.remove("validationSuccess");
        rotor1.classList.add("validationFailed"); rotor2.classList.add("validationFailed"); rotor3.classList.add("validationFailed");
        rotor1.parentElement.parentElement.querySelector(".validationErrorMessage").innerHTML = "Please configure all three rotors.";
        return false;
    }
}

function validatePlugSetting(){
    if(/^([A-Z]{2})( — [A-Z]{2}){0,}$/gi.test(plugSetting.value)){
        plugSetting.classList.add("validationSuccess");
        plugSetting.classList.remove("validationFailed");
        plugSetting.parentElement.querySelector(".validationErrorMessage").innerHTML = "";
        return true
    }
    else{
        plugSetting.classList.remove("validationSuccess");
        plugSetting.classList.add("validationFailed");
        plugSetting.parentElement.querySelector(".validationErrorMessage").innerHTML = "Please follow the plug setting format (Ex. GH-PO-CK-ZX)"
        return false;
    }
}

function validateRotorPosition(){
    if(/^[A-Z]{3}$/gi.test(rotorPosition.value)){
        rotorPosition.classList.add("validationSuccess");
        rotorPosition.classList.remove("validationFailed");
        rotorPosition.parentElement.querySelector(".validationErrorMessage").innerHTML = "";
        return true;
    }else{
        rotorPosition.classList.remove("validationSuccess");
        rotorPosition.classList.add("validationFailed");
        rotorPosition.parentElement.querySelector(".validationErrorMessage").innerHTML = "Please follow the rotor postion format (Ex. HUY)";
        return false;
    }
}

function validateAllSettings(){
    if(!(validateRotorSetting() && validatePlugSetting() && validateRotorPosition())){
        document.querySelector("#plainText").setAttribute('disabled', 'disabled');
        validateRotorPosition();
        validatePlugSetting();
        validateRotorPosition();
        plugSetting.addEventListener("focusout",validateAllSettings);
        rotorPosition.addEventListener("focusout", validateAllSettings);
        rotor1.addEventListener("focusout",validateRotorSetting);
        rotor2.addEventListener("focusout",validateRotorSetting);
        rotor3.addEventListener("focusout",validateRotorSetting);
    }else{
        document.querySelector("#plainText").removeAttribute('disabled');
    }
}


plugSetting.onfocusout = validatePlugSetting;
rotorPosition.onfocusout = validateRotorPosition;
document.querySelector("#plainText").onclick = validateAllSettings;

