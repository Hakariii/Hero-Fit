# Hero-Fit
What is my app?

This program calculate daily steps via "Google Fit" in function "daily_steps_from_google", all steps are recalculating into xp. Xp amount impacts on level, which is main goal of the app. Level is the main aspect because on it's amount are made almost all calculations that impacts on hp (player's helath), dmg (player's damage), heal amount (player's heal amount).

Main goal of the app is to force users to have an active life. Do sports, have daily steps goals.

In "Daily Battle" window is daily goal of steps. Completing required steps goal, user can claim reward (xp and coins).

In "Battle" player kills enemies, using his strategy (when to heal, when to deal damage). He imporves main characteristics as mentioned before by living an active life. 

There are also some futures in user's interface (Add Sleep Time, Add Hydration) that also motivates them to improve their health and in addtion to that improve their "Hero". However throught "Google fit" it's impossible to gain data about hydration and sleep time. So instead of that I relied on users honesty. Changing name is only function that requires "coins"


How to run code?

Just compilate simply.ipnyb

How to use?

Using Thinter module frontend was made, and intuitively users can use by pressing on buttons (All buttons has label what they do, to update daily steps, they just need to move)


How  program covers requirements?

Polymorphism:

Mage:

def health_calculator(self):
    hydration = self._hydration if self._hydration is not None else 0
    sleep_time = self._sleep_time if self._sleep_time is not None else 0
    self._health = (self._progress.get_level()+(20*(hydration+sleep_time)))
def damage_calculator(self):
    hydration = self._hydration if self._hydration is not None else 0
    sleep_time = self._sleep_time if self._sleep_time is not None else 0
    self._damage = pow(self._progress.get_level(),(sleep_time/2 + hydration))
def heal_calculator(self):
    self._heal_amount = self._progress.get_level()*10

Warrior

def health_calculator(self):
        hydration = self._hydration if self._hydration is not None else 0
        sleep_time = self._sleep_time if self._sleep_time is not None else 0
        self._health = (self._progress.get_level()+(50*(hydration+sleep_time)))
def damage_calculator(self):
    hydration = self._hydration if self._hydration is not None else 0
    sleep_time = self._sleep_time if self._sleep_time is not None else 0
    self._damage = pow(self._progress.get_level(),(sleep_time/4 + hydration/2))
def heal_calculator(self):
    self._heal_amount = self._progress.get_level()*5

Each class calculates differently user's hp, dmg, heal amount.

Abstraction:

In the super class

    @abstractmethod
    def damage_calculator(self):
        return "Damage is calculating"
    @abstractmethod
    def heal_calculator(self):
        return "Heal is calculating."

Inheritance:

class Mage(Character)

class Warrior(Character)

Almost all methods in classes are written in parent class.

Encapsulation:

self._name = name
self._age = age
self._gender = gender
self._weight = weight
self._height = height
self._id = str(uuid.uuid4())
self._email = email
self._status = 0

self._beaten_enemies = 0
self._sleep_time = None
self._hydration = None
self._health = None
self._damage = None
self._heal_amount = None
self._progress = Progression(self._id)
self._energy = StepEnergyMeter(self._id)

All variables are protected in order to not have impact from there where they shouldn't be changed.

Design Pattern:

Singleton

_instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

It's neccessary and the best, because with it we can be sure, that player will have only one Character, and not be able to play with different classes each time he is logining in.


Aggregation/Composition

self._progress = Progression(self._id)
self._energy = StepEnergyMeter(self._id)

In project I decided to make composition in order not to make "Character" a "God class".



Reading/Writing in file, db


In code there is reading and writing from/in database.

