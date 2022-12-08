from django.test import TestCase
from lessons.models import User, Payment
from lessons.forms import PaymentForm

class PaymentFormTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email = 'john.doe@example.org',
            first_name='John',
            last_name = 'Doe',
            password = 'Password123',
            outstanding_balance = -200
        )
        self.form_input = {
            'amount_paid':'100'
        }

    def test_valid_payment_form(self):
        form = PaymentForm(data = self.form_input)
        self.assertTrue(form.is_valid())

    def test_payment_form_has_necessary_fields(self):
        form = PaymentForm()
        self.assertIn('amount_paid', form.fields)

    def test_negative_amount_paid(self):
        self.form_input['amount_paid']='-100'
        form = PaymentForm(data = self.form_input)
        self.assertFalse(form.is_valid())

    def test_payment_form_must_save_correctly(self):
        form = PaymentForm(data = self.form_input)
        before_count = Payment.objects.count()
        newPayment = form.save(commit=False)
        newPayment.student = self.user
        newPayment.balance_before = self.user.outstanding_balance
        newPayment.balance_after = self.user.outstanding_balance + newPayment.amount_paid
        newPayment.save()
        after_count = Payment.objects.count()
        self.assertEqual(after_count, before_count+1)
        payment = Payment.objects.get(student=self.user)
        self.assertEqual(payment.amount_paid,100)
        self.assertEqual(payment.balance_before,-200)
        self.assertEqual(payment.balance_after,-100)
