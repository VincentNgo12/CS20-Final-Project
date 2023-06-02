//characters for encrypting:
const characters = "ABCDEFGHIJKLNMOPQRSTUVWXYZ";
//Display text element
var encryptedText = document.getElementById("scramblingText");
//Original text
const originalText = document.getElementById("scramblingText").innerHTML;

function encrypter(text,index){
    let encrypted = "";
    //if the index is the same as length dont do anything.
    if (index >= text.length){
        return text;
    }
    //Else copy the prior characters and decrypt from there.
    else{
        encrypted += originalText.slice(0,index);
        for (let i =index;i<text.length;i++){
            encrypted += characters[Math.floor(Math.random()*characters.length)];
        }
        return encrypted;
    }
}

function animation(){
    let count = 0;
    let index = 0;
    let temp =0;
    let interval = setInterval(function(){
        if (count < 30){
            encryptedText.innerHTML = encrypter(originalText,index);
            count++;
        }
        else if(index < (originalText.length-1)){
            encryptedText.innerHTML = encrypter(originalText,index);
            count++;
            temp += 0.2;
            index = Math.floor(temp);
        }
        else if(index === (originalText.length-1)){
            clearInterval(interval);
            encryptedText.innerHTML = originalText;
        }
    },100);
}

function initialize(){
    encryptedText.innerHTML = "";
    initialText = encrypter(originalText,0);
    let index = 0;
    let interval = setInterval(function(){
        if (index < originalText.length){
            encryptedText.innerHTML += initialText[index];
            index++;
        }
        else{
            encryptedText.innerHTML = initialText;
            clearInterval(interval);
        }
    },150);
}
encryptedText.innerHTML = "";
var animationDelayStart = 250*originalText.length;
setTimeout(animation,500+animationDelayStart);
document.addEventListener("DOMContentLoaded", () => setTimeout(initialize,500));