import json
import os
import math
import time
import random
import string
import matplotlib.pyplot as plt
import networkx as nx

class Song:
    def __init__(self, name, artist, album, genre, duration):
        #Initialisiert die Song-Instanz mit Name, Künstler, Album, Genre und Dauer
        self.name = name
        self.artist = artist
        self.album = album
        self.genre = genre
        self.duration = duration

    def __str__(self):
         #Gibt eine formatierte String-Repräsentation des Songs zurück
        return f"{self.name} by {self.artist} - Album: {self.album}, Genre: {self.genre}, Duration: {self.duration}"

    def to_dict(self):
        #Wandelt die Song-Instanz in ein Dictionary um
        return {
            "name": self.name,
            "artist": self.artist,
            "album": self.album,
            "genre": self.genre,
            "duration": self.duration
        }

    @staticmethod
    def from_dict(data):
        #Erstellt eine Song-Instanz aus einem Dictionary
        return Song(data['name'], data['artist'], data['album'], data['genre'], data['duration'])
    
    def __lt__(self, other):
        #Überprüft, ob der Name des aktuellen Songs lexikografisch kleiner als der des anderen Songs ist
        return self.name < other.name
    
    def __le__(self, other):
        #Überprüft, ob der Name des aktuellen Songs lexikografisch kleiner oder gleich dem des anderen Songs ist
        return self.name <= other.name
    
    def __gt__(self, other):
         #Überprüft, ob der Name des aktuellen Songs lexikografisch größer als der des anderen Songs ist
        return self.name > other.name

    def __eq__(self, other):
        #Überprüft, ob der Name des aktuellen Songs gleich dem des anderen Songs ist
        return self.name == other.name

class Playlist:
    def __init__(self, name):
        #Initialisiert die Playlist-Instanz mit Name und einer leeren Liste von Songs (Playlist ist anfangs noch nicht gefüllt)
        self.name = name
        self.songs = []

    def add_song(self, song):
         #Fügt einen Song zur Playlist (Liste self.songs) hinzu
        self.songs.append(song)

    def __str__(self):
         #Gibt eine formatierte String-Repräsentation der Playlist und der Anzahl der Songs zurück
        return f"Playlist: {self.name}, Songs: {len(self.songs)}"

    def to_dict(self):
        #Wandelt die Playlist-Instanz in ein Dictionary um, einschließlich der Songs
        return {
            "name": self.name,
            "songs": [song.to_dict() for song in self.songs]
        }

    @staticmethod
    def from_dict(data):
        #Erstellt eine Playlist-Instanz aus einem Dictionary, einschließlich der enthaltenen Songs
        playlist = Playlist(data['name'])
        playlist.songs = [Song.from_dict(song_data) for song_data in data['songs']]
        return playlist

