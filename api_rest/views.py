from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Alunos, Turmas, Evento
from .serializers import AlunoSerializer, TurmaSerializer, EventoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LoginSerializer
import csv
from django.http import HttpResponse


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Alunos.objects.all()
    serializer_class = AlunoSerializer
    permission_classes = [permissions.IsAuthenticated]

class TurmaViewSet(viewsets.ModelViewSet):
    queryset = Turmas.objects.all()
    serializer_class = TurmaSerializer
    permission_classes = [permissions.IsAuthenticated]

class EventoViewSet(viewsets.ModelViewSet):
    queryset = Evento.objects.all()
    serializer_class = EventoSerializer
    permission_classes = [permissions.IsAuthenticated]

# Endpoint Simulado para enviar mensagens no WhatsApp
from rest_framework.decorators import action

class AdminActionsViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['post'])
    def enviar_mensagem(self, request):
        numero = request.data.get('telefone')
        mensagem = request.data.get('mensagem')
        if numero and mensagem:
            # Aqui você poderia integrar uma API de WhatsApp real
            return Response({"mensagem": f"Mensagem enviada para {numero}"}, status=status.HTTP_200_OK)
        return Response({"erro": "Dados incompletos"}, status=status.HTTP_400_BAD_REQUEST)

def exportar_alunos_csv(request):

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="alunos.csv"'


    writer = csv.writer(response)
    writer.writerow(['CPF', 'Nome', 'Email', 'Data de Nascimento', 'Telefone', 'Endereço'])

    alunos = Alunos.objects.all().values_list('cpf_alunos', 'nome', 'email', 'data_nascimento', 'telefone', 'endereco')

    for aluno in alunos:
        writer.writerow(aluno)

    return response