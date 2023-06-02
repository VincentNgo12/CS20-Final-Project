# Program name: Newbie Enigma Implementation

# Student name: Vincent Ngo

# Date: 03/04/2023

# Program Description: My implementation of the Enigma Machine used by the German Military in WWII to encrypt their message. My implementation of the Enigma lacks features and is not 100% accurate like the real model.

#This coolest part about this machine is that you can use it to encrypt as well as decrypt messages. You can try on your own.

#Python doesn't allow me to define a costant variable so I'll stick with this way.
ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

#Createing the main() fucntion like ussual. We should go over its constituent functions first before actually reading this main() function.
def main():
  #Introduce the user to input the initial setting of the machine
  print("Enter your Plug Board settings (2 characters each), press enter when done: ")
  PlugSetting = getPlugBoardSetting("Enter 2 characters: ")
  print("Enter your Rotors setting (3 character)")
  RotorsSetting = getRotorsSetting("Enter 3 characters: ")
  #Create the KeyBoard class and the PlugBoard class.
  KB = KeyBoard()
  PB = PlugBoard(PlugSetting)
  #Create the Enigma Machine based off the setting user provided
  Enigma = enigmaMachine(KB,PB,I,II,III,RotorsSetting)
  #Set the rotors
  Enigma.setRotors()
  #Get the text the user want to enchiper
  text = input("Enter text: ").upper()
  #Create the ciphered string
  cipher = ""
  #Encipher each letter in the string.
  for i in text:
    if i.isalpha():
      cipher += Enigma.encipher(i)
    else:
      #If not an alphabetical letter, leave it be.
      cipher += i
  #Print the ciphered string.
  print(f"Ciphered string: {cipher}")


#My first function come to the play, findIndex of a character in a string. It takes 2 parameters.
def findIndex(character,alpha):
  #Irritate through the length of the given string.
  for i in range(len(alpha)):
      #If the character is the character of the string in that index, return the index number.
      if character == alpha[i]:
        return i


#I'll be using classes(objects) in Python, which is essentially defining new data types with unique methods and attributes(data).
#Here I create a class call KeyBoard.
class KeyBoard:
  #All functions defined in a class will be methods that can and only can be used with that class, outside of its objects, methods are meaningless.
  #This is giveSignal() method, when given a character it will give the index of that charcter in the ALPHABET constant, leveraging the findIndex function.
  def giveSignal(self,character):
    return findIndex(character,ALPHABET)
  #This is backward, takt the index and return its character in the ALPHABET constant.
  def receiveSignal(self, signal):
    return ALPHABET[signal]


#Create another class, PlugBoard which implement an important component of the Enigma Machine, it switchs pairs of charcter to eacher other.
class PlugBoard:
  #This function __init__ use to initialize the class as its defined. This means the PlugBoard class takes 1 parameter (switchPairs) when created, "self" is refering to the class itself.
  def __init__(self,switchPairs):
    #switchPairs is provided as a list of pairs of characters.
    #We create a class atribute that is the alphabet and another atribute to record the previous scrambled alphabet.
    self.substituded = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    prevSubstitution = self.substituded
    #Iterrate through the list and start switching pairs.
    for pair in switchPairs:
      #Get the pairs letters and their indexes
      letter1 = pair[0]
      letter2 = pair[1]

      index1 = findIndex(letter1,prevSubstitution)
      index2 = findIndex(letter2,prevSubstitution)

      #Python strings are immutable(I can't substitute letters directly through its index) so I have to use string concatenation and slices to achive the same goal.
      self.substituded = prevSubstitution[:index2]+letter1+prevSubstitution[index2+1:]
      self.substituded = self.substituded[:index1] + letter2 + self.substituded[index1+1:]
      #Record the scrambled string in the prevSubstitution variable
      prevSubstitution = self.substituded

  #Define the fowardSignal method, takes one index, find its letter on the ALPHABET, get the index of that letter in the scrambled string and return it.
  def forwardSignal(self,signal):
    letter = ALPHABET[signal]
    signal = findIndex(letter,self.substituded)
    return signal

  #This method is just backward, get the index of the scrambled string and find and return its index in the ALPHABET.
  def backwardSignal(self,signal):
    letter = self.substituded[signal]
    signal = findIndex(letter,ALPHABET)
    return signal


#The next class is the coolest component in the Enigma Machine.
class Rotors:
  #Initialize the class, it takes 2 parameters when created.
  def __init__(self,wiring,notch):
    #self.wiring is the scramble string and self.alphabet is just the alphabetical string.
    self.alphabet = ALPHABET
    self.wiring = wiring
    #This is the notch, it represent a letter. whenever a rotor rotate to this notch, the next rotor moves.
    self.notch = notch

  #Implement the rotation of the rotors, this method takes 1 parameter.
  def rotate(self,count):
    #Itterate through "count" time.
    for i in range(count):
      #Rotate both the scrambled string and the self.alphabet. Essentially taking the first letter of the string and move it to the end of the string using slices.
      self.wiring = self.wiring[1:]+self.wiring[0]
      self.alphabet = self.alphabet[1:]+self.alphabet[0]

  #This method is used to rotate the rotor until the first letter of its alphabetical string(self.alphabet) is the given letter(1 parameter).
  def rotateToLetter(self,letter):
    #Get the count of the rotations by getting the index of the letter in ALPHABET, and then rotate by that amount.
    count = findIndex(letter,ALPHABET)
    self.rotate(count)


  #forwardSignal and backwardSignal is the exact same as above in the PlugBoard class, no different.
  def forwardSignal(self,signal):
    letter = self.wiring[signal]
    signal = findIndex(letter,ALPHABET)
    return signal

  def backwardSignal(self,signal):
    letter = ALPHABET[signal]
    signal = findIndex(letter,self.wiring)
    return signal


