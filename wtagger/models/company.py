from dataclasses import dataclass
from wtagger.extensions import db


@dataclass
class Company(db.Model):

    __tablename__ = "company"

    id: int = db.Column(db.Integer, primary_key=True)

    company_name_ko: str = db.Column(db.String(64), index=True)
    company_name_en: str = db.Column(db.String(64), index=True)
    company_name_ja: str = db.Column(db.String(64), index=True)

    company_tag_ko: str = db.Column(db.String(1024), index=True)
    company_tag_en: str = db.Column(db.String(1024), index=True)
    company_tag_ja: str = db.Column(db.String(1024), index=True)

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            if v is not None:
                setattr(self, k, v.strip())

    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    @classmethod
    def searchByName(cls, wantToFind):
        companies = cls.query.with_entities(cls.company_name_ko).filter(cls.company_name_ko.like(f"%{wantToFind}%")).all()
        ret = []
        for com in companies:
            ret.append(com.company_name_ko)
        return ret

    def __repr__(self):
        return "<Company '%s'>" % self.company_name_ko
