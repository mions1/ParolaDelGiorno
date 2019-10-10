# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response


from bs4 import BeautifulSoup
from selenium import webdriver
import urllib.request

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Ciao, chiedimi la parola del giorno"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class MainIntentHandler(AbstractRequestHandler):
    """Handler for Main Intent"""
    
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("MainIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        word, mean = self.main()
        speak_output = "La parola di oggi è: "+word
        speak_output += "\nChe significa: "+mean
        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )
    
    def main(self):
        #-----------ZANICHELLI for word
        url = "https://dizionaripiu.zanichelli.it/cultura-e-attualita/le-parole-del-giorno/parola-del-giorno/"
        source = self.get_source(url)
        main_source = self.get_main_source(source)
        opt_main_source = self.delete_more_digit(self.special(self.delete_tag(main_source)))
        
        word = self.get_word(opt_main_source)
        #------------TRECCANI for meaning
        url = "http://www.treccani.it/vocabolario/"+word+"/"
        source = self.get_source(url)
        main_source = self.get_main_source(source, "treccani")
        
        mean = self.get_meaning(self.delete_tag(main_source), "treccani")
        
        return word, mean
    
    def delete_tag(self, txt):
        tmp = ""
        start = False
        for c in txt:
            if c == "<":
                start = True
                continue
            if c == ">":
                start = False
                continue
            if start == False:
                tmp += c
        return tmp

    def special(self, txt):
        txt = txt.replace("&ograve;", "ò")
        txt = txt.replace("&egrave;", "è")
        txt = txt.replace("&igrave;", "ì")
        txt = txt.replace("&ugrave;", "ù")
        return txt
    
    def delete_more_digit(self, txt):
        i = 0
        last_digit = None
        tmp_txt = ""
        
        for c in txt:
            if c.isdigit():
                i += 1
                last_digit = c
            else:
                if i == 1:
                    tmp_txt += last_digit
                tmp_txt += c
                i = 0
            
        return tmp_txt
                
    def get_source(self, url):
        with urllib.request.urlopen(url) as response: 
            source = response.read().decode('utf-8')
        return source
    
    def get_main_source(self, source, src="zanichelli"):
        main_start = main_end = ""
        
        if src == "zanichelli":
            main_start = '<div class="main-content light-txt">'
            main_end = '</div>'
        elif src == "treccani":
            main_start = '<!-- module article full content -->'
            main_end = '<!-- end module -->'
        
        main_source = source[source.index(main_start):(source[source.index(main_start):]).index(main_end)+len(source[:source.index(main_start)])+len(main_end)]
        return main_source
        
    
    def get_word(self, main_source):
        word_start = 'La parola di oggi è: '
        word_end = '\n'
        i = 2 if main_source.index(word_end) == 1 else 1
        word = main_source[main_source.index(word_start)+len(word_start):main_source.index(word_end,i)]
        return word
    
    def get_meaning(self, main_source, src="zingarelli"):
        special_char = ["|",";",".","(","[","#"]
        mean = ""
        if src == "zingarelli":
            main_start = '1 '
            tmp = main_source[main_source.index(main_start)+len(main_start):]
            for c in tmp:
                if c in  special_char:
                    break
                mean += c
        elif src == "treccani":
            trattino = upper = False
            for c in main_source:
                if trattino:
                    if upper:
                        if c in special_char:
                            break
                        mean += c
                    elif c.isupper():
                        upper = True
                        mean += c
                elif "–" in c:
                    trattino = True
        
        return mean

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Puoi chiedermi quale è la parola del giorno"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = ""

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Scusami, c'è stato un problema"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(MainIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
