import os
import certifi
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.metrics import dp

# ตั้งค่าหน้าจอจำลองแบบมือถือ
Window.size = (360, 640)
Window.clearcolor = (0.05, 0.05, 0.05, 1)

# ฐานข้อมูลภาพยนตร์ 10 เรื่อง (ชี้ไปที่โฟลเดอร์ img/)
movie_db = [
    {"title": "Spider-Man: No Way Home", "poster": "img/spiderman.jpg", "genre": "Action / Sci-Fi", "duration": "148 Min", "synopsis": "Peter Parker's life is turned upside down when his identity is revealed.", "showtimes": ["10:30", "13:45", "17:00", "20:15"]},
    {"title": "Thor: Ragnarok", "poster": "img/thor.jpg", "genre": "Action / Fantasy", "duration": "130 Min", "synopsis": "Thor must race against time to stop the destruction of Asgard.", "showtimes": ["11:00", "14:30", "18:00"]},
    {"title": "A Whisker Away", "poster": "img/whisker.jpg", "genre": "Anime / Romance", "duration": "104 Min", "synopsis": "A girl transforms into a cat to get close to her crush.", "showtimes": ["12:00", "15:15", "19:00"]},
    {"title": "Your Name.", "poster": "img/yourname.jpg", "genre": "Anime / Drama", "duration": "106 Min", "synopsis": "Two teenagers swap bodies in their dreams.", "showtimes": ["11:15", "14:20", "18:45"]},
    {"title": "Iron Man", "poster": "img/ironman.jpg", "genre": "Action / Sci-Fi", "duration": "126 Min", "synopsis": "Tony Stark builds an armored suit to save his life.", "showtimes": ["13:00", "16:30", "20:00"]},
    {"title": "Inception", "poster": "img/inception.jpg", "genre": "Action / Sci-Fi", "duration": "148 Min", "synopsis": "A thief steals secrets through dream-sharing.", "showtimes": ["12:45", "16:00", "19:30"]},
    {"title": "Interstellar", "poster": "img/interstellar.jpg", "genre": "Sci-Fi / Drama", "duration": "169 Min", "synopsis": "Explorers travel through a wormhole in space.", "showtimes": ["11:30", "15:00", "18:30"]},
    {"title": "The Dark Knight", "poster": "img/darkknight.jpg", "genre": "Action / Crime", "duration": "152 Min", "synopsis": "Batman faces his greatest threat: The Joker.", "showtimes": ["14:00", "17:30", "21:00"]},
    {"title": "Avatar: Way of Water", "poster": "img/avatar.jpg", "genre": "Action / Sci-Fi", "duration": "192 Min", "synopsis": "Jake Sully lives with his family on Pandora.", "showtimes": ["10:00", "14:30", "19:00"]},
    {"title": "Demon Slayer", "poster": "img/demonslayer.jpg", "genre": "Anime / Action", "duration": "117 Min", "synopsis": "Tanjiro fights demons on the Mugen Train.", "showtimes": ["10:15", "13:30", "16:45"]}
]

class MovieHomeScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=dp(10), spacing=dp(10))
        header = Label(text="MAJOR CLONE", font_size='26sp', size_hint_y=None, height=dp(60), color=(1, 0.8, 0, 1), bold=True)
        self.layout.add_widget(header)

        self.search = TextInput(hint_text="Search movies...", size_hint_y=None, height=dp(45), multiline=False, background_color=(0.15, 0.15, 0.15, 1), foreground_color=(1, 1, 1, 1))
        self.search.bind(text=self.on_search)
        self.layout.add_widget(self.search)

        self.scroll = ScrollView()
        self.grid = GridLayout(cols=2, spacing=dp(15), size_hint_y=None, padding=dp(5))
        self.grid.bind(minimum_height=self.grid.setter('height'))
        
        self.populate_grid(movie_db)
        self.scroll.add_widget(self.grid)
        self.layout.add_widget(self.scroll)
        self.add_widget(self.layout)

    def populate_grid(self, movies):
        self.grid.clear_widgets()
        for movie in movies:
            box = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(280))
            # ใช้ Image แทน AsyncImage เพื่อโหลดจากไฟล์ในเครื่อง
            img = Image(source=movie["poster"], allow_stretch=True, keep_ratio=True, size_hint_y=0.8)
            btn = Button(text=movie["title"], size_hint_y=0.2, background_normal='', background_color=(0.1, 0.1, 0.1, 1), font_size='12sp')
            btn.bind(on_press=lambda inst, m=movie: self.go_details(m))
            box.add_widget(img); box.add_widget(btn)
            self.grid.add_widget(box)

    def on_search(self, instance, value):
        filtered = [m for m in movie_db if value.lower() in m['title'].lower()]
        self.populate_grid(filtered)

    def go_details(self, movie):
        App.get_running_app().booking_data['movie'] = movie
        self.manager.get_screen('details').update_ui()
        self.manager.current = 'details'

class DetailsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.scroll = ScrollView()
        self.content = BoxLayout(orientation='vertical', size_hint_y=None, padding=dp(20), spacing=dp(15))
        self.content.bind(minimum_height=self.content.setter('height'))
        
        self.img = Image(size_hint_y=None, height=dp(350))
        self.title = Label(font_size='22sp', bold=True, size_hint_y=None, height=dp(40), color=(1, 0.8, 0, 1))
        self.meta = Label(font_size='14sp', size_hint_y=None, height=dp(30), color=(0.7, 0.7, 0.7, 1))
        self.synop = Label(font_size='14sp', size_hint_y=None, halign='left')
        self.show_grid = GridLayout(cols=3, spacing=dp(10), size_hint_y=None)
        
        self.content.add_widget(self.img); self.content.add_widget(self.title)
        self.content.add_widget(self.meta); self.content.add_widget(self.synop)
        self.content.add_widget(Label(text="SHOWTIMES", font_size='16sp', bold=True, size_hint_y=None, height=dp(40)))
        self.content.add_widget(self.show_grid)
        self.scroll.add_widget(self.content)
        
        back_btn = Button(text="BACK", size_hint_y=0.1, background_color=(0.2, 0.2, 0.2, 1), on_press=lambda x: setattr(self.manager, 'current', 'home'))
        self.layout.add_widget(self.scroll); self.layout.add_widget(back_btn)
        self.add_widget(self.layout)

    def update_ui(self):
        movie = App.get_running_app().booking_data['movie']
        self.img.source = movie["poster"]; self.title.text = movie["title"]
        self.meta.text = f"{movie['genre']} | {movie['duration']}"; self.synop.text = movie["synopsis"]
        self.synop.text_size = (Window.width - dp(40), None); self.synop.texture_update()
        self.synop.height = self.synop.texture_size[1]
        
        self.show_grid.clear_widgets()
        for t in movie["showtimes"]:
            btn = Button(text=t, size_hint_y=None, height=dp(45), background_color=(0.3, 0.3, 0.3, 1))
            btn.bind(on_press=lambda inst, time=t: self.go_seats(time))
            self.show_grid.add_widget(btn)

    def go_seats(self, time):
        App.get_running_app().booking_data['time'] = time
        self.manager.get_screen('seats').update_ui(); self.manager.current = 'seats'

class SeatSelectionScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=dp(15), spacing=dp(10))
        self.info_label = Label(text="", font_size='18sp', bold=True, size_hint_y=None, height=dp(50), color=(1, 0.8, 0, 1))
        self.seat_grid = GridLayout(cols=5, spacing=dp(10), size_hint_y=0.6)
        self.seats = []
        
        for row in ['A', 'B', 'C', 'D']:
            for col in range(1, 6):
                seat_id = f"{row}{col}"
                btn = ToggleButton(text=seat_id, background_normal='', background_down='', background_color=(0.2, 0.2, 0.2, 1), size_hint=(None, None), size=(dp(55), dp(55)))
                btn.bind(on_release=self.on_seat_click) 
                self.seat_grid.add_widget(btn); self.seats.append(btn)

        self.total_label = Label(text="Selected: 0 | Total: 0 THB", size_hint_y=0.1, font_size='18sp', bold=True)
        nav = BoxLayout(size_hint_y=0.1, spacing=dp(10))
        self.confirm_btn = Button(text="CONFIRM", background_color=(0, 0.6, 0, 1), disabled=True)
        self.confirm_btn.bind(on_press=self.go_to_ticket)
        back_btn = Button(text="BACK")
        back_btn.bind(on_press=lambda x: setattr(self.manager, 'current', 'details'))
        nav.add_widget(back_btn); nav.add_widget(self.confirm_btn)

        self.layout.add_widget(self.info_label)
        self.layout.add_widget(Label(text="--- SCREEN ---", size_hint_y=None, height=dp(30), color=(0.5, 0.5, 0.5, 1)))
        self.layout.add_widget(self.seat_grid); self.layout.add_widget(self.total_label); self.layout.add_widget(nav)
        self.add_widget(self.layout)

    def update_ui(self):
        app = App.get_running_app()
        if app.booking_data['movie']:
            self.info_label.text = f"{app.booking_data['movie']['title']} ({app.booking_data['time']})"
        app.booking_data['seats'] = []
        for s in self.seats:
            s.state = 'normal'; s.background_color = (0.2, 0.2, 0.2, 1)
        self.total_label.text = "Selected: 0 | Total: 0 THB"; self.confirm_btn.disabled = True

    def on_seat_click(self, instance):
        app = App.get_running_app()
        if instance.state == 'down':
            instance.background_color = (0.8, 0.1, 0.1, 1)
            if instance.text not in app.booking_data['seats']: app.booking_data['seats'].append(instance.text)
        else:
            instance.background_color = (0.2, 0.2, 0.2, 1)
            if instance.text in app.booking_data['seats']: app.booking_data['seats'].remove(instance.text)
        count = len(app.booking_data['seats'])
        self.total_label.text = f"Selected: {count} | Total: {count * 250} THB"
        self.confirm_btn.disabled = (count == 0)

    def go_to_ticket(self, instance):
        self.manager.get_screen('ticket').update_ui(); self.manager.current = 'ticket'

class TicketScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=dp(30), spacing=dp(15))
        self.ticket_box = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        self.movie_lbl = Label(font_size='24sp', bold=True, color=(1, 0.8, 0, 1))
        self.details_lbl = Label(font_size='16sp', halign='center')
        self.ticket_box.add_widget(Label(text="--- MOVIE TICKET ---", color=(0.7, 0.7, 0.7, 1)))
        self.ticket_box.add_widget(self.movie_lbl); self.ticket_box.add_widget(self.details_lbl)
        home_btn = Button(text="BOOK MORE", size_hint_y=0.15, background_color=(0.8, 0.1, 0.1, 1), on_press=self.reset)
        self.layout.add_widget(Label(text="BOOKING SUCCESSFUL!", font_size='22sp', bold=True, color=(0, 1, 0, 1), size_hint_y=0.2))
        self.layout.add_widget(self.ticket_box); self.layout.add_widget(home_btn)
        self.add_widget(self.layout)

    def update_ui(self):
        d = App.get_running_app().booking_data
        self.movie_lbl.text = d['movie']['title']
        self.details_lbl.text = f"Time: {d['time']}\nSeats: {', '.join(d['seats'])}\nTotal Paid: {len(d['seats'])*250} THB"

    def reset(self, x):
        App.get_running_app().booking_data = {'movie': None, 'time': None, 'seats': []}
        self.manager.current = 'home'

class MajorCloneApp(App):
    booking_data = {'movie': None, 'time': None, 'seats': []}
    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(MovieHomeScreen(name='home'))
        sm.add_widget(DetailsScreen(name='details'))
        sm.add_widget(SeatSelectionScreen(name='seats'))
        sm.add_widget(TicketScreen(name='ticket'))
        return sm

if __name__ == '__main__':
    MajorCloneApp().run()