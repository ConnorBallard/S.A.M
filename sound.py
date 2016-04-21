import skywriter
from psonic import *
from threading import Thread, Condition

use_synth(HOLLOW)
A = [A4,B4,C4,D4,E4,F4,G4,A5,B5,C5,D5,E5,E5,F5,G5]
B = [D3,E3,F3,G3,A3,B3,C3,D5]
C = [D2,E2,F2,G2]

@skywriter.move()
def spot(x, y, z):
    note_id1 = round(x * 15)
    note_id2 = round(x * 8)
    note_id3 = round(x * 4)
    note1 = A[note_id]
    note2 = B[note_id]
    note3 = C[note_id]
    
def loop_1():
    play(note1, attack = 6, release = 6)
    sleep (z * 10)
    
def loop_2():
    play(note2, attack = 4, release = 5)
    sleep (z * 10 + 2)

def loop_3():
    play(note3, attack = 5, release = 5)
    sleep (z * 10 - 2)

def live_loop_1(condition):
    while True:
        with condition:
            condition.notifyAll() #Message to threads
        loop_1()
            
def live_loop_2(condition):
    while True:
        with condition:
            condition.wait() #Wait for message
        loop_2()

def live_loop_3(condition):
    while True:
        with condition:
            condition.wait() #Wait for message
        loop_3()

condition = Condition()
live_thread_1 = Thread(name='1', target=live_loop_1, args=(condition,))
live_thread_2 = Thread(name='2', target=live_loop_2, args=(condition,))
live_thread_3 = Thread(name='3', target=live_loop_3, args=(condition,))

live_thread_1.start()
live_thread_2.start()
live_thread_3.start()

'''
  live_loop :note1 do
    play choose([:A4,:C5]), attack: 6, release: 6 #THE NOTES ARE VARIABLES DEPENDING ON X POSITION
    sleep 8#SLEEP CHANGES BASED ON Y POSITION
  end

  live_loop :note2 do
    play choose([:E3,:F4]), attack: 4, release: 5 #THE NOTES ARE VARIABLES DEPENDING ON X POSITION
    sleep 10#SLEEP CHANGES BASED ON Y POSITION
  end

  live_loop :note3 do
    play choose([:G4, :B5]), attack: 5, release: 5 #THE NOTES ARE VARIABLES DEPENDING ON X POSITION
    sleep 11#SLEEP CHANGES BASED ON Y POSITION
  end

end
'''
