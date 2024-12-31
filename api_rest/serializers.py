from rest_framework import serializers
from .models import Alunos, Turmas, Evento
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework_simplejwt.tokens import RefreshToken


class AlunoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alunos
        fields = '__all__'

class TurmaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turmas
        fields = '__all__'

class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evento
        fields = '__all__'

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(request=self.context.get('request'), email=email, password=password)
        if not user:
            raise serializers.ValidationError("Credenciais inválidas.")

        refresh = RefreshToken.for_user(user)
        update_last_login(None, user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': user.email
        }