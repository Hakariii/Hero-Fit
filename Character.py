import os
import time
from tkinter import *
import re


from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2 import id_token
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import requests
from datetime import datetime
import json
import asyncio
import threading
import sqlite3
from abc import ABC, abstractmethod
import uuid
from math import floor
import random
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import numpy as np
import matplotlib.pyplot as plt
import Battle
from AppData.Local.Programs.Python.Python311.Lib.idlelib.configdialog import help_pages
from tkinter import ttk
from tkinter import *
from PIL import Image, ImageTk
import Enemy
from AppData.Local.Programs.Python.Python311.Lib.test.test_generators import email_tests

SCOPES = ['https://www.googleapis.com/auth/fitness.activity.read']



class Character(ABC):

    def __init__(self, name, age, gender, weight, height,email):
        self._name = name
        self._age = age
        self._gender = gender
        self._weight = weight
        self._height = height
        self._id = str(uuid.uuid4())
        self._email = email


        self._beaten_enemies = 0
        self._sleep_time = None
        self._hydration = None
        self._health = None
        self._damage = None
        self._heal_amount = None
        self._progress = Progression(self._id)
        self._energy = StepEnergyMeter(self._id)

    def get_damage(self):
        self.damage_calculator()
        return self._damage
    def get_health(self):
        self.health_calculator()
        return self._health
    def get_heal_amount(self):
        self.heal_calculator()
        return self._heal_amount
    def get_beaten_enemies(self):
        return self._beaten_enemies
    def set_beaten_enemies(self,amount):
        self._beaten_enemies = amount
    @abstractmethod
    def health_calculator(self):
        return "Calculating hero health"
    def save_to_db(self):
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
                     all_time_steps, beaten_enemies, email, class)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                        self._id, self._name, self._age, self._gender, self._weight, self._height,
                        self._progress.get_xp(), self._progress.get_level(), self._progress.get_coins(), self._energy.get_daily_steps(),
                        self._energy.get_all_time_steps(), self._beaten_enemies,
                        self._email, type(self).__name__
                    ))
                    conn.commit()
                break
            except sqlite3.OperationalError as e:
                print(f"DB is locked, retry {i+1}/{retries}...")
                time.sleep(delay)
        else:
            print("Failed to save to DB after retries.")

    def set_email(self,email):
        self._email = email
    def set_id(self,id):
        self._id = id
    def set_name(self,name):
        self._name = name
    @abstractmethod
    def damage_calculator(self):
        return "Damage is calculating"
    @abstractmethod
    def heal_calculator(self):
        return "Heal is calculating."

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
    def add_weight(self,amount):
        self._weight = amount

    def add_height(self, amount):
        self._height = amount

    def get_name(self):
        return self._name
    def get_hydration(self):
        return self._hydration
    def set_hydration(self, amount):
        self._hydration = amount
    def add_hydration(self,amount):
        self._hydration = amount

    def sleep_time(self,amount):
        self._sleep_time = amount

    def get_heal_amount(self):
        return self._heal_amount
    def get_sleep_time(self):
        return self._sleep_time
    def set_sleep_time(self,amount):
        amount = min(8,float(amount))
        self._sleep_time = amount
    def get_email(self):
        return self._email

class Warrior(Character):
    def __init__(self, name, age, gender, weight, height,email):
        super().__init__(name, age, gender, weight, height,email)
        self._health = None
        self._damage = None
        self._heal_amount = None

    def get_email(self):
        return self._email
    def get_sleep_time(self):
        return self._sleep_time
    def health_calculator(self):
        hydration = self._hydration if self._hydration is not None else 0
        sleep_time = self._sleep_time if self._sleep_time is not None else 0
        self._health = (self._progress.get_level()+(50*(hydration+sleep_time)))
    def save_to_db(self):
        super().save_to_db()
    def damage_calculator(self):
        hydration = self._hydration if self._hydration is not None else 0
        sleep_time = self._sleep_time if self._sleep_time is not None else 0
        self._damage = pow(self._progress.get_level(),(sleep_time/4 + hydration/2))

    def heal_calculator(self):
        self._heal_amount = self._progress.get_level()*5

    def get_beaten_enemies(self):
        return self._beaten_enemies
    def set_beaten_enemies(self,amount):
        self._beaten_enemies = amount
    def change_name(self, new_name,frame):
        super().change_name(new_name,frame)
    def set_sleep_time(self,amount):
        amount = min(8,float(amount))
        self._sleep_time = amount
    def add_weight(self,amount):
        super().add_weight(amount)
    def add_height(self, amount):
        super().add_height(amount)
    def add_hydration(self,amount):
        super().add_hydration(amount)
    def sleep_time(self,amount):
        super().sleep_time(amount)
    def get_damage(self):
        self.damage_calculator()
        return round(self._damage,0)
    def get_health(self):
        self.health_calculator()
        return self._health
    def get_heal_amount(self):
        self.heal_calculator()
        return self._heal_amount
    def get_name(self):
        return self._name
    def set_hydration(self, amount):
        amount =  min(5,float(amount))
        self._hydration = amount
    def add_hydration(self,amount):
        self._hydration = amount



    def set_email(self,email):
        self._email = email