class MusicApp:
    def __init__(self, data_file='music_data.json'):
        #Initialisiert die MusicApp-Instanz mit dem Dateinamen, einer leeren Song- und Playlist-Liste, und der Funktion load_data um Songs & Playlists zu laden
        self.data_file = data_file
        self.songs = []
        self.playlists = []
        self.load_data()

        if not self.songs:
                #Hier wird die Anzahl der generierten Songs angepasst
                print("No songs found in the database. Generating 1000 random songs...")
                self.songs = self.generate_random_songs(1000)
                self.save_data()

    def generate_random_string(self, min_length=3, max_length=10):
        length = random.randint(min_length, max_length)
        return ''.join(random.choices(string.ascii_lowercase, k=length)).capitalize()

    # Funktion zur Generierung einer zufälligen Dauer (zwischen 2.0 und 5.0 Minuten)
    def generate_random_duration(self):
        minutes = random.randint(2, 5)  # Minuten zwischen 2 und 5
        seconds = random.randint(0, 59)  # Sekunden zwischen 0 und 59
        return f"{minutes}:{seconds:02d}"  # Format: "MM:SS"

    # Funktion zur Generierung zufälliger Songs
    def generate_random_songs(self,num_songs):
        songs = []
        for _ in range(num_songs):
            name = self.generate_random_string()  # Zufälliger Name
            artist = self.generate_random_string()  # Zufälliger Künstler
            album = self.generate_random_string()  # Zufälliges Album
            genre = self.generate_random_string()  # Zufälliges Genre
            duration = self.generate_random_duration()  # Zufällige Dauer

            # Erzeuge Song-Objekt
            song = Song(name, artist, album, genre, duration)
            songs.append(song)

        return songs

    def load_data(self):
        #Lädt Songs und Playlists aus der JSON-Datei, falls vorhanden
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                self.songs = [Song.from_dict(song_data) for song_data in data.get('songs', [])]
                self.playlists = [Playlist.from_dict(pl_data) for pl_data in data.get('playlists', [])]
            print("Data loaded successfully.")
        else:
            print("\033[41No data file found. Starting with an empty database.\033[0m")

    def save_data(self):
        #Speichert die aktuelle Liste der Songs und Playlists in einer JSON-Datei
        data = {
            "songs": [song.to_dict() for song in self.songs],
            "playlists": [playlist.to_dict() for playlist in self.playlists]
        }
        
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=4)
        print("\033[41Data saved successfully.\033[0m")
        return 0

    def add_song(self):
        #Fügt einen neuen Song zur Song-Liste (self.songs) hinzu, indem der Benutzer die Details (Name, Artist, Genre, Dauer) eingibt
        print("\033[1m\033[32mHere you can add a new song to the app\033[0m")
        name = input("\033[92mEnter song name: \033[0m")
        artist = input("\033[92mEnter artist name: \033[0m")
        album = input("\033[92mEnter album name: \033[0m")
        genre = input("\033[92mEnter genre: \033[0m")
        duration = input("\033[92mEnter duration (mm:ss): \033[0m")
        song = Song(name, artist, album, genre, duration)
        self.songs.append(song)
        print(f"\033[103mWe added the song with name: {song.name}, artist: {song.artist}, album: {song.album}, genre: {song.genre}, duration: {song.duration} to your app.\033[0m")
        return 0

    def create_playlist(self):
        #Erstellt eine neue Playlist basierend auf dem Benutzereingabe-Namen und fügt sie der Playlist-Liste (self.playlist) hinzu
        print("\033[1m\033[32mHere you can create a new playlist.\033[0m")
        name = input("\033[92mEnter playlist name: \033[0m")
        playlist = Playlist(name)
        self.playlists.append(playlist)
        print(f"\033[103mWe created a playlist with this name: {playlist} for you\033[0m")
        return 0

    def add_song_to_playlist(self):
        #Fügt einen vorhandenen Song zu einer vorhandenen Playlist hinzu, die der Benutzer durch den Playlist Namen angibt
        print("\033[1m\033[32mHere you can add a song to a playlist.\033[0m")
        playlist_name = input("\033[92mEnter the name of the playlist: \033[0m")
        playlist = next((pl for pl in self.playlists if pl.name.lower() == playlist_name.lower()), None)
        if not playlist:
            print(f"\033[103mWe could not find a playlist with this name {playlist_name}.\033[0m")
            return -1

        song_input = input("\033[92mEnter the name of the song to add: \033[0m")
        song = next((song for song in self.songs if song.name.lower() == song_input.lower()), None)
        if not song:
            print(f"\033[103mWe could not find a song with this name: {song_input}.\033[0m")
            return -1

        playlist.add_song(song)
        print(f"\033[103mWe added the song: '{song.name}' to the playlist: '{playlist.name}'.\033[0m")
        return 0

    def analyze_search_algorithm_runtime(self, algorithm, arr, num_runs=None):
        
        # Dynamische Bestimmung der Anzahl der Durchläufe basierend auf der Anzahl der Songs
        if num_runs is None:
            num_runs = max(30, min(100, len(arr) // 10))  # Mindestens 30, maximal 100 Durchläufe


        # Durchschnittsfall: Mehrere Zufallstests
        random_targets = [random.choice(arr).name for _ in range(num_runs)]


        # Durchschnittsfall Laufzeit über mehrere Zufallsziele
        average_times = []
        for target in random_targets:
            start_time = time.time()
            algorithm(song_input=target)
            average_times.append(time.time() - start_time)

        average_case_time = sum(average_times) / len(average_times)

        return {

            "Average Case Time": average_case_time
        }
    
    def searching_alogrithms_to_test(self):
        #Auswahl der verschiedenen Suchalgorithmen
        print("1. Test linear search")
        print("2. Test binary search")
        print("3. Test depth first search")
        print("4. Test breadth first search")
        print("5. Test jump search")
        print("6. Test fibonacci search")
        print("7. Test exponential search")

        option= input("\033[1mChoose your algorithm by number: \033[0m")
        if option == "1":
            results= self.analyze_search_algorithm_runtime(self.linear_search, self.songs)

        elif option == "2":
            sorted_songs= self.quicksort(self.songs)
            results = self.analyze_search_algorithm_runtime(lambda song_input: self.binary_search(arr=sorted_songs, song_input=song_input), sorted_songs)

        elif option == "3":
            tree = self.create_binary_tree(self.songs)
            results = self.analyze_search_algorithm_runtime(lambda song_input: self.depth_first_search(node=tree, song_input=song_input), self.songs)

        elif option == "4":
            tree = self.create_binary_tree(self.songs)
            results = self.analyze_search_algorithm_runtime(lambda song_input: self.breadth_first_search(node=tree, song_input=song_input), self.songs)

        elif option == "5":
            sorted_songs = self.quicksort(self.songs)  
            results = self.analyze_search_algorithm_runtime(lambda song_input: self.jump_search(arr=sorted_songs, song_input=song_input), sorted_songs)

        elif option == "6":
            sorted_songs = self.quicksort(self.songs)  
            results = self.analyze_search_algorithm_runtime(lambda song_input: self.fibonacci_search(arr=sorted_songs, song_input=song_input), sorted_songs)

        elif option == "7":
            sorted_songs = self.quicksort(self.songs)  
            results = self.analyze_search_algorithm_runtime(lambda song_input: self.exponential_search(arr=sorted_songs, song_input=song_input), sorted_songs)
                                                     
        else:
            print("Invalid option selected.")
            return

        if results:
            print("\n\033[1mSummary of Algorithm Runtime\033[0m")
            print(f"Average Case Time: {results['Average Case Time']:.6f} seconds")

    def search_songs_with_algorithms(self):
        #Auswahl der verschiedenen Suchalgorithmen
        print("1. Search with linear search")
        print("2. Search with binary search")
        print("3. Search with depth first search")
        print("4. Search with breadth first search")
        print("5. Search with jump search")
        print("6. Search with fibonacci search")
        print("7. Search with exponential search")
        
        
        option= input("\033[1mChoose your algorithm by number: \033[0m")
        if option == "1":
            self.linear_search()
        elif option == "2":
            self.songs = self.quicksort(self.songs)
            self.binary_search()
        elif option == "3":
            tree= self.create_binary_tree(self.songs)
            self.depth_first_search(node= tree)
        elif option == "4":
            tree= self.create_binary_tree(self.songs)
            self.breadth_first_search(node=tree)
        elif option == "5":
            sorted_songs= self.quicksort(self.songs)
            self.jump_search(arr=sorted_songs)
        elif option == "6":
            sorted_songs= self.quicksort(self.songs)
            self.fibonacci_search(arr=sorted_songs)
        elif option == "7":
            sorted_songs= self.quicksort(self.songs)
            self.exponential_search(arr= sorted_songs)
       


    def linear_search(self, song_input=None):
        arr= self.songs
        # Wenn keine Eingabe (song_input) bereitgestellt wird, fordert das Programm den Benutzer auf, eine Eingabe zu machen
        if song_input is None:
            print("\033[1m\033[32mLinear Search is started\033[0m")
            song_input= input("\033[92mProvide the name of the song you want to search for: \033[0m")
            song_input = song_input.lower()

        #Zeitmessung für die Dauer der Suche
        start_time = time.time()
        # Iteration durch das Array, um das gesuchte Lied zu finden
        # Der lineare Suchalgorithmus vergleicht jedes Song-Objekt im Array mit der Eingabe
        for index, song in enumerate(arr):
            # Wenn der Song gefunden wird (Unterscheidung von Groß- und Kleinschreibung wird ignoriert)
            if song.name.lower() == song_input:
                # Zeitmessung stoppen
                end_time = time.time()
                print(f"\033[103mWe found the song '{song.name}' by {song.artist} - Album: {song.album}, Genre: {song.genre}, Duration: {song.duration} min at index {index}.\033[0m")
                print(f"Search took {end_time - start_time} seconds.")
                return index 
        #Zeitmessung stoppen, wenn der Song nicht gefunden wurde
        end_time = time.time()
        print(f"\033[103mWe could not find a song with the name: {song_input}.\033[0m")
        print(f"Search took {end_time - start_time} seconds.")
        return -1


    def binary_search(self, arr=None, song_input=None, left=None, right=None):
        # Falls kein Array übergeben wurde, wird das Standardarray der Songs verwendet
        if arr is None:
            arr = self.songs
        # Falls ein song_input übergeben wurde, wird geschaut ob der Songname im Array enthalten ist
        if song_input is not None:
            #Zeitmessung gestartet
            start_time = time.time()
            # Suche das entsprechende Song-Objekt anhand des song_input
            song = next((s for s in arr if s.name.lower() == song_input.lower()), None)
            if not song:
                print(f"\033[103mWe could not find a song with the name: {song_input}.\033[0m")
                return -1
        else:
            #Falls kein song_input übergeben wurde, fordert das Programm den Benutzer auf, einen Songnamen einzugeben
            print("\033[1m\033[32mBinary Search is started\033[0m")
            song_input = input("\033[92mProvide the name of the song you want to search for: \033[0m")
            start_time = time.time()
            song = next((s for s in arr if s.name.lower() == song_input.lower()), None)
            if not song:
                print(f"\033[103mWe could not find a song with the name: {song_input}.\033[0m")
                return -1

        #Standardwerte für linke und rechte Begrenzungen (Suchbereich) setzen, falls nicht übergeben
        if right is None:
            right = len(arr) - 1
        if left is None:
            left = 0

        #Durchführung der Binärsuche
        while left <= right:
            #Berechnung des mittleren Indexes
            mid_index = left + (right - left) // 2
            #Wenn gesuchter Song gefunden wurde, wird dies ausgegeben
            if song.name == arr[mid_index].name:
                #Zeitmessung gestoppt
                end_time = time.time()
                print(f"\033[103mA song with the name: {song.name} was found on index {mid_index}.\033[0m")
                print(f"Search took {end_time - start_time} seconds.")
                return mid_index
            elif song.name > arr[mid_index].name:
                left = mid_index + 1
            else:
                right = mid_index - 1

        end_time = time.time()
        print(f"\033[103mWe could not find a song with the name: {song.name}.\033[0m")
        print(f"Search took {end_time - start_time} seconds.")
        return -1



    def create_binary_tree(self, arr):
        if not arr:
            return None
        #Der mittlere Index des Arrays wird berechnet, um das Array in zwei Hälften zu teilen
        mid_index = len(arr) // 2
        #Es wird ein Knoten (Node) erstellt, dessen Wert das mittlere Element des Arrays ist
        #Die linke und rechte Seite des Baumes wird rekursiv mit den Teilarrays erstellt
        node = {
            'value': arr[mid_index],
            'left': self.create_binary_tree(arr[:mid_index]),
            'right': self.create_binary_tree(arr[mid_index + 1:])
        }

        return node
    
    def depth_first_search(self, node, song_input=None, path=None, first_call=True, index=0, start_time=None):
        if first_call:
            print("\033[1m\033[32mDepth First Search is started\033[0m")

            #Falls kein song_input übergeben wurde, fordert das Programm den Benutzer auf, einen Songnamen einzugeben
            if song_input is None:
                song_input = input("\033[92mProvide the name of the song you want to search for: \033[0m")
            
            #Zeitmessung starten
            start_time = time.time()

        # Suche das Song-Objekt basierend auf dem Namen
        song = next((song for song in self.songs if song.name.lower() == song_input.lower()), None)
        if not song:
            print(f"\033[103mWe could not find a song with the name: {song_input}.\033[0m")
            return -1

        #Initialisierung des Pfads, falls nicht vorhanden
        if path is None:
            path = []

         #Wenn der aktuelle Knoten None ist, kehrt die Funktion zurück (Basisfall)
        if node is None:
            return None

        #Namen des aktuellen Knotens wird zum Pfad hinzugefügt
        if node['value'] is not None:
            path.append(node['value'].name)
        else:
            return None

        #Wenn der gesuchte Song gefunden wurde
        if song.name == node['value'].name:
            end_time = time.time()
            print(f"Total search time: {end_time - start_time} seconds.")
            print(f"\033[103mA song with the name: {song.name} was found.\033[0m")
            print(f"Path: {' -> '.join(path)}")
            print(f"Index in depth-first search: {index}")
            
            

        index += 1

        #Rekursiver Aufruf auf der linken Seite des Baums
        result = self.depth_first_search(node=node['left'], song_input=song_input, path=path, first_call=False, index=index, start_time=start_time)
        if result == 0:
            return result

        #Rekursiver Aufruf auf der rechten Seite des Baums
        result = self.depth_first_search(node=node['right'], song_input=song_input, path=path, first_call=False, index=index, start_time=start_time)
        if result == 0:
            return result

        # Den letzten Pfad entfernen (backtracking)
        path.pop()
        
        if first_call:
            #Zeitmessung stoppen
            end_time = time.time()
            print(f"Total search time: {end_time - start_time} seconds.")

        return -1



    
    def breadth_first_search(self, node, song_input=None, first_call=True):
        visited = [] #liste der besuchten Knoten
        queue = [] #Warteschlange für die Knoten, die durchsucht werden sollen
        ted = []  #Liste zur Speicherung der Tiefe jedes Knotens
        index = 0 #Zähler der Indexsuche

        
        print("\033[1m\033[32mBreadth First Search is started\033[0m")
        #Falls kein song_input übergeben wurde, fordert das Programm den Benutzer auf, einen Songnamen einzugeben
        if song_input is None:
            song_input = input("\033[92mProvide the name of the song you want to search for: \033[0m")

        #Song-Objekt basierend auf dem Namen gesucht
        song = next((song for song in self.songs if song.name.lower() == song_input.lower()), None)
        if not song:
            print(f"\033[103mWe could not find a song with the name: {song_input}.\033[0m")
            return -1

        queue.append((node, 0))  #Startknoten und die Tiefe 0 wird zu Wartexhclange hinzugefügt

        #solange die Wartechlange nicht leer ist:
        while queue:
            #Aktuelle Tiefe & Knoten aus Warteschlange holen
            m, depth = queue.pop(0)
            current_song = m['value']

            #Tiefe in die Liste ted hinzufügen
            ted.append((current_song.name, depth))
            
            #Wenn der gesuchte Song gefunden wurde
            if current_song.name == song.name:
                visited.append(current_song.name)  # Füge den gesuchten Song zuletzt zum Pfad hinzu
                print(f"\033[103m\nSong '{current_song.name}' by {current_song.artist} - Album: {current_song.album}, Genre: {current_song.genre}, Duration: {current_song.duration} was found!\033[0m")
                print(f"Path to song: {' -> '.join(visited)}")
                print(f"Depth at which the song was found: {depth}")
                print(f"Index in breadth-first search: {index}")
                return 0

            # Füge den aktuellen Knoten zum Pfad hinzu, wenn er nicht der gesuchte Song ist
            visited.append(current_song.name)

            #Füge die Nachbarn (linkes und rechtes Kind) zur Warteschlange hinzu, falls sie nicht besucht wurden
            if m['left'] and m['left']['value'].name not in visited:
                queue.append((m['left'], depth + 1))  # Füge das linke Kind mit erhöhter Tiefe hinzu

            if m['right'] and m['right']['value'].name not in visited:
                queue.append((m['right'], depth + 1))  # Füge das rechte Kind mit erhöhter Tiefe hinzu

            #Erhöhe den Index
            index += 1

        #Song wurde nicht gefunden
        print(f"\nWe could not find a song with the name: '{song.name}'")
        return -1



    def jump_search(self, arr, song_input=None):
        print("\033[1m\033[32mJump Search is started\033[0m")

        #Wenn kein Song_input übergeben wurde, muss der Nutzer selbst die EIngabe machen
        if song_input is None:
            song_input = input("\033[92mProvide the name of the song you want to search for: \033[0m")

        song = next((song for song in arr if song.name.lower() == song_input.lower()), None)
        if not song:
            print(f"\033[103mThe song with the name: '{song_input}' could not be found.\033[0m")
            return -1

        num_elements = len(arr)
        #Berechnung der Sprunggröße basierend auf der Quadratwurzel der Anzahl der Elemente
        step = int(math.sqrt(num_elements))
        prev = 0 #Startpunkt

        #Sprungweise Suche nach dem Block, der den gesuchten Song enthalten könnte
        while prev < num_elements and song.name > arr[min(step, num_elements) - 1].name:
            prev = step
            step += int(math.sqrt(num_elements))

            #Wenn der Suchbereich außerhalb des Arrays liegt, abbrechen
            if prev >= num_elements:
                print(f"\033[103mWe could not find a song with the name: '{song.name}'\033[0m")
                return -1

        #Lineare Suche im gefundenen Block durchführen
        while prev < min(step, num_elements) and song.name >= arr[prev].name:
            if arr[prev].name == song.name:
                print(f"\033[103mWe found a song with the name: '{song.name}' on index: {prev}\033[0m")
                return prev  # Erfolgreich gefunden
            prev += 1

        # Falls der Song nicht gefunden wurde
        print(f"\033[103mWe could not find a song with the name: '{song.name}'\033[0m")
        return -1

            
        
    def fibonacci_search(self, arr, song_input= None):
        print("\033[1m\033[32mFibonacci Search is started\033[0m")

        #Falls kein song_input mitgegeben wurde, muss der Nutzer die Eingabe machen
        if song_input is None:
            song_input = input("\033[92mPlease provide the name of the song you want to search for: \033[0m")

        song = next((song for song in arr if song.name.lower() == song_input.lower()), None)
        if not song:
            print(f"\033[103mWe could not find a song with the name: '{song_input}'\033[0m")
            return -1

        num_elements = len(arr)

        # Initialisiere Fibonacci-Zahlen
        f0 = 0  
        f1 = 1  
        f2 = f0 + f1 

        #Bestimmung der kleinsten Fibonacci-Zahl, die größer oder gleich der Anzahl der Elemente ist
        while f2 < num_elements:
            f0 = f1
            f1 = f2
            f2 = f1 + f0

        #Der Offset markiert die Grenze, bis zu der der Song gefunden werden kann
        offset = -1

        #Solange noch zu durchsuchende Elemente vorhanden sind
        while f2 > 1:
            # Index des Elements berechnen, das verglichen werden soll
            index = min(offset + f0, num_elements - 1)

            # Wenn das Element an `index` kleiner als das gesuchte Element ist: Suchgrenze nach rechts verschieben
            if arr[index].name < song.name:
                f2 = f1
                f1 = f0
                f0 = f2 - f1
                offset = index

            # Wenn das Element an `index` größer als das gesuchte Element ist: Suchgrenze nach links verschieben
            elif arr[index].name > song.name:
                f2 = f0
                f1 = f1 - f0
                f0 = f2 - f1

             #Wenn der Song gefunden wurde, gib den Index zurück
            else:
                print(f"\033[103mA song with the name: {song.name} was found at index: {index}.\033[0m")
                return index

        #Überprüfen, ob der Song an der letzten möglichen Position gefunden wird
        if f1 and arr[offset + 1].name == song.name:
            print(f"\033[103mA song with the name: '{song.name}' was found at index: {offset + 1}.\033[0m")
            return offset + 1

        # Wenn der Song nicht gefunden wurde
        print(f"\033[103mWe could not find a song with the name: '{song.name}'\033[0m")
        return -1



    def exponential_search(self, arr, song_input= None):
        print("\033[1m\033[32mExponential Search is started\033[0m")

        if song_input is None:
            song_input = input("\033[92mPlease provide the name of the song you want to search for: \033[0m")

        song = next((song for song in arr if song.name.lower() == song_input.lower()), None)
        if not song:
            print(f"\033[103mWe could not find a song with the name: '{song_input}'\033[0m")
            return -1

        num_elements = len(arr)
        #Überprüfen, ob der gesuchte Song das erste Element im Array ist
        if song.name == arr[0].name:
            return 0

        #Exponentielle Suche nach der maximalen möglichen Position des gesuchten Elements 
        index = 1
        #Solange der Index innerhalb der Grenzen des Arrays liegt (index < num_elements) und der Name des gesuchten Songs alphabetisch größer oder gleich dem Song an der aktuellen Position (arr[index]) ist, wird der Index weiter exponentiell vergrößert (index verdoppelt).
        while index < num_elements and song.name >= arr[index].name:
            index = index * 2

        #Anwendung der Binärsuche auf den gefundenen Bereich
        return self.binary_search(arr, left=index // 2, right=min(index, num_elements - 1), song_input=song_input)


    def test_sorting_algorithm(self, algorithm, arr):
        print(f"\033[1m\033[32mTesting {algorithm.__name__}...\033[0m")

        # Messen der Startzeit
        start_time = time.time()
        
        # Ausführen des übergebenen Algorithmus
        algorithm(arr)
        
        # Messen der Endzeit
        end_time = time.time()
        
        # Berechnen der benötigten Zeit
        elapsed_time = end_time - start_time
        
        # Ausgabe der Laufzeit
        print(f"Sorting completed in {elapsed_time:.6f} seconds.")
        
        return elapsed_time
    
    def sorting_algorithms_to_test(self):
        # Auswahl der Sortieralgorithmen
        print('1. Test Quicksort')
        print('2. Test Bubble sort')
        print('3. Test Merge Sort')
        print('4. Test Block Sort')
        
        option = input("Choose the algorithm by number: ")
        
        if option == '1':
            elapsed_time = self.test_sorting_algorithm(self.quicksort, self.songs)
        elif option == '2':
            elapsed_time = self.test_sorting_algorithm(self.bubble_sort, self.songs)
        elif option == '3':
            elapsed_time = self.test_sorting_algorithm(self.merge_sort, self.songs)
        elif option == '4':
            elapsed_time = self.test_sorting_algorithm(self.block_sort, self.songs)
        else:
            print("Invalid option selected.")
            return



    def sort_songs_with_algorithms(self):
        #Auswahl der Sortieralgorithmen
        print('1. Quicksort')
        print('2. Bubble sort')
        print('3. Merge Sort')
        print('4. Block Sort')
        option = input("Choose your algorithm by number: ")

        if option == '1':
            self.songs = self.quicksort(self.songs)
        elif option == '2':
            self.songs = self.bubble_sort(self.songs)
        elif option == '3':
            self.songs = self.merge_sort(self.songs)
        elif option=='4':
            self.songs = self.block_sort(self.songs)

        print(f"\033[33m{self.display_all_songs()}\033[0m")



    def quicksort(self, arr=None, first_call=True):
        if arr is None:
            arr= self.songs
        # Nur beim ersten Aufruf prüfen, ob das Array sortiert werden kann
        if first_call and len(arr) <= 1:
            print(f"Array cannot be sorted")  # Nur bei leerem oder einem Element
            return arr  # Gib das Array zurück und beende

        # Wenn das Array keine oder nur ein Element enthält (rekursiver Fall), einfach zurückgeben
        if len(arr) <= 1:
            return arr

        # Auswahl des Pivot-Elements, in diesem Fall das mittlere Element des Arrays
        pivot = arr[len(arr) // 2]

        # Erstellt eine Liste aller Elemente, die kleiner als das Pivot-Element sind (linker Teil des Arrays)
        left = [song for song in arr if song < pivot]

        # Erstellt eine Liste aller Elemente, die gleich dem Pivot-Element sind (das Pivot-Element selbst)
        middle = [song for song in arr if song == pivot]

        # Erstellt eine Liste aller Elemente, die größer als das Pivot-Element sind (rechter Teil des Arrays)s
        right = [song for song in arr if song > pivot]

        # Rekursion: Sortiere den linken und rechten Teil des Arrays und füge das Pivot in die Mitte ein
        return self.quicksort(left, first_call=False) + middle + self.quicksort(right, first_call=False)





    def bubble_sort(self, arr):
        print("\033[94mBubble Sort is started\033[0m")
        
        #Äußerer Schleifenindex: Wiederholung für jeden Song in der Liste
        #Die äußere Schleife sorgt dafür, dass der Sortierprozess mehrmals durchlaufen wird, bis die Liste vollständig sortiert ist
        for index1 in range(len(arr)):
            swapped= False
            #Innerer Schleifenindex: Vergleich benachbarter Elemente
            #Die innere Schleife durchläuft die Liste bis zum unsortierten Teil (der bei jeder Iteration kleiner wird)
            for index2 in range(0, len(arr) - index1 - 1):
                #Vergleich der benachbarten Elemente, um festzustellen, ob sie in der falschen Reihenfolge sind -> flashce Reihenfolge wenn linkes Element größer als rechtes
                if arr[index2] > arr[index2 + 1]:
                    #Wenn das linke Element größer als das rechte ist, tauschen wir ihre Plätze
                    arr[index2], arr[index2 + 1] = arr[index2 + 1], arr[index2]
                    #wenn swapped true ist, hat ein Tausch stattgefunden und es besteht weitherhin die Möglichkeit, dass die Liste noch nicht vollständig sortiert ist
                    swapped= True
            
            #wenn in dieser Iteration keine Elemente vertauscht wurden, bedeutet das, dass die Liste bereits sortiert ist -> Der Algorithmus kann vorzeitig abbrechen
            if not swapped:
                break

        print("Songs were successfully sorted")
        return arr



    def merge_sort(self, arr, first_call=True):
        if first_call and len(arr) <= 1:
            print(f"Array cannot be sorted")  # Nur bei leerem oder einem Element
            return arr  # Gib das Array zurück und beende

        # Wenn das Array keine oder nur ein Element enthält (rekursiver Fall), einfach zurückgeben
        if len(arr) <= 1:
            return arr
        
        #Finden des mittleren Index, um das Array in zwei Hälften zu teilen
        mid = len(arr) // 2

        #Rekursiver Aufruf der merge_sort-Funktion auf der linken Hälfte des Arrays
        left = self.merge_sort(arr[:mid], first_call=False)

        #Rekursiver Aufruf der merge_sort-Funktion auf der rechten Hälfte des Arrays
        right = self.merge_sort(arr[mid:], first_call=False)

        #Zusammenführen der beiden sortierten Hälften und Rückgabe des zusammengeführten Arrays
        return self.merge(left, right)


    def merge(self, left, right):
        #Erstellen einer leeren Liste, um die beiden sortierten Listen zu kombinieren
        merged = []
        #Initialisieren von zwei Indizes, um die Position in den beiden Listen (left und right) zu verfolgen
        index1, index2 = 0, 0

        #Schleife, um die beiden Listen so lange zu vergleichen, bis eine von ihnen vollständig durchlaufen wurde
        while index1 < len(left) and index2 < len(right):
            #Wenn das Element in der linken Liste kleiner oder gleich dem Element in der rechten Liste ist, wird es zur merged-Liste hinzugefügt, und der Index der linken Liste wird erhöht
            if left[index1] <= right[index2]:
                merged.append(left[index1])
                index1 += 1
            else:
                #Andernfalls wird das Element der rechten Liste zur merged-Liste hinzugefügt, und der Index der rechten Liste wird erhöht
                merged.append(right[index2])
                index2 += 1

        #Wenn die rechte oder linke Liste vollständig durchlaufen ist, aber noch Elemente in der anderen Liste vorhanden sind,werden diese restlichen Elemente einfach angehängt (da sie bereits sortiert sind)
        merged.extend(left[index1:])
        merged.extend(right[index2:])

        return merged


    def calculate_block_size(self, num_elements):
        # Für kleine Arrays, setze die Blockgröße auf mindestens 1
        if num_elements <= 10:
            return 1

        # Für größere Arrays, setze die Blockgröße auf den Logarithmus der Anzahl der Elemente
        block_size = int(num_elements ** 0.5)  # Quadratwurzel der Array-Größe
        return block_size
        

    def block_sort(self, arr):
        print("\033[94mBlock Sort is started\033[0m")
        
        #Berechnung der Block Größen
        block_size = self.calculate_block_size(len(arr))

        #Liste, um die Blöcke zu speichern, die wir nach und nach sortieren werden
        blocks = []
    
        #Aufteilen der Liste in Blöcke von der angegebenen Größe
        for index in range(0, len(arr), block_size):
    
            block = arr[index:index + block_size] #Erstelle einen Block aus einem Teil des Arrays

            blocks.append(sorted(block)) #Sortiere den Block sofort und füge ihn der Blockliste hinzu

        #Ergebnisliste, die die vollständig sortierten Elemente enthalten wird
        result = []

        #Hauptschleife: Solange noch Blöcke übrig sind, wird das kleinste Element (min Heap) aus den Blöcken entnommen und zum Ergebnis hinzugefügt
        while blocks:
            #Findet den Block, der das kleinste erste Element enthält
            min_index = 0
            for index in range(1, len(blocks)): #Vergleicht das erste Element jedes Blocks
                if blocks[index][0] < blocks[min_index][0]:
                    min_index = index #Speichert den Index des Blocks mit dem kleinsten Element

            #Fügt das kleinste Element aus dem entsprechenden Block zur Ergebnisliste (Output Array) hinzu
            result.append(blocks[min_index].pop(0))
    
            #Wenn ein Block leer ist, entfernt man ihn vollständig aus der Liste der Blöcke
            if len(blocks[min_index]) == 0:
                blocks.pop(min_index)

        print("Songs were successfully sorted")

        #Rückgabe der vollständig sortierten Liste/Arrays
        return result




    def delete_song(self):
        song_input= input("Provide the song name you want to delete: ")


        song_to_delete = next((song for song in self.songs if song.name.lower() == song_input.lower()), None)
        #Prüfen ob Song name in Liste vorkommt
        if song_to_delete:
            self.songs.remove(song_to_delete)
            print(f"Song '{song_to_delete.name}' by {song_to_delete.artist} has been deleted.")
        else:
            print(f"No song named '{song_input}' found in the list.")
    
        
    def display_all_songs(self):
        if not self.songs:
            print("No songs available.")
        else:
            for song in self.songs:
                print(song)

    def display_playlists(self):
        if not self.playlists:
            print("No playlists available.")
        else:
            for playlist in self.playlists:
                print(playlist)
                for song in playlist.songs:
                    print(f"  - {song}")



    def main_menu(self):
        while True:
            print("\n--- Music App ---")
            print("1. Add New Song")
            print("2. Create Playlist")
            print("3. Add Song to Playlist")
            print("4. Search Songs")
            print("5. Sort Songs")
            print("6. Display All Songs")
            print("7. Display Playlists")
            print("8. Delete Song")
            print("9. Test the Runtime of the searching-algorithms")
            print("10. Test the Runtime of the sorting-algorithms")
            print("11. Save")
            print("12. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                self.add_song()
                self.save_data()
            elif choice == '2':
                self.create_playlist()
            elif choice == '3':
                self.add_song_to_playlist()
            elif choice == '4':
                self.search_songs_with_algorithms()
            elif choice == '5':
                self.sort_songs_with_algorithms()
            elif choice == '6':
                self.display_all_songs()
            elif choice == '7':
                self.display_playlists()
            elif choice == '8':
                self.delete_song()
            elif choice == '9':
                self.searching_alogrithms_to_test()
            elif choice == '10':
                self.sorting_algorithms_to_test()
            elif choice == '11':
                self.save_data()
            elif choice == '12':
                self.save_data()
                print("Exiting the app.")
                break
            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    app = MusicApp()
    app.main_menu()