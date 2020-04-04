import datetime

def get_user_email():
    return None if auth.user is None else auth.user.email

def get_user_full_name():
    return None if auth.user is None else auth.user.first_name + ' ' + auth.user.last_name


db.define_table('tweet_users_table',
    Field('name', 'text'),
    Field('user_data', 'text')
)

# Set defaults!