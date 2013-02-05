python-be2bill
==============

An sdk implementing the be2bill API.
Only POST requests through a form are implemented for now, contributions to extend the sdk are welcome.

## Installation

Working in your project's [virtualenv](http://www.virtualenv.org/en/latest/index.html):
```
git clone https://github.com/thomasWajs/python-be2bill.git
cd python-be2bill
python setup.py install
```

## Configuration

To initialize the sdk, make a call to Be2BillConfig.configure

```
from be2bill_sdk import Be2BillConfig

Be2BillConfig.configure(identifier='chuck norris',
						password='your password',
						form_target='https://secure-test.be2bill.com/front/form/process.php',
						form_target_secondary='https://secure-test.be2bill.com/front/form/process.php'):
```

Alternatively, if you use django (if not, you should), you can just set these 4 settings in the django settings :

```
BE2BILL_IDENTIFIER = 'chuck norris'
BE2BILL_PASSWORD = 'your password'

BE2BILL_FORM_TARGET = 'https://secure-test.be2bill.com/front/form/process.php'
BE2BILL_FORM_TARGET_SECONDARY = 'https://secure-test.be2bill.com/front/form/process.php'
```

## Usage

To create a request, you must create any Be2BillRequest subclass. Each keyword argument is stored as part of the request.
Instead of using the Be2Bill uppercase parameters,
you can be more pythonic by using lowercase_with_undersocre, and it will be converted by stripping the underscore and uppercasing :

```
#These two are equivalent
request = Be2BillRequest(OPERATIONTYPE="payment")
request = Be2BillRequest(operation_type="payment")
```

## Form usage

1/ Prepare a form to be rendered inside your html page :

```
start_payment_form = Be2BillForm(operation_type="payment",
                           		client_ident=client_ident,
                           		description=description,
                           		order_id=order.id,
                           		amount=amount,

                           		client_email=order.billing_detail_email,
                           		card_full_name=fullname)
```

2/ Render it into the page (exemple with the django template language) :

```
<form action="{{start_payment_form.get_form_target}}" method="POST"> 
{{start_payment_form.render_form_inputs|safe}}
<input type="submit" value="payer">
</form>
{% endblock %}
```
