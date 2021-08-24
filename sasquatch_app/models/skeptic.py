from sasquatch_app.config.mysqlconnection import connectToMySQL


class Skeptic:
    def __init__(self,data):
        self.user_id  = data['user_id']
        self.sasquatch_id  = data['sasquatch_id']
        
    @classmethod
    def create_skeptic(cls,data):
        query = "INSERT INTO skeptics (user_id,sasquatch_id) VALUES (%(user_id)s,%(sasquatch_id)s);"
        new_skeptic_id = connectToMySQL('sasquatch').query_db(query,data)

        return new_skeptic_id
    
    @classmethod
    def delete_skeptic(cls,data):
        query = "DELETE FROM skeptics WHERE user_id =%(user_id)s  and sasquatch_id= %(sasquatch_id)s;"
        connectToMySQL('sasquatch').query_db(query,data)

    @classmethod
    def delete_skeptic_all(cls,data):
        query = "DELETE FROM skeptics WHERE sasquatch_id= %(id)s;"
        connectToMySQL('sasquatch').query_db(query,data)

