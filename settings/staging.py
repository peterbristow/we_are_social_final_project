from base import *
import dj_database_url

DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DATABASES['default'] = dj_database_url.parse('mysql://b73a49feeb6804:7272322c@eu-cdbr-west-01.cleardb.com/heroku_c792b4d395a7d48?reconnect=true')

# Stripe environment variables
STRIPE_PUBLISHABLE = os.getenv('STRIPE_PUBLISHABLE', 'pk_test_gxQDf9QL5eKhTgDpoWr560AP')
STRIPE_SECRET = os.getenv('STRIPE_SECRET', 'sk_test_WODOSCNhYTVcDu7nHCnnp34A')

# Paypal environment variables
SITE_URL = 'https://wearesocialfinalproject.herokuapp.com'
PAYPAL_NOTIFY_URL = 'https://wearesocialfinalproject.herokuapp.com/a-very-hard-to-guess-url/'
PAYPAL_RECEIVER_EMAIL = 'peterjb73+1@gmail.com'
