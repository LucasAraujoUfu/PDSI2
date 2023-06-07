from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, nome=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.nome = nome
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    nome = models.TextField(blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class dataset(models.Model):
    SEXO = models.IntegerField()
    DT_NASCIMENTO = models.IntegerField()
    NOME_CIDADE = models.IntegerField()
    ESTADO_CIVIL = models.IntegerField()
    FORMA_INGRESSO = models.IntegerField()
    MODALIDADE_INGRESSO = models.IntegerField()
    ANO_INGRESSO = models.IntegerField()
    CRA_PERIODO_INGRESSO = models.FloatField()
    CRA_GERAL = models.FloatField()
    FORMA_EVASAO = models.BooleanField()
