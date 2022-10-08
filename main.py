import curses
from curses import wrapper
from math import ceil
import time
from wonderwords import RandomSentence

def main(scr):
    scr.clear()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    redblack = curses.color_pair(1)
    greenblack = curses.color_pair(2)
    str = "Press any key to start or press esc to exit" #First screen
    middle_x = int(round((curses.COLS/2)-20)) #x coord
    horz = int(middle_x - len(str)/20)
    vert = int(round((curses.LINES/2)-2)) #y coord
    scr.addstr(vert,horz,f"{str}")
    str = "Pressing any number key will give the corrosponding no. of sentences" #First screen
    middle_x = int(round((curses.COLS/2)-31)) #x coord
    horz = int(middle_x - len(str)/20)
    vert = int(round((curses.LINES/2)-2)) #y coord
    scr.addstr(vert+1,horz,f"{str}")
    scr.refresh()
    inp = scr.getch()
    if inp == 27:
        exit() #exit on esc
    else: #countinue on any other key
        while True:
            count = -1 #setting parameters
            correct = 0
            wrong = 0
            scr.clear()
            s = RandomSentence() #putting the module class in a var
            try:
                no = int(chr(inp))
                text = ""
                for i in range(no):
                    text += s.sentence() + " "
            except Exception as e:
                text = s.sentence() +" "+s.sentence()+" "+s.sentence() #generation of 3 random sentences
            scr.addstr(f"{text}")
            scr.refresh()
            scr.move(0,0) #bringing cursor as starting
            wpm = 0 #setting more parameters
            timer = 0
            vertical = 0
            while True:
                exit = False
                try:
                    if count == len(text)-1: #finishing when user hits the end of sentences
                        raise IndexError #using Index error to provide an ending
                    if count+2 > curses.COLS: #support for multiple lines
                        vertical = 1
                    elif count+2 > 2*curses.COLS:
                        vertical = 2
                    elif count+2 > 3*curses.COLS:
                        vertical = 3
                    scr.refresh()
                    char = scr.getch()
                    skip = False
                    if not timer:
                        start_time = time.time() #time for WPM and time elapsed :shrug:
                        timer+=1
                    time_elapsed = max(time.time() - start_time, 1)
                    count += 1
                    if char == 8: #handling backspaces
                        if count > 1 and count < 3:
                            count = 2
                            scr.move(0,count+1)
                        if count > 2:
                            count -= 2
                            wrong -= 1
                            scr.move(vertical,count-(vertical*curses.COLS)+4)
                        else:
                            count = -1
                            scr.move(0,count+1)
                    elif char == 27: #handling esc
                        exit = True
                        break
                    elif char == 260: #handling left arrow key
                        count -= 2
                        skip = True
                        scr.move(0,count+1)
                    elif char == 261: #handling right arrow key
                        count += 0
                        skip = True
                        scr.move(0,count+1)
                    if not skip:
                        char = chr(char) #converts input from ASCII value to normal key
                        if char == text[count]: #comarision with actual text
                            scr.addstr(vertical,count-(vertical*curses.COLS),f"{char}",greenblack)
                            scr.move(vertical,count-(vertical*curses.COLS)+1)
                            correct += 1
                        else:
                            if char != "enter":
                                scr.addstr(vertical,count-(vertical*curses.COLS),f"{char}",redblack) #Mistakes on wrong keypresses
                                scr.move(vertical,count-(vertical*curses.COLS)+1)
                                wrong += 1
                    wpm = (correct/time_elapsed)*12 #calculating WPM
                    actual_vert = ceil((len(text)/curses.COLS))
                    scr.addstr(actual_vert,0,f"Time elapsed: {round(time_elapsed)}s, WPM: {round(wpm)}") #Info to be shown while typing
                    scr.move(vertical,count-(vertical*curses.COLS)+1)
                except IndexError:
                    scr.addstr(actual_vert,0,f"time = {round(time_elapsed)}\nWPM = {round(wpm)}\npress any key to play again or press esc to exit")#Info after done typing
                    inp = scr.getch() #handling key presses after done
                    if inp == 27: #esc key handling
                        exit()
                    else:
                        break
                except Exception as e: #in case of any other exception (mainly for debugging)
                    #print(e)
                    pass
            if exit:
                break

wrapper(main)
