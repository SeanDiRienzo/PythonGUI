#Author Sean Di Rienzo
import DataAccess as dl


class Session:

    def __init__(self):
        self.database_session = dl.CheeseRecord()

    def get_model(self):
        """Pass model to presentation layer"""
        return self.database_session.model.model

