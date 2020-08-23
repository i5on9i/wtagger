from dataclasses import dataclass

from sqlalchemy import or_

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
    def searchByName(cls, wantToFind, lang):
        colCompanyName = f"company_name_{lang}"
        if not hasattr(cls, colCompanyName):
            return []

        compNameCol = getattr(cls, colCompanyName)
        companies = (
            cls.query.with_entities(compNameCol)
            .filter(compNameCol.like(f"%{wantToFind}%"))
            .all()
        )
        ret = []
        for com in companies:
            ret.append(getattr(com, colCompanyName))
        return ret

    @classmethod
    def searchByTag(cls, wantToFind, lang):
        colCompanyName = f"company_name_{lang}"
        if not hasattr(cls, colCompanyName):
            return []

        compNameCol = getattr(cls, colCompanyName)
        companies = (
            cls.query.with_entities(compNameCol)
            .filter(
                or_(
                    # delimiter = "|"
                    cls.company_tag_ko.like(f"%|{wantToFind}%"),
                    cls.company_tag_ko.like(f"%{wantToFind}|%"),
                    cls.company_tag_ko.like(wantToFind),
                    cls.company_tag_ja.like(f"%|{wantToFind}%"),
                    cls.company_tag_ja.like(f"%{wantToFind}|%"),
                    cls.company_tag_ja.like(wantToFind),
                    cls.company_tag_en.like(f"%|{wantToFind}%"),
                    cls.company_tag_en.like(f"%{wantToFind}|%"),
                    cls.company_tag_en.like(wantToFind),
                )
            )
            .all()
        )
        ret = []
        for com in companies:
            comName = getattr(com, colCompanyName)
            if comName:
                ret.append(comName)
        return ret

    def __repr__(self):
        return "<Company '%s'>" % self.company_name_ko