ef save_to_db(self):
        print("Saving...")
        retries = 5
        delay = 3

        for i in range(retries):
            try:
                with sqlite3.connect("game.db", timeout=10, check_same_thread=False) as conn:
                    cursor = conn.cursor()
                    cursor.execute('''
                    INSERT OR REPLACE INTO characters
                    (id, name, age, gender, weight, height, xp, level, coins, daily_steps,
                     all_time_steps, beaten_enemies, email, class,status)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    self._id, self._name, self._age, self._gender, self._weight, self._height,
                    self._progress.get_xp(), self._progress.get_level(), self._progress.get_coins(), self._energy.get_daily_steps(),
                    self._energy.get_all_time_steps(), self._beaten_enemies,
                    self._email, type(self).__name__, self.get_status()
                ))
                    conn.commit()
                break  
            except sqlite3.OperationalError as e:
                print(e)
                print(f"DB is locked, retry {i+1}/{retries}...")
                time.sleep(delay)
        else:
            print("Failed to save to DB after retries.")

There is a bit debugs to ensure that it works and if something will happent with database it would be fixed.


def change_name(self, new_name,frame):
        Res= Toplevel(frame,bg='#878E99')
        Res.title("Result")
        if self._progress.get_coins() >= 500:
            self._name = new_name
            lab = Label(Res,text="You succesfully changed your hero's name for 500 coins!")

            coins = self._progress.get_coins()
            coins -= 500
            self._progress.set_coins(coins)
            conn, cursor = connect_db()
            cursor.execute('UPDATE characters SET name = ? WHERE id = ?', (self._name, self._id))
            conn.commit()
            conn.close()
        else:
            lab = Label(Res,text="Not enough coins, price of changing name 500 coins!")
        lab.pack()
        btn_ex = Button(Res,text="OK", command=lambda : destr_windows(Res,frame))
        btn_ex.pack()


Here are updating name of hero in database.

 with sqlite3.connect("game.db", timeout=10, check_same_thread=False) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM characters WHERE email = ?", (email,))
            row = cursor.fetchone()
            
            cursor.close()
            print(row)
            print("\n")
            print(row[0])
            id = row[0] if row[0] is not None else 0
            name = row[1] if row[1] is not None else ""
            age = row[2] if row[2] is not None else 0
            gender = row[3] if row[3] is  None else ""
            weight = row[4] if row[4] is   None else 0
            height = row[5] if row[5] is  None else 0
            xp = row[6] if row[6] is not None else 0
            level = row[7] if row[7] is  None else 0
            coins = row[8] if row[8] is not None else 0
            daily_steps = row[9] if row[9] is not None else 0
            all_time_s = row[10] if row[10] is not None else 0
            beaten_enemies = row[11] if row[11] is not None else 0
            emaill = row[12] if row[12] is  None else ""
            classi = row[13] if row[13] is  None else ""
            status = row[14] if row[14] is None else 0
                
                
            start_game(name, age, height, weight, classi, gender, xp, level, coins, daily_steps, all_time_s, beaten_enemies, emaill,status,frame_start=None)

Here demonstrating reading from database, when user is logging in information from database is being readed and in function "start_game" loading hero.

with open("Enemies.txt", "r") as file:
    for line in file:
        currentline = line.strip().split(",")
        Enemies.append(Enemy(int(currentline[0]),int(currentline[1]),str(currentline[2])))

In this example is demonstrated reading from file and saving it into the list of "Daily Battles" enemies.


with open("quotes.txt", "r", encoding="utf-8") as file:
    quotes = [line.strip() for line in file if line.strip()]

As well as here, but making list with motivational quotes.

Results

First my full-stack project, faced with difficulties with working with "Google Oath2" not knowing syntaxies, how they send data. The second difficulty is Tkinter module, it was hard imagine how everything should look like. New syntaxies also made front-end process last longier than was expected. Good point is that I understood how to make self "mini deadlines" in order to control process of making projects in such big volume. Understood how to use "Git" to upload projects. Also I faced with problems with database a lot of times program just crashed because of database, however in the end all aspects were understood.


Conclusion

I got an experience writing full stack code. Understood and repeated all main aspects of OOP. Understood when should be used patterns/polymorphism/inheritance etc. functions of OOP. Got experience working with database, "Google Oath2", front-end. Result is GUI programm which will help people to "Become Heroes of their lives". Future plans is to add inventory and make more usage of coins, andd custamizations and icons for characters, clans and co-op battles and most important monitization. Rewrite step reading from "Google Oath2" to step reading from "Apple Health" using "Swift". Make the table and graphs of people losing weight/daily steps/daily hydration/daily sleep time. Make frontend more beautiful.