class Mage(Character):
    def __init__(self, name, age, gender, weight, height,email):
        super().__init__(name,age,gender,weight,height,email)
        self._health = None
        self._damage = None
        self._heal_amount = None
    def save_to_db(self):
        super().save_to_db()

    def get_email(self):
        return self._email
    def set_hydration(self, amount):
        amount =  min(5,float(amount))
        self._hydration = amount
    def add_hydration(self,amount):
        self._hydration = amount

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
    def change_name(self, new_name,frame):
        super().change_name(new_name,frame)
    def add_weight(self,amount):
        super().add_weight(amount)
    def add_height(self, amount):
        super().add_height(amount)
    def add_hydration(self,amount):
        super().add_hydration(amount)
    def sleep_time(self,amount):
        super().sleep_time(amount)
    def get_damage(self):
        self.damage_calculator()
        return round(self._damage,0)
    def get_beaten_enemies(self):
        return self._beaten_enemies
    def set_beaten_enemies(self,amount):
        self._beaten_enemies = amount
    def get_health(self):
        self.health_calculator()
        return self._health
    def get_heal_amount(self):
        self.heal_calculator()
        return self._heal_amount
    def get_name(self):
        return self._name
    def get_sleep_time(self):
        return self._sleep_time
    def set_sleep_time(self,amount):
        amount = min(8,float(amount))
        self._sleep_time = amount


    def set_email(self,email):
        self._email = email
    def get_email(self):
        return self._email


class Progression:
    def __init__(self,id):
        self._id = id
        self._level= 1
        self._xp=0
        self._coins = 0

    def get_coins(self):
        return self._coins
    def set_coins(self, coins):
        self._coins = coins
    def get_xp(self):
        return round(self._xp,0)
    def set_xp(self, xp):
        self._xp = xp


    def add_coins(self,amount):
        self._coins += amount

    def set_level(self, level):
        self._level = level
    def get_level(self):
        A, B, C, D, E = 50, 1.5, 200, 100, 5
        for level in range(1, 1000):
            if self._xp <= E * (A * (level ** B) + D * level + C):
                return level
        return 999
    def xp_calculation(self, amount):
        self._xp += amount
    def steps_to_xp(self):
        pass
    def add_xp(self,amount):
        print("!@#!@!#@!@#!@#!@#")
        print(f"{amount} !!!!!!!!!!!!!!!!!!!!!")
        self._xp += amount


class StepEnergyMeter:
    def __init__(self,id):
        self._id = id
        self._total_steps = 0
        self._daily_steps = 0
        self._temp = 0


    def set_daily_steps(self, stepss):
        self._daily_steps = stepss
    def get_daily_steps(self):
        return self._daily_steps
    def set_all_time_steps(self,steps):
        if self.get_daily_steps() != steps:
            self._total_steps = steps
    def update_all_time_steps(self):
        self._total_steps += self.daily_steps_from_google()
        print("CHECK")
        if player._energy.get_daily_steps() > player._energy.get_all_time_steps():
            print("CHECK 2")
            print(player._energy.get_daily_steps())
            player._energy.set_all_time_steps(player._energy.get_daily_steps())
    def daily_steps_from_google(self):
        creds = None
        token_name = player.get_email()
        if os.path.exists(f'{token_name}.json'):
            print("Found token.json, loading credentials...")
            creds = Credentials.from_authorized_user_file(f'{token_name}.json', SCOPES)
        else:
            print("token.json not found, need OAuth flow")

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                print("Refreshing expired token...")
                creds.refresh(Request())
            else:
                print("Starting OAuth flow...")
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)


        with open(f'{token_name}.json', 'w') as token:
            print(f"Saving new token to {token_name}.json")
            token.write(creds.to_json())
        today = datetime.today().strftime("%Y-%m-%d")
        start_time = int(time.mktime(time.strptime(f"{today} 00:00:00", "%Y-%m-%d %H:%M:%S"))) * 1000
        end_time = int(time.mktime(time.strptime(f"{today} 23:59:59", "%Y-%m-%d %H:%M:%S"))) * 1000

        url ="https://www.googleapis.com/fitness/v1/users/me/dataset:aggregate"
        headers = {
            "Authorization": f"Bearer {creds.token}",
            "Content-Type": "application/json"
        }
        body = {
            "aggregateBy": [{
                "dataTypeName": "derived:com.google.step_count.delta",
                "dataSourceId": "derived:com.google.step_count.delta:com.google.android.gms:estimated_steps"
            }],
            "bucketByTime": {"durationMillis": 86400000},
            "startTimeMillis": start_time,
            "endTimeMillis": end_time
        }

        response = requests.post(url, headers=headers, json=body)


        data = response.json()

        total_steps = 0
        if "bucket" in data:

            for bucket in data["bucket"]:
                if "dataset" in bucket:
                    for dataset in bucket["dataset"]:
                        for point in dataset["point"]:
                            for value in point["value"]:
                                total_steps += value.get("intVal", 0)

        print(f"{total_steps} + TOTAL STEPS")
        player._progress.add_xp(-player._energy.get_daily_steps())
        player._progress.add_xp(total_steps)
        temp = self.get_daily_steps()
        if total_steps!=temp:
            self._daily_steps = total_steps


            player._progress.steps_to_xp()
        print(self._daily_steps-temp)

        return self._daily_steps-temp


    def get_temp(self):
        return self._temp
    def get_all_time_steps(self):
        return self._total_steps