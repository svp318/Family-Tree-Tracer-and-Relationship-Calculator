import csv


class FamilyMatrix:
    def __init__(self):
        with open('family_matrix.csv', 'r') as f:
            reader = csv.reader(f)
            self.family_matrix = list(reader)

    def get_relationship(self, coordinates):
        return self.family_matrix[coordinates[0]][coordinates[1]]
