import sqlite3
from config import *
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import cartopy.crs as ccrs


class DB_Map():
    def __init__(self, database):
        self.database = database
    
    def create_user_table(self):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS users_cities (
                                user_id INTEGER,
                                city_id TEXT,
                                FOREIGN KEY(city_id) REFERENCES cities(id)
                            )''')
            conn.commit()

    def add_city(self,user_id, city_name ):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM cities WHERE city=?", (city_name,))
            city_data = cursor.fetchone()
            if city_data:
                city_id = city_data[0]  
                conn.execute('INSERT INTO users_cities VALUES (?, ?)', (user_id, city_id))
                conn.commit()
                return 1
            else:
                return 0

            
    def select_cities(self, user_id):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT cities.city 
                            FROM users_cities  
                            JOIN cities ON users_cities.city_id = cities.id
                            WHERE users_cities.user_id = ?''', (user_id,))

            cities = [row[0] for row in cursor.fetchall()]
            return cities


    def get_coordinates(self, city_name):
        conn = sqlite3.connect(self.database)
        with conn:
            cursor = conn.cursor()
            cursor.execute('''SELECT lat, lng
                            FROM cities  
                            WHERE city = ?''', (city_name,))
            coordinates = cursor.fetchone()
            return coordinates

    def create_grapf(self, path, cities):
        ax = plt.axes(projection=ccrs.PlateCarree())
        ax.stock_img()
        for city in cities:
            coord = self.get_coordinates(city_name=city)
            if not coord:
                return
            
            lon, lat = coord
            plt.plot([lat], [lon], color='r', linewidth=1, marker='.', transform=ccrs.Geodetic())
            plt.text(lat + 3, lon + 12, city, horizontalalignment='left', transform=ccrs.Geodetic())
        
        plt.savefig(path)

    def get_population(user_id,city_name):
        # Подключаемся к базе данных
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        
        # Создаем запрос к базе данных
        query = "SELECT population FROM cities WHERE city = ?"
        
        # Выполняем запрос
        cursor.execute(query, (city_name,))
        
        # Получаем результат
        result = cursor.fetchone()
        
        # Закрываем соединение с базой данных
        conn.close()
        
        # Проверяем, есть ли результат
        if result:
            return result[0]
        else:
            return "Население не найдено"
        
        
    def draw_distance(self, city1, city2):
        pass


if __name__=="__main__":
    m = DB_Map(DATABASE)
    m.create_user_table()
    print('Hello world')
    m.create_grapf('test.jpg', ['Moscow','New York'])
