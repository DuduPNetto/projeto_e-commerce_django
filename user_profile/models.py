import re

from django.contrib.auth.models import User
from django.db import models
from django.forms import ValidationError

from utils.validatecpf import validate_cpf


class UserProfile(models.Model):
    class Meta:
        verbose_name = 'UserProfile'
        verbose_name_plural = 'UserProfiles'

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField()
    birthday = models.DateField()
    cpf = models.CharField(max_length=11)
    address = models.CharField(max_length=100)
    number = models.CharField(max_length=5)
    complement = models.CharField(max_length=50)
    neighborhood = models.CharField(max_length=50)
    cep = models.CharField(max_length=8)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2, default='SP',
                             choices=(('AC', 'Acre'),
                                      ('AL', 'Alagoas'),
                                      ('AP', 'Amapá'),
                                      ('AM', 'Amazonas'),
                                      ('BA', 'Bahia'),
                                      ('CE', 'Ceará'),
                                      ('DF', 'Distrito Federal'),
                                      ('ES', 'Espírito Santo'),
                                      ('GO', 'Goiás'),
                                      ('MA', 'Maranhão'),
                                      ('MT', 'Mato Grosso'),
                                      ('MS', 'Mato Grosso do Sul'),
                                      ('MG', 'Minas Gerais'),
                                      ('PA', 'Pará'),
                                      ('PB', 'Paraíba'),
                                      ('PR', 'Paraná'),
                                      ('PE', 'Pernambuco'),
                                      ('PI', 'Piauí'),
                                      ('RJ', 'Rio de Janeiro'),
                                      ('RN', 'Rio Grande do Norte'),
                                      ('RS', 'Rio Grande do Sul'),
                                      ('RO', 'Rondônia'),
                                      ('RR', 'Roraima'),
                                      ('SC', 'Santa Catarina'),
                                      ('SP', 'São Paulo'),
                                      ('SE', 'Sergipe'),
                                      ('TO', 'Tocantins'),)
                             )

    def __str__(self) -> str:
        return f'{self.user}'

    def clean(self) -> None:
        error_messages = {}

        send_cpf = self.cpf or None
        saved_cpf = None
        profile = UserProfile.objects.filter(cpf=send_cpf).first()

        if profile:
            saved_cpf = profile.cpf

            if saved_cpf is not None and self.pk != profile.pk:
                error_messages['cpf'] = 'CPF already exists.'

        if not validate_cpf(self.cpf):
            error_messages['cpf'] = 'CPF invalid.'

        if re.search(r'[^0-9]', self.cep) or len(self.cep) < 8:
            error_messages['cep'] = 'CEP invalid.'

        if error_messages:
            raise ValidationError(error_messages)
