import tkinter as tk
import numpy as np
import random

class SmartTrafficLight:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Traffic AI")
        self.root.geometry("500x500")

        # عدد السيارات فكل اتجاه (0: شمال، 1: شرق، 2: جنوب، 3: غرب)
        self.traffic_data = np.random.randint(0, 20, 4)

        self.canvas = tk.Canvas(root, width=500, height=500, bg="white")
        self.canvas.pack()

        # نرسم الطرق
        self.draw_roads()

        # رسم الإشارات
        self.lights = []
        self.create_lights()

        # نشغل أول تحديث
        self.update_lights()

    def draw_roads(self):
        # طريق عمودي
        self.canvas.create_rectangle(225, 0, 275, 500, fill="gray")
        # طريق أفقي
        self.canvas.create_rectangle(0, 225, 500, 275, fill="gray")

    def create_lights(self):
        positions = [(200, 200), (300, 200), (300, 300), (200, 300)]
        for pos in positions:
            light = self.canvas.create_oval(pos[0], pos[1], pos[0]+20, pos[1]+20, fill="red")
            self.lights.append(light)

    def update_lights(self):
        # نحاولو نخلو الطريق الأقل زحام ياخد الضوء الأخضر
        min_index = np.argmin(self.traffic_data)

        # تحديث الألوان
        for i, light in enumerate(self.lights):
            color = "green" if i == min_index else "red"
            self.canvas.itemconfig(light, fill=color)

        # نعرض عدد السيارات
        self.canvas.delete("text")
        directions = ["Nord", "Est", "Sud", "Ouest"]
        for i, cars in enumerate(self.traffic_data):
            x = 20 if i % 2 == 0 else 400
            y = 50 + i*30
            self.canvas.create_text(x, y, text=f"{directions[i]}: {cars} voitures", font=("Arial", 12), fill="black", tag="text")

        # تحديث عدد السيارات عشوائياً
        self.traffic_data += np.random.randint(-2, 3, 4)
        self.traffic_data = np.clip(self.traffic_data, 0, 50)

        # كل 3 ثواني نرجع نحدّث
        self.root.after(3000, self.update_lights)

# تشغيل البرنامج
if __name__ == "__main__":
    root = tk.Tk()
    app = SmartTrafficLight(root)
    root.mainloop()
