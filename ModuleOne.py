'''
ModuleOne.py
A program for transferring json into a sql database using peewee
Leslie Wilson, April 2018
'''

from peewee import *
import json

db = SqliteDatabase('test.db')

# Basemodel that everything inherits from

class BaseModel(Model):
    class Meta:
        database = db

# Create the person and address models

class Person(BaseModel):
    person_id = PrimaryKeyField()
    firstname = CharField()
    middlename = CharField(null=True)
    lastname = CharField()


class Address(BaseModel):
    address_id = PrimaryKeyField()
    street = CharField()
    city = CharField()
    zipcode = IntegerField()
    person = ForeignKeyField(Person, to_field="person_id")


def main():

    # create a person table and address table if they don't exist

    db.create_tables([Person, Address])

        # create person instances

    jsondata = json.load(open('input.json'))

    for person in jsondata:
        for address in person['Address']:
            human = Person(firstname= person['firstname'], middlename = person['middlename'], lastname = person['lastname'])
            place = Address(street= address['street'], city= address['city'], zipcode= int(address['zipcode']), person= 1)
        # save them to database in one transaction

    with db.atomic():
        human.save()
        place.save()

    print()
    print("-- get some information and display it")

    sam = Person.get(Person.firstname == 'sam')
    print("person: {} {}".format(sam.firstname, sam.lastname))

    newyork = Address.get(Address.city == 'new york')
    print("place: {} {}".format(newyork.street, newyork.city))

    print("a place corresponds to 1 person : place '{}' -> person '{}' ".format(
              newyork.city, newyork.person.firstname))
main()
