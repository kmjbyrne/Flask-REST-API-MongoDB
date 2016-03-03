


from pymongo import MongoClient
import datetime
import time

client = MongoClient()

db = client['FantasyDB']

db['unicorns']



db.unicorns.insert_one({'name': 'Horny', 'dob': datetime.date(1992,2,13,7,47), 'loves': ['carrot','papaya'], 'weight': 600, 'gender': 'm', 'vampires': 63}); 
db.unicorns.insert_one({'name': 'Aurora', 'dob': datetime.date(1991, 0, 24, 13, 0), 'loves': ['carrot', 'grape'], 'weight': 450, 'gender': 'f', 'vampires': 43}); 
db.unicorns.insert_one({'name': 'Unicrom', 'dob': datetime.date(1973, 1, 9, 22, 10), 'loves': ['energon', 'redbull'], 'weight': 984, 'gender': 'm', 'vampires': 182}); 
db.unicorns.insert_one({'name': 'Roooooodles', 'dob': datetime.date(1979, 7, 18, 18, 44), 'loves': ['apple'], 'weight': 575, 'gender': 'm', 'vampires': 99}); 
db.unicorns.insert_one({'name': 'Solnara', 'dob': datetime.date(1985, 6, 4, 2, 1), 'loves':['apple', 'carrot', 'chocolate'], 'weight':550, 'gender':'f', 'vampires':80}); 
db.unicorns.insert_one({'name':'Ayna','dob': datetime.date(1998, 2, 7, 8, 30), 'loves': ['strawberry', 'lemon'], 'weight': 733, 'gender': 'f', 'vampires': 40}); 
db.unicorns.insert_one({'name':'Kenny', 'dob': datetime.date(1997, 6, 1, 10, 42), 'loves': ['grape', 'lemon'], 'weight': 690, 'gender': 'm', 'vampires': 39}); 
db.unicorns.insert_one({'name': 'Raleigh', 'dob': datetime.date(2005, 4, 3, 0, 57), 'loves': ['apple', 'sugar'], 'weight': 421, 'gender': 'm', 'vampires': 2}); 
db.unicorns.insert_one({'name': 'Leia', 'dob': datetime.date(2001, 9, 8, 14, 53), 'loves': ['apple', 'watermelon'], 'weight': 601, 'gender': 'f', 'vampires': 33}); 
db.unicorns.insert_one({'name': 'Pilot', 'dob': datetime.date(1997, 2, 1, 5, 3), 'loves': ['apple', 'watermelon'], 'weight': 650, 'gender': 'm', 'vampires': 54}); 
db.unicorns.insert_one({'name': 'Nimue', 'dob': datetime.date(1999, 11, 20, 16, 15), 'loves': ['grape', 'carrot'], 'weight': 540, 'gender': 'f'}); 
db.unicorns.insert_one({'name': 'Dunx', 'dob': datetime.date(1976, 6, 18, 18, 18), 'loves': ['grape', 'watermelon'], 'weight': 704, 'gender': 'm', 'vampires': 165});
