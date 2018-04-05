from peewee import *
import json

db = SqliteDatabase('test.db')

class BaseModel(Model):
    class Meta:
        database = db



class Person(BaseModel):
    person_id = PrimaryKeyField()
    firstname = CharField()
    middlename = CharField(null=True)
    lastname = CharField()

#Why have seperate tables for name and address instead of just a person with name, address, city, zip etc?

class Address(BaseModel):
    address_id = PrimaryKeyField()
    street = CharField()
    city = CharField()
    zipcode = IntegerField()
    # person = ForeignKeyField(Person, to_field="person_id")
    # commented out foreign key but necessary to associate tables
    # create a person table if it does not exist

db.create_tables([Person, Address])
    # create person instances
jsondata = json.load(open('input.json'))

for person in jsondata:
    for address in person['Address']:
        human = Person(firstname= person['firstname'], middlename = person['middlename'], lastname = person['lastname'])
        place = Address(street= address['street'], city= address['city'], zipcode= int(address['zipcode']))
    # save them to database in one transaction
    # What's the best way to associate an address with the foreign key of this person when saving it in the database?

with db.atomic():
    human.save()
    place.save()



    # # simple SELECT example, select every fields and order by last name. if you don't specify the select columns it selects everything from that model.
    #
    # sq = Person.select().order_by(Person.lastname)
    #
    # for person in sq:
    #     print('{} {} {} age {}').format(
    #     person.firstname, person.middlename, or '\b',
    #     person.lastname, person.age))
    #
    # # example of JOINING conditions:
    #
    # # and
    #
    # sq.where((Person.firstname == 'Leslie') & (Person.lastname == 'Wilson'))
    #
    # # OR
    #
    # sq.where((Person.firstname == 'Leslie') | (Person.firstname == 'Julie'))
