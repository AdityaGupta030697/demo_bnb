import mongoengine
import re

MONGODB_ALIAS_CORE = 'core'
MONGODB_DB_NAME = 'demo_bnb'


class PhoneField(mongoengine.StringField):
    """
    A field that validates input as phone.
    """
    PHONE_REGEX = re.compile("^\+[1-9]{1}[0-9]{3,14}$")

    def validate(self, value):
        if not PhoneField.PHONE_REGEX.match(value):
            self.error('Invalid phone number: %s' % value)
        super(PhoneField, self).validate(value)


def global_init():
    mongoengine.register_connection(alias=MONGODB_ALIAS_CORE,
                                    name=MONGODB_DB_NAME)
