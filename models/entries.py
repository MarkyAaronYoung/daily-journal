class Entries():

    def __init__(self, id, concept, entry, date, moodId):
        self.id = id
        self.concept = concept
        self.entry = entry
        self.date = date
        self.moodId = moodId
        self.mood = None

    def __repr__(self):
         return f"{self.entry} on date {self.date} I learned {self.concept} and I am {self.moodId}"
