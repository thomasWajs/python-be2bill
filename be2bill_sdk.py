# -*- coding: utf-8 -*-
import cgi
import hashlib
from UserDict import DictMixin

#The version of the API used
BE2BILL_API_VERSION = '2.0'

class MissingSetting(Exception):
    def __init__(self, setting_name):
        super(MissingSetting, self).__init__('Paramètre de configuration Be2Bill manquant : ' + setting_name)

class MissingRequiredField(Exception):
    def __init__(self, field_name):
        super(MissingRequiredField, self).__init__('Champ de requête obligatoire manquant : ' + field_name)

class Be2BillConfig(object):
    '''Global configuration with user credentials'''
    IDENTIFIER = None
    PASSWORD = None
    FORM_TARGET = None
    FORM_TARGET_SECONDARY = None

    @classmethod
    def configure(cls, identifier, password, form_target, form_target_secondary=None):
        cls.IDENTIFIER = identifier
        cls.PASSWORD = password
        cls.FORM_TARGET = form_target
        cls.FORM_TARGET_SECONDARY = form_target_secondary

    @classmethod
    def check_config(cls):
        if cls.IDENTIFIER is None:
            raise MissingSetting('IDENTIFIER')
        if cls.PASSWORD is None:
            raise MissingSetting('PASSWORD')
        if cls.FORM_TARGET is None:
            raise MissingSetting('FORM_TARGET')

class Be2BillFields:
    '''Available fields enum'''
    OPERATIONTYPE = "OPERATIONTYPE"
    CLIENTIDENT = "CLIENTIDENT"
    DESCRIPTION = "DESCRIPTION"
    ORDERID = "ORDERID"
    AMOUNT = "AMOUNT"

    CARDTYPE = "CARDTYPE"
    CLIENTEMAIL = "CLIENTEMAIL"
    CARDFULLNAME = "CARDFULLNAME"
    LANGUAGE = "LANGUAGE"
    EXTRADATA = "EXTRADATA"
    CLIENTDOB = "CLIENTDOB"
    CLIENTADDRESS = "CLIENTADDRESS"
    CREATEALIAS = "CREATEALIAS"
    _3DSECURE = "3DSECURE"
    _3DSECUREDISPLAYMODE = "3DSECUREDISPLAYMODE"
    USETEMPLATE = "USETEMPLATE"
    HIDECLIENTEMAIL = "HIDECLIENTEMAIL"
    HIDECARDFULLNAME = "HIDECARDFULLNAME"
#Create an Alias for fast reference
F = Be2BillFields

class Be2BillRequest(DictMixin):
    '''Base class for all Be2Bill requests.
    Each subclass correspond to one kind of available request in the Be2Bill API.
    Subclasses must be instanciated to issue one request.
    '''
    #Subclasses should populate these two tuples at class-level
    REQUIRED_FIELDS = ()
    OPTIONNAL_FIELDS = ()

    def __init__(self, **kwargs):
        self.ALL_FIELDS = self.REQUIRED_FIELDS + self.OPTIONNAL_FIELDS
        self.fields = {}
        self.set_fields(**kwargs)

    #===========================================================================
    # Dictionnary access to the fields
    #===========================================================================
    def __setitem__(self, field_name, value):
        if field_name not in self.ALL_FIELDS:
            raise ValueError("Le champ {} n'est pas disponible pour ce type de requête".format(field_name))
        self.fields[field_name] = unicode(value)
    def __getitem__(self, field_name, value):
        return self.fields.__getitem__(field_name)
    def __delitem__(self, field_name):
        self.fields__delitem__(field_name)
    def keys(self):
        return self.fields.keys()
    def __contains__(self, field_name):
        return self.fields.__contains__(field_name)
    def __iter__(self):
        return self.fields.__iter__()
    def iteritems(self):
        return self.fields.iteritems()

    def set_fields(self, **kwargs):
        '''Helper method that allows to set fields conveniently.
        Accept only named attributes. Each attribute is converted to a field
        by removing underscores and uppercasing its name.
        
            request.set_fields(operation_type='payment', client_ident='chuck_norris')
        '''
        for field_name, value in kwargs.items():
            field_name = field_name.replace('_', '').upper()
            self[field_name] = value

    #===========================================================================
    # Field processing
    #===========================================================================
    def _compute_be2bill_hash(self):
        password = Be2BillConfig.PASSWORD
        parameters = sorted("{}={}".format(key, value) for key, value in self.fields.items())
        clear_string = password + password.join(parameters) + password
        return hashlib.sha256(clear_string).hexdigest()

    def _check_required_fields(self):
        for required_field_name in self.REQUIRED_FIELDS:
            if required_field_name not in self.fields.keys():
                raise MissingRequiredField(required_field_name)

    def _prepare_fields(self):
        Be2BillConfig.check_config()
        self._check_required_fields()
        self.fields['IDENTIFIER'] = Be2BillConfig.IDENTIFIER
        self.fields['VERSION'] = BE2BILL_API_VERSION
        self.fields['HASH'] = self._compute_be2bill_hash()

class Be2BillForm(Be2BillRequest):
    '''Request by POST request through a form'''
    REQUIRED_FIELDS = (F.OPERATIONTYPE, F.CLIENTIDENT, F.DESCRIPTION,
                       F.ORDERID, F.AMOUNT)
    OPTIONNAL_FIELDS = (F.CARDTYPE, F.CLIENTEMAIL, F.CARDFULLNAME,
                        F.LANGUAGE, F.EXTRADATA, F.CLIENTDOB,
                        F.CLIENTADDRESS, F.CREATEALIAS, F._3DSECURE,
                        F._3DSECUREDISPLAYMODE, F.USETEMPLATE, F.HIDECLIENTEMAIL,
                        F.HIDECARDFULLNAME)

    def render_form_inputs(self):
        self._prepare_fields()
        html_string = ''
        for field_name, value in self.fields.items():
            html_string += '<input type="hidden" name="{}" value="{}">'.format(field_name, cgi.escape(value, True))
        return html_string

    def get_form_target(self):
        return Be2BillConfig.FORM_TARGET

try:
    from django.conf import settings
    Be2BillConfig.configure(getattr(settings, 'BE2BILL_IDENTIFIER', None),
                            getattr(settings, 'BE2BILL_PASSWORD', None),
                            getattr(settings, 'BE2BILL_FORM_TARGET', None),
                            getattr(settings, 'BE2BILL_FORM_TARGET_SECONDARY', None))
except ImportError: #django isn't used
    pass
