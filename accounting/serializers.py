from rest_framework import serializers
from accounting.models import bill_of_payment



class BillOfPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = bill_of_payment
        fields = ['id','invoice_no','date_of_invoice','due_date','amount','bill_upload','payments',]



    