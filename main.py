import curses
from curses import wrapper
import time
from wonderwords import RandomSentence

def main(scr):
    scr.clear()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    redblack = curses.color_pair(1)
    greenblack = curses.color_pair(2)
    str = "Press any key to start or press esc to exit"
    middle_x = int(round((curses.COLS/2)-20)) #x coord
    horz = int(middle_x - len(str)/20)
    vert = int(round((curses.LINES/2)-2)) #y coord
    scr.addstr(vert,horz,f"{str}")
    scr.refresh()
    inp = scr.getch()
    if inp == 27:
        exit()
    else:
        while True:
            count = -1
            correct = 0
            wrong = 0
            scr.clear()
            s = RandomSentence()
            text = s.sentence() +" "+s.sentence()+" "+s.sentence()
            scr.addstr(f"{text}")
            scr.refresh()
            wpm = 0
            start_time = time.time()
            while True:
                exit = False
                try:
                    if count == len(text)-1:
                        raise IndexError
                    time_elapsed = max(time.time() - start_time, 1)
                    scr.refresh()
                    char = scr.getch()
                    count += 1
                    if char == 8:
                        if count > 1:
                            count -= 1
                            wrong -= 1
                        else:
                            count = 0
                    elif char == 27:
                        exit = True
                        break
                    ord_char = char
                    char = chr(char)
                    if char == text[count]:
                        scr.addstr(0,count,f"{char}",greenblack)
                        correct += 1
                    else:
                        if char != "enter":
                            scr.addstr(0,count,f"{char}",redblack)
                            wrong += 1
                    wpm = ((correct + wrong)/(time_elapsed))*10
                    scr.addstr(1,0,f"Time elapsed: {round(time_elapsed)}s, WPM: {round(wpm)}")
                except IndexError:
                    scr.addstr(0,count,f"\naccuracy = {round((correct/(correct+wrong))*100)}%\ntime = {round(time_elapsed)}\nWPM = {round(wpm)}\npress any key to play again or press esc to exit",greenblack)
                    inp = scr.getch()
                    if inp == 27:
                        exit()
                    else:
                        break
                except Exception as e:
                    print(e)
            if exit:
                break

wrapper(main)
