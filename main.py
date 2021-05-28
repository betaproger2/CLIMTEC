# imports libs
import requests
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.switch import Switch
from kivy.uix.slider import Slider
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.gridlayout import GridLayout

Window.clearcolor = (27/255, 27/255, 27/255, 1)
Window.title = 'CLIMTEC Smart recuperator'


class MyApp(App):

    def send_data(self, *args):
        if self.input_pwr_controll_sw.active == True and self.output_pwr_controll_sw == True:
            val = float(self.input_pwr_controll.value)
            val_2 = float(self.output_pwr_controll.value)
            url = f"http://{self.ip.text}/input=False/output=True/in_pwr={str(round(val))}/out_pwr={str(round(val_2))}"
            try:
                requests.get(url=url)
            except:
                print(url)
        elif self.input_pwr_controll_sw.active == True:
            val = float(self.input_pwr_controll.value)
            url = f"http://{self.ip.text}/input=False/output=True/in_pwr={str(round(val))}/out_pwr=0"
            try:
                requests.get(url=url)
            except:
                print(url)
        elif self.output_pwr_controll_sw.active == True:
            val = float(self.output_pwr_controll.value)
            url = f"http://{self.ip.text}/input=False/output=True/in_pwr=0/out_pwr={str(round(val))}"
            try:
                requests.get(url=url)
            except:
                print(url)
        else:
            url = f"http://{self.ip.text}/input=False/output=False/in_pwr=0/out_pwr=0"
            try:
                requests.get(url=url)
            except:
                print(url)

    def recive(self, *args):
        url = f"http://{self.ip.text}/"
        self.recv = requests.get(url).text
        print(self.recv)

    def build(self):
        box = BoxLayout(orientation="vertical", padding=35, spacing=0)

        self.logo = Image(source="img/logo.jpg")
        box.add_widget(self.logo)

        btns_layer = BoxLayout(padding=20, orientation="vertical", spacing=10)
        self.ip = TextInput(background_color=(30/255, 30/255, 30/255), foreground_color=(255/255, 255/255, 255/255), multiline=False)
        self.my_btn = Button(background_down="img/bg.png", background_normal="img/bg.png", text="Device Manager")
        self.submit_btn = Button(text="Send", background_down="img/bg.png", background_normal="img/bg.png")
        btns_layer.add_widget(self.ip)
        # btns_layer.add_widget(self.my_btn)
        btns_layer.add_widget(self.submit_btn)
        self.submit_btn.bind(on_press=self.send_data)
        box.add_widget(btns_layer)

        pwr_input_contrll_layer = GridLayout(cols=3)
        self.input_pwr_controll_label = Label(text="Приток", pos=(0, 0))
        self.input_pwr_controll = Slider(pos=(100, -50), min=0, max=100)
        self.input_pwr_controll_sw = Switch()
        pwr_input_contrll_layer.add_widget(self.input_pwr_controll_label)
        pwr_input_contrll_layer.add_widget(self.input_pwr_controll)
        pwr_input_contrll_layer.add_widget(self.input_pwr_controll_sw)

        self.output_pwr_controll_label = Label(text="Вытяжка", pos=(0, 50))
        self.output_pwr_controll = Slider(pos=(0, 50), min=0, max=100)
        self.output_pwr_controll_sw = Switch()
        pwr_input_contrll_layer.add_widget(self.output_pwr_controll_label)
        pwr_input_contrll_layer.add_widget(self.output_pwr_controll)
        pwr_input_contrll_layer.add_widget(self.output_pwr_controll_sw)
        box.add_widget(pwr_input_contrll_layer)

        sensors_layer = GridLayout(cols=2)

        self.input_pwr_label = Label(text=f"IN PWR - {str(0)}%", font_size=20)
        self.output_pwr_label = Label(text=f"OUT PWR - {str(0)}%", font_size=20)
        sensors_layer.add_widget(self.input_pwr_label)
        sensors_layer.add_widget(self.output_pwr_label)
        box.add_widget(sensors_layer)

        self.input_temp_label = Label(text=f"INPUT - {str(0)}°C", font_size=20)
        self.output_temp_label = Label(text=f"OUTPUT - {str(0)}°C", font_size=20)
        sensors_layer.add_widget(self.input_temp_label)
        sensors_layer.add_widget(self.output_temp_label)
        # humidity
        self.indoor_temp = Label(text=f"INDOOR_TMP - {str(0)}°C", font_size=20)
        self.outdoor_temp = Label(text=f"OUTDOOR_TMP - {str(0)}°C", font_size=20)
        self.indoor_hum = Label(text=f"INDOOR_HUM - {str(0)}%", font_size=20)
        self.outdoor_hum = Label(text=f"OUTDOOR_HUM - {str(0)}%", font_size=20)
        self.indoor_press = Label(text=f"INDOOR_PRS - {str(0)}Pa", font_size=20)
        self.outdoor_press = Label(text=f"OUTDOOR_PRS - {str(0)}Pa", font_size=20)
        sensors_layer.add_widget(self.indoor_temp)
        sensors_layer.add_widget(self.outdoor_temp)
        sensors_layer.add_widget(self.indoor_hum)
        sensors_layer.add_widget(self.outdoor_hum)
        sensors_layer.add_widget(self.indoor_press)
        sensors_layer.add_widget(self.outdoor_press)

        co2_layer = GridLayout(cols=1)
        self.co2 = Label(text=f"CO2 - {str(0)}PPM", font_size=20)
        self.get = Button(text="Get data", background_down="img/bg.png", background_normal="img/bg.png")
        self.get.bind(on_press=self.recive)
        co2_layer.add_widget(self.co2)
        co2_layer.add_widget(self.get)
        box.add_widget(co2_layer)

        return box


if __name__ == "__main__":
    MyApp().run()