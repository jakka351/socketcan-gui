#coding:utf-8
#################################################################################################################
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, 
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#################################################################################################################
# SOCKET CAN GUI USING PYSIMPLEGUI
#################################################################################################################
'''
    Library Imports
'''
#################################################################################################################
import time, threading, logging, os, sys, datetime, requests, operator, textwrap, can
import PySimpleGUI as sg
from threading import Thread
from datetime import datetime
#################################################################################################################
'''
    Global Variables
'''
#################################################################################################################
CAN_IF   = "vcan0"
CAN_ID   = ""
CAN_DATA = ""
THREAD_EVENT = '-THREAD-'
bus = can.interface.Bus(channel=CAN_IF, bustype='socketcan')
#################################################################################################################
def cansend(CAN_ID,CAN_DATA):
    global bus
    msg = can.Message(arbitration_id=CAN_ID,data=CAN_DATA,extended_id=False)
    bus.send(msg)

def cangen(CAN_ID,CAN_DATA):
    global bus
    msg = can.Message(arbitration_id=CAN_ID,data=CAN_DATA,extended_id=False)
    bus.send(msg)

def candump():
    global bus
    msg = can.Message(arbitration_id=CAN_ID,data=CAN_DATA,extended_id=False)
    bus.send(msg)

def main():
    global bus, CAN_ID, CAN_DATA
    ##########################################
    '''
    Base 64 Image for SocketCANLogo
    '''
    ##########################################
    logo = b'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'
    ##########################################
    '''
    pysimplegui theme setting
    '''
    ##########################################
    sg.theme('black')
    sg.theme_text_color('#0000FF')
    ##########################################
    '''
    main layout
    '''
    ##########################################
    layout = [  [sg.Image(data=logo, 
                          enable_events=True, 
                          background_color='black', 
                          key='-IMAGE-', 
                          right_click_menu=['UNUSED', ['Exit']], 
                          pad=0)],

                [sg.T('    CAN-Utils GUI for Linux SocketCAN Interfaces', 
                    font='Monospace-Bold 12', 
                    text_color='green')],

                [sg.Multiline(size=(120,20), 
                              font='Monospace-Bold 10', 
                              key='-ML-', 
                              autoscroll=True, 
                              reroute_stdout=True, 
                              write_only=True, 
                              reroute_cprint=True)],
               
                [sg.Button('cansend', button_color='green', key='cansend'),  
                 sg.Button('candump', button_color='green', key='candump'),  
                 sg.Button('cansniffer', button_color='green', key='cansniffer'),  
                 sg.Button('cangen', button_color='green', key='cangen'),  
                 sg.Button('      Exit      ', button_color='blue', key='exit')],
                  ]
    '''
    create window
    '''
    window = sg.Window(' can-utils socketcan  ', layout)
    '''
    events handling
    '''
    while True:             # Event Loop
        event, values = window.read()
        sg.cprint(event, values)
        if event == sg.WIN_CLOSED or event == 'Exit':
            break            
        if event.startswith('candump'):
            pass
        if event.startswith('cansend'):
            cansend()
        if event.startswith('cangen'):
            pass
        if event.startswith('cansniffer'):
            pass
        if event.startswith('stop'):
            break
        if event.startswith('exit'):
            break

    window.close()

if __name__ == '__main__':
    main()
#################################################################################################################
