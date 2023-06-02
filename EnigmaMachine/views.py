import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .EnigmaMachine import *
from .models import Message, User


# Create your views here.

def main(request):
  return render(request, "EnigmaMachine/frontPageEnigma.html")



def simulator(request):
  rotors = ["I","II","III","IV","V"]
  return render(request, "EnigmaMachine/simulator.html", {
     "rotors": rotors
  })


@csrf_exempt
def encryptor(request):

  #Reseting the rotor discs
  discs = {
    "I" : Rotors("EKMFLGDQVZNTOWYHXUSPAIBRCJ","Q"),
    "II" : Rotors("AJDKSIRUXBLHWTMCQGZNPYFVOE","E"),
    "III" : Rotors("BDFHJLCPRTXVZNYEIWGAKMUSQO","V"),
    "IV" : Rotors("ESOVPZJAYQUIRHXLNFTGKDCMWB","J"),
    "V" : Rotors("VZBRGITYUPSDNHLXAWMJQOFECK","Z")
  }

  # Encrypting must be via POST
  if request.method != "POST":
      return JsonResponse({"error": "POST request required."}, status=400)
  #Get the posted data
  data = json.loads(request.body)
  rotors = data.get("rotors").split(",")
  rotor_positions = data.get("position").upper()
  plain_text = data.get("plainText").upper()
  plug_settings = data.get("plugBoard").split(" — ")

  #Correct the plug settings
  plug_settings = [setting.upper() for setting in plug_settings]

  KB = KeyBoard()
  PB = PlugBoard(plug_settings)
  Enigma = enigmaMachine(KB,PB,discs[rotors[0]],discs[rotors[1]],discs[rotors[2]],rotor_positions)

  Enigma.setRotors()

  #Create the ciphered string
  cipher_text = ""
  #Encipher each letter in the string.
  for i in plain_text:
    if i.isalpha():
      cipher_text += Enigma.encipher(i)
    else:
      #If not an alphabetical letter, leave it be.
      cipher_text += i

  return JsonResponse({"message": "Text Encrypted Successfully.",
                       "cipherText":cipher_text}, status=201)



@csrf_exempt
def sendMessage(request):
  # Via Post
  if request.method != "POST":
    return JsonResponse({"error": "POST request required."}, status=400)

  data = json.loads(request.body)
  isPublic = data.get("isPublic")
  recipient = data.get("recipient").strip()
  encryptedContent = data.get("content")
  rotors = data.get("rotors")
  plugBoardSetting = data.get("plugSetting")
  rotorPositions = data.get("rotorPositions")


  # Creating a public message
  if isPublic:
    message = Message(
      user = request.user,
      sender = request.user,
      encryptedContent = encryptedContent,
      rotors = rotors,
      plugBoardSetting = plugBoardSetting,
      rotorPositions = rotorPositions,
    )
    message.save()
    return JsonResponse({"message": "Message sent successfully."}, status=201)

  # Creating a message with a recipient
  if len(recipient) == 0:
    return JsonResponse({"error": "Private Message must have one recipient."}, status=400)
  try:
    recipientUser = User.objects.get(username=recipient)
  except User.DoesNotExist:
    return JsonResponse({"error": f"User {recipient} doesn't exist."}, status=400)
  # Actually creating the message
  message = Message(
      user = request.user,
      sender = request.user,
      encryptedContent = encryptedContent,
      rotors = rotors,
      plugBoardSetting = plugBoardSetting,
      rotorPositions = rotorPositions,
      public = isPublic,
      recipient = recipientUser,
    )
  message.save()

  return JsonResponse({"message": "Message sent successfully."}, status=201)



@csrf_exempt
def viewMessages(request,group):
  # Get the messages specific to a group
  if group == "public":
    messages = Message.objects.filter(
      public = True,
    )
  elif group == "private":
    messages = Message.objects.filter(
      public = False,
    )
  # In The "sent" group, if user is not logged in, return an empty json
  elif group == "sent":
    if not request.user.is_authenticated:
     return JsonResponse([],safe=False)
    messages = Message.objects.filter(
      sender = request.user,
     )
    #Messages fowared to the current user.
  elif group == "me":
    if not request.user.is_authenticated:
      return JsonResponse([], safe=False)
    messages = Message.objects.filter(
      recipient = request.user,
    )
# All messages
  elif group == "all":
     messages = Message.objects.all()
  else:
    return JsonResponse({"error": "Invalid group."}, status=400)


  # Return emails in reverse chronologial order
  messages = messages.order_by("-timestamp").all()
  return JsonResponse([message.serialize() for message in messages], safe=False)



@csrf_exempt
def message(request, messageID):
  # Query for requested message
  # Query if the message is public
  try:
    message = Message.objects.get(public=True, pk=messageID)
  except Message.DoesNotExist:
    # If it is not public, the message is only available for the specified users
    try:
        message = Message.objects.get(user=request.user, pk=messageID)
    except Message.DoesNotExist:
      # If the user is the recipient
      try:
        message = Message.objects.get(recipient=request.user, pk=messageID)
      except Message.DoesNotExist:
        return JsonResponse({"error": "Email not found."}, status=404)

  # Return email contents
  if request.method == "GET":
      return JsonResponse(message.serialize())



#remove messages
@csrf_exempt
def removeMessage(request, messageID):
  message = Message.objects.get(id = messageID)
  if request.method != "POST":
    return JsonResponse({"error": "POST request required."}, status=400)

  # Check if the user have the right to remove
  if request.user.id != message.user.id:
    return JsonResponse({"error":"You do not have the permission to remove this message."}, status=400)

  # Removing
  Message.objects.get(user=request.user, id=messageID).delete()
  return JsonResponse({"message": "Message removed successfully."}, status=201)

