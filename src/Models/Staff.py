from src.Connector.MA import MA
class Staff(object):
    def __init__(self, first_name, last_name, team, location):
        self.first_name = first_name
        self.last_name = last_name
        self.team = team
        self.location = location

    @staticmethod
    def get_all_staffs():
        result = MA().query("SELECT first_name, last_name, team, location FROM Staff")
        all_staffs = list(map(lambda x: Staff(*x), result))
        return all_staffs

if __name__ == '__main__':
    a = Staff.get_all_staffs()
    for i in a:
        print(i.team)
        print(i.first_name)
        print(i.last_name)
        print(i.location)