#This will be the last component of the Enigma Machine I will implement. The reflector.
class Reflector:
  #This class takes no parameter, but it will have an attribute that is its scrambled string called self.reflected.
  def __init__(self):
    self.reflected = "EJMZALYXVBWFCRQUONTSPIKHGD"

  #This reflect method takes one signal, take its according letter from the alphabet and extract the index from the letter in self.reflected.
  def reflect(self,signal):
    letter = ALPHABET[signal]
    signal = findIndex(letter,self.reflected)
    return signal


#This getInput will prompt the user for input but only allow alphabetical charcter.
def getInput(prompt):
  while True:
    text = input(prompt)
    #isalpha() method for strings is a boolean expression to determine if it is aplhabetical or not.
    if text.isalpha():
      return text.upper()
    #If user enter nothing, return a blank srting
    elif len(text) == 0:
      return ""
    else:
      print("Alphabetical characters only",end="\n\n")


#This function prompt the user for a list of two charcter strings.
def getPlugBoardSetting(prompt):
  #Create the list
  settings = []
  while True:
    setting = getInput(prompt)
    #Only accept if the prompted string lenght is 2, getInput() will take care of the alphabetical characteristic.
    if len(setting) == 2:
      settings.append(setting)
    elif len(setting) == 0:
      #If the user enter nothing, return the list
      return settings
    else:
      print("Each setting contain 2 characters only")


#This function is used to get the rotors setting for the machine, much like the previous function but only accept a character string.
def getRotorsSetting(prompt):
  while True:
    setting = getInput(prompt)
    if len(setting) == 3:
      return setting
    else:
      print("Rotors setting must contain 3 characters only.")


#This is the historical rotor discs of the Enigma machine, defiene using the Rotors() class I create earlier, taking 2 parameters.
I = Rotors("EKMFLGDQVZNTOWYHXUSPAIBRCJ","Q")
II = Rotors("AJDKSIRUXBLHWTMCQGZNPYFVOE","E")
III = Rotors("BDFHJLCPRTXVZNYEIWGAKMUSQO","V")
IV = Rotors("ESOVPZJAYQUIRHXLNFTGKDCMWB","J")
V = Rotors("VZBRGITYUPSDNHLXAWMJQOFECK","Z")
#Define the Reflector
Reflector = Reflector()


#We now move the Enigma Machine, the heart of the program.
class enigmaMachine:
  #This class takes quite many parameter, all of which are the componenets of the machine defined as objects from earlier.
  def __init__(self,KeyBoard,PlugBoard,Rotor1,Rotor2,Rotor3,Setting):
    #Assign the attributed
    self.KeyBoard = KeyBoard
    self.PlugBoard = PlugBoard
    self.Rotor1 = Rotor1
    self.Rotor2 = Rotor2
    self.Rotor3 = Rotor3
    self.RotorSetting = Setting

  #This method is when we do the enchipering.
  def encipher(self,letter):
    #The Engima machine has three rotors, the right-most rotor rotates everytime the user type a charcter on the machine. When the rotor reaches its "notch", the consecutive rotor rotate once. The mechanism is much like the odometer of the car.
    if self.Rotor3.wiring[0] == self.Rotor3.notch and self.Rotor2.wiring[0] == self.Rotor2.notch:
      self.Rotor1.rotate(1)
      self.Rotor2.rotate(1)
      self.Rotor3.rotate(1)
    elif self.Rotor3.wiring[0] == self.Rotor3.notch:
      self.Rotor2.rotate(1)
      self.Rotor3.rotate(1)
    #This is the double stepping effect of the second rotor of the machine, it is unknown if this effect is intentional or not.
    elif self.Rotor2.wiring[0] == self.Rotor2.notch:
      self.Rotor1.rotate(1)
      self.Rotor2.rotate(1)
      self.Rotor3.rotate(1)
    else:
      self.Rotor1.rotate(1)

    #After implementing the rotating mechanism of the machine, we move through the process of the enciphering.
    letter = letter
    #First the letter goes throught the keyboard, get a signal and the signal move through the Plug Board, three rotors, through the reflector and move backward through the rotors, Plug Board and Keyboard to give the enciphered letter to the user.
    signal = self.KeyBoard.giveSignal(letter)
    signal = self.PlugBoard.forwardSignal(signal)
    signal = self.Rotor3.forwardSignal(signal)
    signal = self.Rotor2.forwardSignal(signal)
    signal = self.Rotor1.forwardSignal(signal)
    signal = Reflector.reflect(signal)
    signal = self.Rotor1.backwardSignal(signal)
    signal = self.Rotor2.backwardSignal(signal)
    signal = self.Rotor3.backwardSignal(signal)
    signal = self.PlugBoard.backwardSignal(signal)
    return self.KeyBoard.receiveSignal(signal)


  #This method is the initialize the rotors of the machine based off the setting the user provided.
  def setRotors(self):
    self.Rotor1.rotateToLetter(self.RotorSetting[0])
    self.Rotor2.rotateToLetter(self.RotorSetting[1])
    self.Rotor3.rotateToLetter(self.RotorSetting[2])

#Call the main() function only when the program is the main program. This promgram could be imported in other programs that I might use in the future, and the main() function of this program won't be called if i do so.
if __name__ == "__main__":
  main()

