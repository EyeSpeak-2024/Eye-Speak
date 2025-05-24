import RealtimeSTT as st
from pynput.keyboard import Key, Controller
keyboard = Controller()
import time
import string
import sys
import extra_speech_functions
from playsound import playsound


status = 2

class SpeechKeyboard:
    '''
    takes text input and converts into keystrokes or predefiend key commands
     
    Args:
    
        text: literally just the text you provide lmao
    
    '''
    
    def __init__(self, text):
        self.text = str(text)

    
    
    # commands for texting, uses pynput.keyboard commands
    text_commands = {
        'play': lambda: keyboard.tap(Key.media_play_pause),
        'pause': lambda: keyboard.tap(Key.media_play_pause),
        'volume up': lambda: keyboard.tap(Key.media_volume_up),
        'volume down': lambda: keyboard.tap(Key.media_volume_down),
        'up': lambda: keyboard.tap(Key.up),
        'down': lambda: keyboard.tap(Key.down),
        'right': lambda: keyboard.tap(Key.right),
        'left': lambda: keyboard.tap(Key.left),
        'mute': lambda: keyboard.tap(Key.media_volume_mute),
        'unmute': lambda: keyboard.tap(Key.media_volume_mute),
        'caps lock': lambda: keyboard.tap(Key.caps_lock),
        'scroll up': lambda: keyboard.tap(Key.page_up),
        'scroll down': lambda: keyboard.tap(Key.page_down),
        'enter': lambda: keyboard.tap(Key.enter),
        'forward slash': lambda: keyboard.tap('/'),
        'open tab': lambda: extra_speech_functions.tab(),
        'undo': lambda: extra_speech_functions.undo(),
        'emphasize': lambda: extra_speech_functions.emphasize(),
        'italicize': lambda: extra_speech_functions.italicize(),
        'save file': lambda: extra_speech_functions.save(),
        'select all': lambda: extra_speech_functions.select_all(),
        
        
        }
    
    # commands for gaming, uses pynput.keyboard keystrokes
    game_commands = {
        'w': lambda: keyboard.press('w'),
        'forward': lambda: keyboard.press('w'),
        'a': lambda: keyboard.press('a'),
        'left': lambda: keyboard.press('a'),
        's': lambda: keyboard.press('s'),
        'backwards': lambda: keyboard.press('s'),
        'd': lambda: keyboard.press('d'),
        'right': lambda: keyboard.press('d'),
        'stop': lambda: extra_speech_functions.stop_moving(),
        'space': lambda: keyboard.tap(Key.space),
        'see': lambda: keyboard.tap('c')
 
    }
    

    
    
    def process_texting(self):
  
        # changing status will temrinate program, switch modes, ect.
        global status
        
        # take self.text
        line = str(self.text)
        print(line)
        raw_char = line.lower()
        lower_line = raw_char[:-1]
        
        
        
        if lower_line in self.text_commands:
            cmd = self.text_commands[lower_line]
            cmd()
        
        elif "delete" in lower_line and "characters" in lower_line:
            extra_speech_functions.del_characters(lower_line)
            
        elif "terminate program" in lower_line:
            status = 3
            
        elif "switch modes" in lower_line:
            status = 2
            
        else:
            if "lowercase" in raw_char:
                extra_speech_functions.typing(raw_char[9:])
            else:
                extra_speech_functions.typing(line)

        return line

    def process_game(self):
        global status
        move = False
        
        line = str(self.text)
        print(line)
        raw_char = line.lower()
        lower_line = raw_char[:-1]
        print(lower_line)
        
        
        if lower_line in self.game_commands:
                cmd = self.game_commands[lower_line]
                move = True
                print(move)
                cmd()
                
        elif "switch modes" in lower_line:
            status = 1
            
        else:
            
            for i in range(len(line)):  
                if line[i].isnumeric() or line[i].isalpha() or any(char in string.punctuation for char in line[i]):            
                    keyboard.tap(line[i])
                
        

            
if __name__ == '__main__':

    # # status = 1
    # bol = False
    # use Audio to Text Recorder
    sound = 'ding.mp3'
    with st.AudioToTextRecorder() as recorder:

        print("running!")


        while True and status != 3:
            
            spoke = recorder.text()
            

            text = SpeechKeyboard(spoke)
            
        
            if status == 1:
                print("MODE IS 1")
                text.process_texting()
            elif status == 2:
                print("MODE IS 2")
                text.process_game()
        print("program has been terminated")
        sys.exit()
                

            
                # s = recorder.text(process_texting)
                # # p = recorder.text(s)
                # test = str(s)
                # if not "switch modes" in test.lower():
                #     print(test)
                #     if status == 2:
                #         recorder.text(process_game)
                #     else: continue
                    
                # else:
                #     status = 2
                #     print("mode has bee nswithced") 
                    
                
                    
                        
# MAKE SURE TO REFACTOR AND MAKE TEXTING AND GAMING IS A CLASS

            
            
