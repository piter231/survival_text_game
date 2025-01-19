import random
import pickle
import os

class SurvivalGame:
    def __init__(self):
        self.day = 1
        self.health = 100
        self.food = 50
        self.water = 50
        self.wood = 0
        self.location = "beach"
        self.map = ["beach", "forest", "mountain", "river", "cave", "plain"]
        self.inventory = {"tools": [], "herbs": 0, "stones": 0, "rope": 0, "arrows": 0, "fish": 0}
        self.game_running = True
        self.difficulty = "normal"
        self.events_log = []
        self.buildings = {"shelter": False, "fireplace": False, "trap": False, "fishing_rod": False}
        self.weather = "clear"
        self.morale = 100

    def display_status(self):
        print("\n=== STATUS ===")
        print(f"Day: {self.day}")
        print(f"Health: {self.health}")
        print(f"Food: {self.food}")
        print(f"Water: {self.water}")
        print(f"Wood: {self.wood}")
        print(f"Morale: {self.morale}")
        print(f"Location: {self.location}")
        print(f"Weather: {self.weather}")
        print(f"Inventory: {self.inventory}")
        print(f"Buildings: {self.buildings}")
        print("===============")

    def choose_action(self):
        print("\nWhat would you like to do?")
        print("1. Explore")
        print("2. Gather resources")
        print("3. Eat food")
        print("4. Drink water")
        print("5. Rest")
        print("6. Craft tools")
        print("7. Build structures")
        print("8. Use herbs")
        print("9. Hunt for food")
        print("10. Fish")
        print("11. Check weather")
        print("12. Save game")
        print("13. Quit game")

        choice = input("Enter the number of your choice: ")
        return choice

    def explore(self):
        new_location = random.choice(self.map)
        print(f"You explore the area and move from {self.location} to {new_location}.")
        self.location = new_location
        self.log_event(f"Explored and moved to {new_location}.")
        self.random_event()

    def gather_resources(self):
        if self.location == "forest":
            wood_gathered = random.randint(5, 15)
            self.wood += wood_gathered
            print(f"You gathered {wood_gathered} units of wood.")
        elif self.location == "river":
            water_gathered = random.randint(5, 15)
            self.water += water_gathered
            print(f"You collected {water_gathered} units of water.")
        elif self.location == "beach":
            food_found = random.randint(5, 10)
            self.food += food_found
            print(f"You found {food_found} units of food.")
        elif self.location == "mountain":
            stones_found = random.randint(3, 8)
            self.inventory["stones"] += stones_found
            print(f"You found {stones_found} stones in the mountains.")
        elif self.location == "cave":
            rope_found = random.randint(1, 3)
            self.inventory["rope"] += rope_found
            print(f"You found {rope_found} pieces of rope in the cave.")
        elif self.location == "plain":
            herbs_found = random.randint(2, 5)
            self.inventory["herbs"] += herbs_found
            print(f"You found {herbs_found} herbs in the plains.")
        else:
            print("You cannot gather resources here.")
        self.log_event(f"Gathered resources at {self.location}.")
        self.random_event()

    def eat_food(self):
        if self.food > 0:
            self.food -= 10
            self.health += 5
            print("You ate some food. Health increased!")
            self.log_event("Ate food and restored health.")
        else:
            print("You have no food to eat!")

    def drink_water(self):
        if self.water > 0:
            self.water -= 10
            self.health += 5
            print("You drank some water. Health increased!")
            self.log_event("Drank water and restored health.")
        else:
            print("You have no water to drink!")

    def rest(self):
        print("You take a rest to recover.")
        self.health += 10
        self.food -= 5
        self.water -= 5
        self.morale += 5
        self.log_event("Took a rest to recover health.")
        self.random_event()

    def craft_tools(self):
        if self.wood >= 10 and self.inventory["stones"] >= 2:
            self.wood -= 10
            self.inventory["stones"] -= 2
            self.inventory["tools"].append("axe")
            print("You crafted an axe. This will help you gather resources more efficiently!")
            self.log_event("Crafted an axe.")
        elif self.wood >= 5 and self.inventory["rope"] >= 1:
            self.wood -= 5
            self.inventory["rope"] -= 1
            self.inventory["tools"].append("bow")
            self.inventory["arrows"] += 5
            print("You crafted a bow and 5 arrows. Ready for hunting!")
            self.log_event("Crafted a bow and arrows.")
        elif self.wood >= 15 and self.inventory["rope"] >= 2:
            self.wood -= 15
            self.inventory["rope"] -= 2
            self.buildings["fishing_rod"] = True
            print("You crafted a fishing rod. Now you can fish for food!")
            self.log_event("Crafted a fishing rod.")
        else:
            print("You don't have enough materials to craft tools.")

    def build_structures(self):
        if not self.buildings["shelter"] and self.wood >= 20:
            self.wood -= 20
            self.buildings["shelter"] = True
            print("You built a shelter. This will protect you from harsh weather.")
            self.log_event("Built a shelter.")
        elif not self.buildings["fireplace"] and self.wood >= 10:
            self.wood -= 10
            self.buildings["fireplace"] = True
            print("You built a fireplace. Now you can cook food.")
            self.log_event("Built a fireplace.")
        elif not self.buildings["trap"] and self.wood >= 5 and self.inventory["rope"] >= 1:
            self.wood -= 5
            self.inventory["rope"] -= 1
            self.buildings["trap"] = True
            print("You built a trap. This will help you catch food.")
            self.log_event("Built a trap.")
        else:
            print("You don't have enough materials to build any structure.")

    def use_herbs(self):
        if self.inventory["herbs"] > 0:
            self.inventory["herbs"] -= 1
            self.health += 15
            print("You used some herbs to heal yourself. Health restored!")
            self.log_event("Used herbs to heal.")
        else:
            print("You have no herbs to use!")

    def hunt_for_food(self):
        if "bow" in self.inventory["tools"] and self.inventory["arrows"] > 0:
            self.inventory["arrows"] -= 1
            food_gathered = random.randint(10, 20)
            self.food += food_gathered
            print(f"You went hunting and brought back {food_gathered} units of food.")
            self.log_event("Hunted for food and succeeded.")
        else:
            print("You don't have the tools or arrows to hunt!")

    def fish(self):
        if self.buildings["fishing_rod"]:
            fish_caught = random.randint(5, 15)
            self.inventory["fish"] += fish_caught
            print(f"You went fishing and caught {fish_caught} fish.")
            self.log_event("Fished and caught food.")
        else:
            print("You need a fishing rod to fish!")

    def check_weather(self):
        weather_conditions = ["clear", "rainy", "stormy", "foggy"]
        self.weather = random.choice(weather_conditions)
        print(f"Today's weather is {self.weather}.")
        self.log_event(f"Checked weather: {self.weather}.")

    def random_event(self):
        events = [
            "You encountered a wild animal and lost some health!",
            "A storm damaged your camp and you lost some wood!",
            "You found some extra food while exploring!",
            "You slipped and hurt yourself, losing health!",
            "You discovered rare herbs for healing!",
            "Your trap caught some food!",
            "Nothing unusual happened.",
        ]
        event = random.choice(events)
        print(f"Random event: {event}")
        self.log_event(event)

        if event == "You encountered a wild animal and lost some health!":
            self.health -= 10
        elif event == "A storm damaged your camp and you lost some wood!":
            self.wood = max(0, self.wood - 10)
        elif event == "You found some extra food while exploring!":
            self.food += 10
        elif event == "You slipped and hurt yourself, losing health!":
            self.health -= 5
        elif event == "You discovered rare herbs for healing!":
            self.inventory["herbs"] += 1
        elif event == "Your trap caught some food!" and self.buildings["trap"]:
            self.food += random.randint(10, 20)

    def log_event(self, event):
        self.events_log.append(event)
        if len(self.events_log) > 10:
            self.events_log.pop(0)

    def save_game(self):
        with open("savegame.pkl", "wb") as f:
            pickle.dump(self.__dict__, f)
        print("Game saved successfully.")

    def load_game(self):
        if os.path.exists("savegame.pkl"):
            with open("savegame.pkl", "rb") as f:
                self.__dict__ = pickle.load(f)
            print("Game loaded successfully.")
        else:
            print("No saved game found.")

    def start_game(self):
        self.load_game()
        while self.game_running:
            self.display_status()
            choice = self.choose_action()
            if choice == "1":
                self.explore()
            elif choice == "2":
                self.gather_resources()
            elif choice == "3":
                self.eat_food()
            elif choice == "4":
                self.drink_water()
            elif choice == "5":
                self.rest()
            elif choice == "6":
                self.craft_tools()
            elif choice == "7":
                self.build_structures()
            elif choice == "8":
                self.use_herbs()
            elif choice == "9":
                self.hunt_for_food()
            elif choice == "10":
                self.fish()
            elif choice == "11":
                self.check_weather()
            elif choice == "12":
                self.save_game()
            elif choice == "13":
                print("Thanks for playing! Goodbye.")
                self.game_running = False
            else:
                print("Invalid choice. Please select a valid option.")
            self.day += 1

if __name__ == "__main__":
    game = SurvivalGame()
    game.start_game()

