from pynput.keyboard import Key, Controller
from word2num import word2num
import time
import re
import string

keyboard = Controller()


    
def extract_nums(text):
        return re.findall(r'\d+', text)

def del_characters(line):
        x = 0
        nums = extract_nums(line)
        if len(nums) == 0:
            delete = "delete"
            char = "characters"
            new_line = line.replace(delete, "")
            new_line = new_line.replace(char, "")
            print(new_line)
            x = word2num(new_line)
        else:
            x = int(nums[0])
        times = 0
        while (times < x):
                keyboard.press(Key.backspace)
                times += 1
                print("works")
                time.sleep(0.1)

def tab():
        keyboard.press(Key.ctrl)
        keyboard.press('t')
        keyboard.release(Key.ctrl)
        keyboard.release('t')
        
        
       
def undo():
        keyboard.press(Key.ctrl)
        keyboard.press('z')
        keyboard.release(Key.ctrl)
        keyboard.release('z')
        
        
def emphasize():
        keyboard.press(Key.ctrl)
        keyboard.press('b')
        keyboard.release(Key.ctrl)
        keyboard.release('b')
        
        
def italicize():
        keyboard.press(Key.ctrl)
        keyboard.press('i')
        keyboard.release(Key.ctrl)
        keyboard.release('i')
        
        
def save():
        keyboard.press(Key.ctrl)
        keyboard.press('s')
        keyboard.release(Key.ctrl) 
        keyboard.release('s')
        
        
def select_all():
        keyboard.press(Key.ctrl)
        keyboard.press('a')
        keyboard.release(Key.ctrl)
        keyboard.release('a')
        
def forward():
        keyboard.press('w')


        
        
def stop_moving():
        keyboard.release('w')
        keyboard.release('a')
        keyboard.release('s')
        keyboard.release('d')
        
def typing(line):
        for i in range(len(line)):
                if line[i] == '.' or line[i] == '!' or line[i] == '?':
                        keyboard.tap(line[i])
                        keyboard.tap(' ')
                        keyboard.tap(' ')
                        
                elif line[i].isnumeric() or line[i].isalpha() or any(char in string.punctuation for char in line[i]):            
                        keyboard.tap(line[i])
                        
                elif line[i] == ' ':
                        keyboard.tap(Key.space)
