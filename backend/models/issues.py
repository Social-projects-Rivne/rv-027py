from app_builder import db


class Attachment(db.Model):
    """This class is used for attachment table in database."""

    __tablename__ = 'attachments'

    id = db.Column(db.Integer, primary_key=True)
    issue_id = db.Column(db.ForeignKey(u'issues.id'), index=True)
    image_url = db.Column(db.Text)
    delete_date = db.Column(db.Date)

    issue = db.relationship(u'Issue')


class Category(db.Model):
    """This class is used for category table in database."""

    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.Text)
    favicon = db.Column(db.Text)


class IssueHistory(db.Model):
    """This class is used for issueHistory table in database."""

    __tablename__ = 'issue_History'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey(u'users.id'))
    issue_id = db.Column(db.ForeignKey(u'issues.id'), index=True)
    status_id = db.Column(db.ForeignKey(u'statuses.id'), index=True)
    transaction_date = db.Column(db.Date)
    delete_date = db.Column(db.Date)

    issue = db.relationship(u'Issue')
    status = db.relationship(u'Status')
    user = db.relationship(u'User')


class Issue(db.Model):
    """This class is used for issues table in database."""

    __tablename__ = 'issues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    user_id = db.Column(db.ForeignKey(u'users.id'), index=True)
    category_id = db.Column(db.ForeignKey(
        u'category.id'), nullable=False, index=True)
    location = db.Column(db.Text)
    description = db.Column(db.Text)
    open_date = db.Column(db.Date)
    close_date = db.Column(db.Date)
    delete_date = db.Column(db.Date)

    category = db.relationship(u'Category')
    user = db.relationship(u'User')


class Status(db.Model):
    """This class is used for status table in database."""

    __tablename__ = 'statuses'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Text)
