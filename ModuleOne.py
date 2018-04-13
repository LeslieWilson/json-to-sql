'''
ModuleOne.py
A program for transferring json into a sql database using peewee
Leslie Wilson, April 2018
'''

from peewee import *
import json

db = SqliteDatabase('test.db')
#this is a peewee command to make sqlite database

# Basemodel that everything inherits from, (i don't know what model is)

class BaseModel(Model):
    class Meta:
        #I don't know what meta is, class meta is a peewee thing
        database = db

# Create the person and address models that hook up with the database

class Person(BaseModel):
    person_id = PrimaryKeyField()
    #here im just naming the unique id, which is automatically made when you make an entry into the database
    firstname = CharField()
    middlename = CharField(null=True)
    lastname = CharField()


class Address(BaseModel):
    address_id = PrimaryKeyField()
    street = CharField()
    city = CharField()
    zipcode = IntegerField()
    person = ForeignKeyField(Person, to_field="person_id")
    #this connects the persno id to the address


def main():

    # create a person table and address table if they don't exist

    db.create_tables([Person, Address])

    

    jsondata = json.load(open('input.json'))

    for person in jsondata:
        for address in person['Address']:
            human = Person(firstname= person['firstname'], middlename = person['middlename'], lastname = person['lastname'])
            place = Address(street= address['street'], city= address['city'], zipcode= int(address['zipcode']), person= 1)
        # save them to database in one transaction
        #setting a new person and place with a new address in the database.

    with db.atomic():
        human.save()
        place.save()

#this is a search query, t get info from the datavbase. this si an example of how to serach the database and get informnation out



    print()

    print("-- now I'll get some information and display it")

    sam = Person.get(Person.firstname == 'sam')
    print("person: {} {}".format(sam.firstname, sam.lastname))

    newyork = Address.get(Address.city == 'new york')
    print("place: {} {}".format(newyork.street, newyork.city))

    print("a place corresponds to 1 person : place '{}' -> person '{}' ".format(
              newyork.city, newyork.person.firstname))
main()
