from Interpreter import Interpreter
from Order import *
from SpeechToText import *
from TextToSpeech import *

interpreter = Interpreter('sentence-transformers/paraphrase-xlm-r-multilingual-v1')
order = Order()


def get_response(action, item):
    if action == 1:
        print("Adding " + item + " to your order")
        speak("Adding " + item + " to your order")
        order.add_item(item)
    else:
        print(item + " is " + str(get_price(item)) + " dollars. Would you like to add it to your order?")
        speak(item + " is " + str(get_price(item)) + " dollars. Would you like to add it to your order?")

        usr_input = get_speech_to_text(2)

        response = interpreter.confirm(usr_input)

        if response == 1:
            print("Ok it is now added to your order")
            speak("Ok it is now added to your order")
            order.add_item(item)
        else:
            print("Ok, guess you are just curious")
            speak("Ok, guess you are just curious")


if __name__ == '__main__':
    print("Hi, welcome to our AI-assisted drivethru, how can I help you today?")
    speak("Hi, welcome to our AI-assisted drivethru, how can I help you today?")
    while True:
        misunderstood = False
        user_input = get_speech_to_text(5)

        predicted_action, item, predicted_ask = interpreter.interpret(user_input)
        print(predicted_ask)
        speak(predicted_ask)

        # Confirming whether the predicted ask was correct:
        user_input = get_speech_to_text(2)

        confirmation = interpreter.confirm(user_input)

        if confirmation == 1:
            get_response(predicted_action, item)
        else:
            print("I'm sorry for the misunderstanding, can you repeat what you would like again?")
            speak("I'm sorry for the misunderstanding, can you repeat what you would like again?")
            misunderstood = True

        if not misunderstood:
            total = order.get_total()
            if total > 0:
                print("Your total so far is " + str(total) + " dollars. Anything else I can help you with? If not then "
                                                             "please drive up to the window")
                speak("Your total so far is " + str(total) + " dollars. Anything else I can help you with? If not then "
                                                             "please drive up to the window")
            else:
                print("Anything else I can help you with? If not then please drive up to the window")
                speak("Anything else I can help you with? If not then please drive up to the window")
