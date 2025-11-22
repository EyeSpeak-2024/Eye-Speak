#   day 67 of spending a night on this fuckass file
#   i should have never tried to revamp this ui for the third time
#   September 6th, 2025 | 3:06 AM
import tkinter as tk
import pyaudio
import customtkinter as ctk
from PIL import Image, ImageTk
import cv2
import threading
import multiprocessing
import speech
import config
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"



class GUI: # Gooey
    def __init__(self, master):
        # Window Setup -------------------------------------------------
        self.master = master
        self.frame = tk.Frame(self.master, bg="#fbfbfb")
        # self.frame.grid(sticky="nsew")
        self.frame.place(x=0, y=0, relwidth=1, relheight=1)
        self.master.resizable(False, False)

        #   makes the screen not take up your entire screen lmao
        self.screen_width = config.SCREEN_WIDTH
        self.screen_height = config.SCREEN_HEIGHT
        self.master.geometry(f"{self.screen_width}x{self.screen_height}")

        def close():
            speech.stop()
            self.master.destroy()

        # Grid Layout -------------------------------------------------
        #   this creates the entire grid format for the ui
        # for i in range(12):
        #     self.frame.columnconfigure(i, weight=1, uniform='a')
        #     self.frame.rowconfigure(i, weight=1, uniform='a')
            # BRO THIS SHIT WAS SO USELESS, WHAT'S THE POINT IN TRYING TO BE A GOOD FRONTEND DEV WHEN THE RESPONSIVE ASPECT DOESN'T WORK RAAAA

        # Fonts -------------------------------------------------
        self.lsp_titles = ctk.CTkFont(family="League Spartan SemiBold", size=19)
        self.lsp_text = ctk.CTkFont(family="League Spartan Regular", size=15)

        # Background Setup -------------------------------------------------
        self.bg_base = Image.open("images/background.png")
        self.bg_canvas = tk.Canvas(self.frame, width=self.screen_width, height=self.screen_height, highlightthickness=0)
        self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)

        self.bg_img = ImageTk.PhotoImage(self.bg_base.resize((self.screen_width, self.screen_height), Image.LANCZOS))
        self.bg_canvas.create_image(0, 0, anchor="nw", image=self.bg_img)

        # Title -------------------------------------------------
        self.eyespeak = ctk.CTkImage(
            light_image=Image.open("images/title_transp.png"),
            dark_image=Image.open("images/title_transp.png"),
            size=(448*0.5, 76*0.5)
        )
        self.title = ctk.CTkLabel(self.frame, image=self.eyespeak, text=None, fg_color="#fbfbfb", bg_color="#fbfbfb")
        # self.title.grid(column=0, row=0, columnspan=1, sticky="ns")
        self.title.place(x=15, y=30)

        def get_microphones():
            p = pyaudio.PyAudio()
            mic_list = []
            for i in range(p.get_device_count()):
                device_info = p.get_device_info_by_index(i)
            if (
                device_info.get("maxInputChannels", 0) > 0
                and device_info.get("hostApi") == p.get_host_api_info_by_index(device_info.get("hostApi"))["index"]
                and device_info.get("name") not in mic_list
            ):
                mic_list.append(device_info.get("name"))
            p.terminate()
            return mic_list
        
        def get_cameras():
            # Returns a list of available camera indices
            index = 0
            arr = []
            while True:
                cap = cv2.VideoCapture(index)
                if not cap.isOpened():
                    cap.release()
                    break
                arr.append(f"Camera {index}")
                cap.release()
                index += 1
                return arr

        #  Slider creator because i'm like REALLY lazy asf --------------------------------------------------------------------------
        def createSlider(variable, f, t, steps, width):
            slider = ctk.CTkSlider(
                self.frame,
                from_= f,
                to= t,
                number_of_steps= steps,
                variable= variable,
                width= width,
                fg_color="#d8d8d8",
                bg_color="#fbfbfb",
                progress_color="#5AB17D",
                button_color="#38915C",
                hover=False,
                border_width=10,
                border_color="#d8d8d8",
            )
            return slider

        def createText(text:str, color):
            txt = ctk.CTkLabel(
                self.frame,
                text = text,
                text_color=color,
                font=self.lsp_titles,
                fg_color="#fbfbfb"
            )
            return txt
        
        def createDropdown(variable, values, width):
            dropdown = ctk.CTkOptionMenu(
                self.frame,
                variable=variable,
                values=values,
                fg_color="#d8d8d8",
                bg_color="#fbfbfb",
                button_color="#d8d8d8",
                button_hover_color="#d8d8d8",
                dropdown_fg_color="#d8d8d8",
                dropdown_text_color="#000000",
                font=self.lsp_text,
                text_color="#000000",
                width=width,
                height=30,
                corner_radius=20
            )
            return dropdown
        


        # Audio device dropdown -------------------------------------------------
        self.cam_device = tk.StringVar()
        self.cam_device.set("Default Camera Device")
        self.cam_text = createText("Video Device", "#000000")
        self.cam_dropdown = createDropdown(self.cam_device, get_cameras(), 590)
        self.cam_text.place(x=30, y=520)
        self.cam_dropdown.place(x=20, y=550)
        # Red Circle Size -------------------------------------------------
        config.cursor_size_var = tk.DoubleVar(value=1)
        self.circle_size = createSlider(config.cursor_size_var, 0, 3, 50, 375)
        self.circle_size_text = createText("Cursor Size", "#000000")
        self.circle_size_text.place(x=30, y=590)
        self.circle_size.place(x=245, y=600)
        # Mouse Sensitivity -------------------------------------------------
        config.mouse_sens_var = tk.DoubleVar(value=0.8)
        self.mouse_sens = createSlider(config.mouse_sens_var, 0.3, 1.5, 100, 375)
        self.mouse_sens_text = createText("Mouse Sensitvity", "#000000")
        # self.mouse_sens.grid(column=3, row=1, rowspan=2)
        # self.mouse_sens_text.grid(column=3, row=1, sticky="s", pady=12)
        self.mouse_sens_text.place(x=30, y=620)
        self.mouse_sens.place(x=245,y=630)
        # Capture Strength -------------------------------------------------
        config.capt_str_var = tk.DoubleVar(value=0.6)
        self.capt_str = createSlider(config.capt_str_var, 0, 1, 20, 375)
        self.capt_str_text = createText("Capture Strength", "#000000")
        # self.capt_str.grid(column=3, row=2, rowspan=2)
        # self.capt_str_text.grid(column=3, row=2, sticky="s", pady=25)
        self.capt_str_text.place(x=30, y=650)
        self.capt_str.place(x=245, y=660)


        # Microphone Device Dropdown -------------------------------------------------
        self.micr_device = tk.StringVar()
        self.micr_device.set("Default Input Device")
        self.micr_text = createText("Input Device", "#000000")
        self.micr_dropdown = createDropdown(self.micr_device, get_microphones(), 200)
        self.micr_text.place(x=700, y=90)
        self.micr_dropdown.place(x=700, y=120)
        # Loopback Test -------------------------------------------------
        self.loopback_text = createText("Loopback Test", "#000000")
        self.loopback_text.place(x=700, y=160)
        

        
        # Microphone Volume -------------------------------------------------
        config.micr_vol_var = tk.DoubleVar(value=50)
        self.micr_vol = createSlider(config.micr_vol_var, 0, 100, 100, 375)
        self.micr_vol_text = createText("Input Volume", "#000000")
        self.micr_vol.place(x=915, y=550)
        self.micr_vol_text.place(x=700, y=540)
        # Microphone Sensitivity -------------------------------------------------
        config.micr_sens_var = tk.DoubleVar(value=1)
        self.micr_sens = createSlider(config.micr_sens_var, 0, 1, 20, 375)
        self.micr_sens_text = createText("Microphone Sensitivity", "#000000")
        # self.micr_sens.grid(column=4, row=7, sticky="", columnspan=2)
        # self.micr_sens_text.grid(column=3, row=7, sticky="w", columnspan=1)
        self.micr_sens.place(x=915, y=590)
        self.micr_sens_text.place(x=700,y=580)

        # Toggleables
        self.echo_cancellation = createText("Echo Cancellation", "#000000")
        self.noise_suppression = createText("Noise Suppression", "#000000")
        self.echo_cancellation.place(x=700, y=620)
        self.noise_suppression.place(x=700, y=660)

        # that random text box lmao -------------------------------------------------
        self.test_box = ctk.CTkTextbox(
            self.frame,
            wrap="word",
            fg_color="#d8d8d8",
            text_color="#000000",
            font=self.lsp_text,
            scrollbar_button_color="#545454",
            corner_radius=20,
            width=400, height=410
        )
        # self.test_box.grid(column=4, row=1, sticky="nsew", rowspan=5, columnspan=2, padx=20)
        self.test_box.place(x=915, y=80)

        # The TRASHH -------------------------------------------------
        self.trash = ctk.CTkImage(
            light_image=Image.open("images/delete.png"),
            dark_image=Image.open("images/delete.png"),
            size=(42, 42),
            
        )
        self.delete = ctk.CTkButton(
            self.frame,
            image=self.trash,
            fg_color="#d8d8d8",
            bg_color="#d8d8d8",
            text=None,
            width=42,
            height=42,
            hover=False,
            command=lambda: self.test_box.delete("1.0", "end")
        )
        # self.delete.grid(column=5, row=5, sticky="nw", pady=0)
        self.delete.place(x=1250, y=430)
        
        # temp Camera widget -------------------------------------------------
        self.cam_label = ctk.CTkLabel(self.frame, fg_color="#000000", text="cv2 is loading!", font=self.lsp_text, text_color="#ffffff", width=(320*2), height=(240*1.5))
        self.cam_label.place(x=30, y=80)

        # this will close everything when we close ui
        self.master.protocol("WM_DELETE_WINDOW", close)


# Main ---------------- # i'm maining it ooh yes i'm maining it soo good
def main():
    window = tk.Tk()
    global app
    app = GUI(window)
    window.title("EyeSpeak V2.0")
    window.configure(bg="#fbfbfb")
    window.iconphoto(False, (tk.PhotoImage(file="images/icon.png"))) 
    window.resizable(False, False)
    multiprocessing.freeze_support()
    threading.Thread(target=speech_run, daemon=True).start()
    threading.Thread(target=tracker_run, daemon=True).start()

    window.mainloop()

def speech_run():
    speech.main()
def tracker_run():
    import face_track_v5 as face_track
    f = face_track.FaceControlledMouse(gui_ref=app)
    f.camera_on()

if __name__ == "__main__":
    # multiprocessing.freeze_support()
    # threading.Thread(target=speech_run, daemon=True).start()
    # threading.Thread(target=tracker_run, daemon=True).start()
    main()


    
#   4am, phonk blasting, and a dream

'''stand proud lomax, you were strong'''





'''what is the greatest thing you've ever gooned to
    uh my code?'''