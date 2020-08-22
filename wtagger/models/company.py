
from wtagger.extensions import db


class Company(db.Model):
    __tablename__ = 'company'

    id = db.Column(db.Integer, primary_key=True)
    
    company_name_ko = db.Column(db.String(64), index=True)
    company_name_en = db.Column(db.String(64), index=True)
    company_name_ja = db.Column(db.String(64), index=True)

    company_tag_ko = db.Column(db.String(1024), index=True)
    company_tag_en = db.Column(db.String(1024), index=True)
    company_tag_ja = db.Column(db.String(1024), index=True)



    def __init__(self, **kwargs):
        super(Company, self).__init__(**kwargs)

    def full_name(self):
        return '%s %s' % (self.first_name, self.last_name)


    # @property
    # def password(self):
    #     raise AttributeError('`password` is not a readable attribute')

    # @password.setter
    # def password(self, password):
    #     self.password_hash = generate_password_hash(password)

    @classmethod
    def searchByName(cls, wantToFind):
        companies = cls.query.filter(cls.company_tag_ko.like(f"%{wantToFind}%")).all()
        return companies

    
    # @staticmethod
    # def generate_fake(count=100, **kwargs):
    #     """Generate a number of fake users for testing."""
    #     from sqlalchemy.exc import IntegrityError
    #     from random import seed, choice
    #     from faker import Faker

    #     fake = Faker()
    #     roles = Role.query.all()

    #     seed()
    #     for i in range(count):
    #         u = User(
    #             first_name=fake.first_name(),
    #             last_name=fake.last_name(),
    #             email=fake.email(),
    #             password='password',
    #             confirmed=True,
    #             role=choice(roles),
    #             **kwargs)
    #         db.session.add(u)
    #         try:
    #             db.session.commit()
    #         except IntegrityError:
    #             db.session.rollback()

    def __repr__(self):
        return '<Company \'%s\'>' % self.company_name_ko
