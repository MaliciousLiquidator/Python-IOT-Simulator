import tkinter as tk
from tkinter import ttk
import random

class SmartLight:
    def __init__(self, device_id):
        self.device_id = device_id
        self.status = "off"  
        self.brightness = 0  
        self.color = "white"  

    def turn_on(self):
        self.status = "on"
        self.brightness = 50  

    def turn_off(self):
        self.status = "off"
        self.brightness = 0

    def set_brightness(self, brightness):
        if 0 <= brightness <= 100:
            self.brightness = brightness

    def set_color(self, color):
        self.color = color

    def update_randomly(self):
        self.brightness = random.randint(0, 100)
        self.color = random.choice(["white", "red", "blue", "green", "yellow"])


class Thermostat:
    def __init__(self, device_id):
        self.device_id = device_id
        self.mode = "off"  
        self.current_temperature = 70  
        self.target_temperature = 70

    def set_mode(self, mode):
        if mode in ["off", "heating", "cooling"]:
            self.mode = mode

    def set_target_temperature(self, temperature):
        self.target_temperature = temperature

    def update_temperature(self):
        if self.mode == "heating":
            self.current_temperature += 1
        elif self.mode == "cooling":
            self.current_temperature -= 1

    def update_randomly(self):
        self.target_temperature = random.randint(60, 80)


class SecurityCamera:
    def __init__(self, device_id):
        self.device_id = device_id
        self.motion_detection = False
        self.recording = False

    def enable_motion_detection(self):
        self.motion_detection = True

    def disable_motion_detection(self):
        self.motion_detection = False

    def start_recording(self):
        self.recording = True

    def stop_recording(self):
        self.recording = False

    def detect_motion(self):
        self.motion_detection = random.choice([True, False])

class CentralAutomationSystem:
    def __init__(self):
        self.devices = {} 

    def add_device(self, device):
        self.devices[device.device_id] = device

    def remove_device(self, device_id):
        if device_id in self.devices:
            del self.devices[device_id]

    def get_device(self, device_id):
        return self.devices.get(device_id, None)

    def update_devices(self):
        for device in self.devices.values():
            if isinstance(device, SmartLight) or isinstance(device, Thermostat) or isinstance(device, SecurityCamera):
                device.update_randomly()  

    def simulate(self, duration):
        for _ in range(duration):
            self.update_devices()
            



def create_smart_light_controls(light, parent_frame):
    label = ttk.Label(parent_frame, text=f"Light {light.device_id}: {light.status}, {light.brightness}, {light.color}")
    on_button = ttk.Button(parent_frame, text="On", command=lambda: [light.turn_on(), update_gui()])
    off_button = ttk.Button(parent_frame, text="Off", command=lambda: [light.turn_off(), update_gui()])
    
    label.grid(row=0, column=0, sticky=tk.W)
    on_button.grid(row=0, column=1)
    off_button.grid(row=0, column=2)



def create_thermostat_controls(thermostat, parent_frame):
    label = ttk.Label(parent_frame, text=f"Thermostat {thermostat.device_id}: {thermostat.mode}, Current: {thermostat.current_temperature}, Target: {thermostat.target_temperature}")
    mode_combobox = ttk.Combobox(parent_frame, values=["off", "heating", "cooling"])
    mode_combobox.set(thermostat.mode)
    set_mode_button = ttk.Button(parent_frame, text="Set Mode", command=lambda: [thermostat.set_mode(mode_combobox.get()), update_gui()])
    set_temp_spinbox = ttk.Spinbox(parent_frame, from_=60, to=80)
    set_temp_button = ttk.Button(parent_frame, text="Set Temp", command=lambda: [thermostat.set_target_temperature(int(set_temp_spinbox.get())), update_gui()])

    label.grid(row=0, column=0, sticky=tk.W)
    mode_combobox.grid(row=0, column=1)
    set_mode_button.grid(row=0, column=2)
    set_temp_spinbox.grid(row=0, column=3)
    set_temp_button.grid(row=0, column=4)


def create_security_camera_controls(camera, parent_frame):
    label = ttk.Label(parent_frame, text=f"Camera {camera.device_id}: Motion Detection - {'On' if camera.motion_detection else 'Off'}, Recording - {'On' if camera.recording else 'Off'}")
    motion_button = ttk.Button(parent_frame, text="Toggle Motion Detection", command=lambda: [camera.enable_motion_detection() if not camera.motion_detection else camera.disable_motion_detection(), update_gui()])
    record_button = ttk.Button(parent_frame, text="Toggle Recording", command=lambda: [camera.start_recording() if not camera.recording else camera.stop_recording(), update_gui()])

    label.grid(row=0, column=0, sticky=tk.W)
    motion_button.grid(row=0, column=1)
    record_button.grid(row=0, column=2)


def update_interaction_panel(device):
    for widget in interaction_frame.winfo_children():
        widget.destroy()

    if isinstance(device, SmartLight):
        create_smart_light_controls(device, interaction_frame)
    elif isinstance(device, Thermostat):
        create_thermostat_controls(device, interaction_frame)
    elif isinstance(device, SecurityCamera):
        create_security_camera_controls(device, interaction_frame)

def on_device_select(event):
    try:
        index = device_listbox.curselection()[0]
        device_id = device_listbox.get(index)
        selected_device = central_system.get_device(device_id)
        update_interaction_panel(selected_device)
    except IndexError:
        pass

def update_device_list():
    device_listbox.delete(0, tk.END)
    for device_id in central_system.devices:
        device_listbox.insert(tk.END, device_id)

def update_gui():
    update_device_list()
    for widget in interaction_frame.winfo_children():
        widget.destroy()

root = tk.Tk()
root.title("Smart Home Automation System")

main_frame = ttk.Frame(root, padding="10")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

monitoring_frame = ttk.Frame(main_frame, padding="10")
monitoring_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

interaction_frame = ttk.Frame(main_frame, padding="10")
interaction_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))

device_listbox = tk.Listbox(monitoring_frame)
device_listbox.bind('<<ListboxSelect>>', on_device_select)
device_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

central_system = CentralAutomationSystem()
central_system.add_device(SmartLight("Light1"))
central_system.add_device(Thermostat("Thermostat1"))
central_system.add_device(SecurityCamera("Camera1"))

update_gui()

root.mainloop()

