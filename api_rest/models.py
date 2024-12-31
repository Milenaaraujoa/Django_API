from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class AdminManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O email é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class Admin(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    nome = models.CharField(max_length=200)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = AdminManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class Base(models.Model):
    criacao = models.DateTimeField(auto_now_add=True)
    atualizacao = models.DateTimeField(auto_now=True)
    ativo = models.BooleanField(default=True)
    
    class Meta:
        abstract = True
    
class Alunos(Base):
    cpf_alunos = models.CharField(max_length=11, primary_key=True)
    nome = models.CharField(max_length=200)
    email = models.EmailField()
    data_nascimento = models.DateField()
    telefone = models.CharField(max_length=10)
    endereco = models.CharField(max_length=200)
    
    class Meta: 
        verbose_name = 'Aluno'
        verbose_name_plural = 'Alunos'
    
class Turmas(Base):
    id_turma = models.IntegerField(primary_key=True)
    modalidade = models.CharField(max_length=50)
    horario = models.TimeField()
    dia_semana = models.CharField(max_length=20)
    faixa_etaria = models.CharField(max_length=20)
    
    
    class Meta:
        verbose_name = 'Turma'
        verbose_name_plural = 'Turmas'
        
class Evento(Base):
    nome_evento = models.CharField(max_length=100, primary_key=True)
    vagas = models.IntegerField()
    cpf_aluno = models.CharField(max_length=11)
    data_evento = models.DateField()
    valor = models.DecimalField(max_digits=5, decimal_places=2)
    
    class Meta:
        verbose_name = 'Evento'
        verbose_name_plural = 'Eventos'
    
class Admin(Base):
    email = models.EmailField(primary_key=True)
    senha = models.CharField(max_length=50)
    
    
    class Meta:
        unique_together = ('email', 'senha')
