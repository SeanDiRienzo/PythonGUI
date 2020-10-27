#Author Sean Di Rienzo
import unittest
from Application import Session as api
import qsqltest

"""Sean Di Rienzo"""


class MyTestCase(unittest.TestCase):

    def test_add_filter(self):
        milk_type = "Buffalo Cow"
        characteristics = "Creamy and fresh, this delicious locally-made cheese offers the traditional taste of Italy."
        milk_treatment_type = 'Pasteurized'
        """ we are only expecting to have one row after executing our search"""
        expected_rowcount = 1
        """ the cheese_id of the record we're trying to filter is 1944, we will assert this"""
        expected_cheese_id = 1944
        app = api()
        model = app.get_model()
        model.select()
        while model.canFetchMore():
            model.fetchMore()
        print(model.columnCount())
        print(model.rowCount())
        """Using the same filter settings as provided in the example of the final project handout"""
        model.setFilter(
            "MilkTypeEn = '" + milk_type + "' AND CharacteristicsEn = '" + characteristics + "' AND MilkTreatmentTypeEn = '" + milk_treatment_type + "'")
        print(model.rowCount())
        cheeseid = model.record(0).value("CheeseId")
        print(cheeseid, expected_cheese_id)
        print(model.rowCount(), expected_rowcount)
        self.assertEqual(cheeseid, expected_cheese_id)
        self.assertEqual(model.rowCount(), expected_rowcount)
    if __name__ == '__main__':
        unittest.main()
