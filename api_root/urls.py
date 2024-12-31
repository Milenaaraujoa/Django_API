from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AlunoViewSet, TurmaViewSet, EventoViewSet, AdminActionsViewSet

router = DefaultRouter()
router.register('alunos', AlunoViewSet)
router.register('turmas', TurmaViewSet)
router.register('eventos', EventoViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin-actions/', AdminActionsViewSet.as_view({'post': 'enviar_mensagem'})),
]
