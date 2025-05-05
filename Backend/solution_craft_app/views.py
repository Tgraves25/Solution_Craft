from django.http import JsonResponse
from django.contrib.auth import authenticate, get_user_model
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated

from .models import Ticket
from .serializers import TicketSerializer

User = get_user_model()
CustomUser = get_user_model()

# Root API endpoint
def api_root(request):
    return JsonResponse({
        "message": "Welcome to Solution Craft API",
        "endpoints": [
            "/api/signup/",
            "/api/login/",
            "/api/tickets/",
            "/api/tickets/<id>/",
            "/api/ai_recommendation/"
        ]
    })


# SIGNUP VIEW
class SignupView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not (username and email and password):
            return Response({"detail": "username, email, and password are required"}, status=400)

        if User.objects.filter(username=username).exists():
            return Response({"detail": "Username already taken"}, status=400)

        if User.objects.filter(email=email).exists():
            return Response({"detail": "Email already taken"}, status=400)

        user = User.objects.create_user(username=username, email=email, password=password)
        user.is_active = True
        user.save()

        refresh = RefreshToken.for_user(user)
        return Response({
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh)
        }, status=201)


# LOGIN VIEW
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not (username and password):
            return Response({"detail": "Username and password required"}, status=400)

        user = authenticate(username=username, password=password)

        if not user:
            return Response({"detail": "Invalid credentials"}, status=401)

        refresh = RefreshToken.for_user(user)
        return Response({
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh)
        })


# TICKET LIST & CREATE (GET, POST)
from rest_framework.exceptions import ValidationError

class TicketAPIView(generics.ListCreateAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        assigned_to_id = self.request.data.get('assigned_to')  # Get the selected technician's ID

        # Log assigned_to_id for debugging
        print(f"Assigned to ID: {assigned_to_id}")

        if not assigned_to_id:
            raise ValidationError("Assigned technician ID is required.")

        try:
            # Fetch the technician object
            assigned_to = CustomUser.objects.get(id=assigned_to_id)
        except CustomUser.DoesNotExist:
            raise ValidationError("Assigned technician does not exist.")
        
        # Save the ticket with the valid assigned_to user
        serializer.save(assigned_to=assigned_to)



# TICKET DETAIL (GET, PUT, DELETE)
class TicketDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [permissions.IsAuthenticated]


# AI Recommendation Placeholder Endpoint
def ai_recommendation(request):
    return JsonResponse({"message": "AI recommendation endpoint is active!"})
