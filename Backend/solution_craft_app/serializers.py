from rest_framework import serializers
from .models import Ticket

class TicketSerializer(serializers.ModelSerializer):
    assigned_to_name = serializers.CharField(source='assigned_to.username', read_only=True)
    
    class Meta:
        model = Ticket
        fields = '__all__' 