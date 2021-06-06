import cwiid
import time
from mqtt_publisher import Publisher

class Controller:
    
    def __init__(self):
        # Setup Wii-Controller
        self.connect()
        self.wii.rpt_mode = cwiid.RPT_BTN
        
        # Setup MQTT Publisher
        self.mqtt_pub_client = Publisher('localhost', 1883, 'wii', 'wii-controller')
        self.mqtt_pub_client.start()
        
        # Default Vaules (button, alias)
        self.buttons = (
            (cwiid.BTN_LEFT, "down"),
            (cwiid.BTN_RIGHT, "up"),
            (cwiid.BTN_UP, "left"),
            (cwiid.BTN_DOWN, "right"),
            (cwiid.BTN_1, "1"),
            (cwiid.BTN_2, "2"),
            (cwiid.BTN_A, "a"),
            (cwiid.BTN_B, "b"),
            (cwiid.BTN_MINUS, "minus"),
            (cwiid.BTN_HOME, "home"),
            (cwiid.BTN_PLUS, "plus")
        )
        
        self.prevValues = {
            "up": False,
            "down": False,
            "left": False,
            "right": False,
            "a": False,
            "b": False,
            "plus": False,
            "minus": False,
            "home": False,
            "1": False,
            "2": False,
            "position": 125
        }
        
        
    def connect(self):
        print 'Please press buttons 1 + 2 on your Wiimote now ...'
        try:
          self.wii=cwiid.Wiimote()
        except RuntimeError:
          print "Cannot connect to your Wiimote. Run again and make sure you are holding buttons 1 + 2!"
          quit()
          
        print 'Connected to Wii Controller!'
        print 'Press + and - to Disconnect!'
        
        
    def listen(self):
        while True:
            self.changedValues = {}
            buttons = self.wii.state['buttons']
            
            # Detect Button State
            for (button, alias) in self.buttons:
                if (buttons & button):
                    if not self.prevValues[alias]:
                        self.prevValues[alias] = True
                        self.changedValues[alias] = True
                else:
                    if self.prevValues[alias]:
                        self.prevValues[alias] = False
                        self.changedValues[alias] = False

            
            # Detect Position State
            self.wii.rpt_mode = cwiid.RPT_BTN | cwiid.RPT_ACC
            if self.prevValues["position"] != self.wii.state['acc'][1]:
                self.prevValues["position"] = self.wii.state['acc'][1]
                self.changedValues["position"] = self.wii.state['acc'][1]
                
            # If something Changed, Publish the Changed Values
            if len(self.changedValues) > 0:
                self.mqtt_pub_client.publish(self.changedValues)
                
            
            time.sleep(0.05)
                
        
        