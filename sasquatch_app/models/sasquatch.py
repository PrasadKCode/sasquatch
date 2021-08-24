from datetime import date
from sasquatch_app.models.skeptic import Skeptic
from sasquatch_app.config.mysqlconnection import connectToMySQL
from flask import flash
from datetime import datetime,date
from sasquatch_app.models.user import User


class Sasquatch:
    def __init__(self,data):
        self.id  = data['id']
        self.user_id  = data['user_id']
        self.location  = data['location']
        self.what_happened  = data['what_happened']
        self.date_of_sighting  = data['date_of_sighting']
        self.num_of_sasquatches  = data['num_of_sasquatches']
        self.created_at  = data['created_at']
        self.updated_at  = data['updated_at']
        self.users=[]
        self.reported_user =''
        self.skeptic_users = []
        self.count = ''

    @staticmethod
    def validate_sasquatch(form_data):
        is_valid = True

        if len(form_data['location']) <3:
            flash('Location must be entered','location')
            is_valid = False
        if form_data['num_of_sasquatches'] =="":
            flash('num_of_sasquatches must be entered','num_of_sasquatches')
            is_valid = False
        if form_data['date_of_sighting'] == "":
            flash('Date of sighting must be given!','date_of_sighting')
            is_valid = False
        if len(form_data['what_happened']) <3:
            flash('what happened must be entered','what_happened')
            is_valid = False
            
        if int(form_data['num_of_sasquatches']) <0:
            flash('num_of_sasquatch must be positive','num_of_sasquatches')
            is_valid = False
        return is_valid

    @classmethod
    def save(cls,data):
        query = "INSERT INTO sasquatches (location,num_of_sasquatches,date_of_sighting,what_happened,user_id) VALUES (%(location)s,%(num_of_sasquatches)s,%(date_of_sighting)s,%(what_happened)s,%(user_id)s);"
        new_sasquatch_id = connectToMySQL('sasquatch').query_db(query,data)

        return new_sasquatch_id

    @classmethod
    def get_one(cls,data):

        query = "SELECT * FROM sasquatches LEFT JOIN users on sasquatches.user_id = users.id LEFT JOIN skeptics ON skeptics.sasquatch_id = sasquatches.id LEFT JOIN users as users_2 ON users_2.id = skeptics.user_id WHERE sasquatches.id= %(id)s;"
        
        results = connectToMySQL("sasquatch").query_db(query,data)
        sasquatch = cls(results[0])
        data = {
            'id' : results[0]['users.id'],
            'first_name' : results[0]['first_name'],
            'last_name':results[0]['last_name'],
            'email':results[0]['email'],
            'password':results[0]['password'],
            'created_at':results[0]['users.created_at'],
            'updated_at':results[0]['users.updated_at']
        }
        sasquatch.reported_user = User(data)
        sasquatch.skeptic_users = []

        for row in results:


            
            data2 = {
                'id' : row['users_2.id'],
                'first_name' : row['users_2.first_name'],
                'last_name':row['users_2.last_name'],
                'email':row['users_2.email'],
                'password':row['users_2.password'],
                'created_at':row['users_2.created_at'],
                'updated_at':row['users_2.updated_at']
            }
            
            sasquatch.skeptic_users.append(User(data2))

        return sasquatch
        


    @classmethod
    def update(cls,data):
        query = "UPDATE sasquatches SET location = %(location)s,num_of_sasquatches = %(num_of_sasquatches)s, date_of_sighting = %(date_of_sighting)s, what_happened = %(what_happened)s WHERE id = %(id)s;"
        connectToMySQL("sasquatch").query_db(query,data)


    @classmethod
    def delete(cls,data):
        query = "DELETE FROM sasquatches WHERE id = %(id)s;"

        connectToMySQL("sasquatch").query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT sasquatches.*,users.*,count(skeptics.user_id) as count FROM sasquatches JOIN users ON sasquatches.user_id = users.id LEFT JOIN skeptics ON skeptics.sasquatch_id = sasquatches.id group by sasquatches.id;"
        results = connectToMySQL("sasquatch").query_db(query)
        all_sas = []

        for row in results:
            sas = cls(row)
            data = {
                'id' : row['users.id'],
                'first_name' : row['first_name'],
                'last_name':row['last_name'],
                'email':row['email'],
                'password':row['password'],
                'created_at':row['users.created_at'],
                'updated_at':row['users.updated_at']
            }
            
            sas.reported_user = User(data)
            sas.count = row['count']
            all_sas.append(sas)

        return all_sas

    
