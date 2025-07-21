import tkinter as tk
import random
import numpy as np

class QTraffic4Ways:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Traffic Light AI - 4 Directions")

        # بناء كل الحالات الممكنة (N,S,E,W) من 0 حتى 10 سيارات
        self.states = []
        for n in range(11):
            for s in range(11):
                for e in range(11):
                    for w in range(11):
                        self.states.append((n, s, e, w))

        self.actions = [0, 1, 2, 3]  # 0=شمال،1=جنوب،2=شرق،3=غرب
        self.Q = {state: [0, 0, 0, 0] for state in self.states}

        # معاملات التعلم
        self.alpha = 0.1
        self.gamma = 0.9
        self.epsilon = 0.2

        self.state = (0, 0, 0, 0)

        self.labels = {}
        self.lights = {}
        self.directions = ["شمال", "جنوب", "شرق", "غرب"]

        self.init_ui()
        self.train_q_learning()
        self.update_simulation()

    def init_ui(self):
        for i, direction in enumerate(self.directions):
            tk.Label(self.root, text=direction, font=("Arial", 16)).grid(row=i, column=0, padx=20, pady=10)
            self.labels[direction] = tk.Label(self.root, text="0 سيارات", font=("Arial", 14))
            self.labels[direction].grid(row=i, column=1)
            self.lights[direction] = tk.Label(self.root, text="  ", font=("Arial", 20), width=4, height=2, bg="red")
            self.lights[direction].grid(row=i, column=2)

    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.choice(self.actions)
        return int(np.argmax(self.Q[state]))

    def get_reward(self, state, action):
        # العقاب (أو المكافأة السالبة) هو عدد السيارات في الطريق المختار (نريد تقليل الزحام)
        return -state[action]

    def train_q_learning(self):
        for _ in range(10000):
            s = (random.randint(0, 10), random.randint(0, 10), random.randint(0, 10), random.randint(0, 10))
            action = self.choose_action(s)
            reward = self.get_reward(s, action)
            old_q = self.Q[s][action]
            self.Q[s][action] = old_q + self.alpha * (reward + self.gamma * max(self.Q[s]) - old_q)

    def update_simulation(self):
        # توليد أعداد عشوائية للسيارات في كل طريق
        n = random.randint(0, 10)
        s = random.randint(0, 10)
        e = random.randint(0, 10)
        w = random.randint(0, 10)
        self.state = (n, s, e, w)

        action = self.choose_action(self.state)

        for i, direction in enumerate(self.directions):
            self.labels[direction].config(text=f"{self.state[i]} سيارات")
            if i == action:
                self.lights[direction].config(bg="green")
            else:
                self.lights[direction].config(bg="red")

        reward = self.get_reward(self.state, action)
        old_q = self.Q[self.state][action]
        self.Q[self.state][action] = old_q + self.alpha * (reward + self.gamma * max(self.Q[self.state]) - old_q)

        # إعادة التحديث كل 3 ثواني
        self.root.after(3000, self.update_simulation)

root = tk.Tk()
app = QTraffic4Ways(root)
root.mainloop()
