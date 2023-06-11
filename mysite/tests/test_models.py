from django.test import TestCase
from mysite.models import dataset


class dataset_test(TestCase):
    def setUp(self):
        dataset.objects.create(
            SEXO=1,
            DT_NASCIMENTO=1990,
            NOME_CIDADE=3,
            ESTADO_CIVIL=2,
            FORMA_INGRESSO=1,
            MODALIDADE_INGRESSO=3,
            ANO_INGRESSO=2017,
            CRA_PERIODO_INGRESSO=8.5,
            CRA_GERAL=8.2,
            FORMA_EVASAO=True,
        )

    def test_dataset_creation(self):
        obj = dataset.objects.get(pk=1)
        self.assertEqual(obj.SEXO, 1)
        self.assertEqual(obj.DT_NASCIMENTO, 1990)
        self.assertEqual(obj.NOME_CIDADE, 3)
        self.assertEqual(obj.ESTADO_CIVIL, 2)
        self.assertEqual(obj.FORMA_INGRESSO, 1)
        self.assertEqual(obj.MODALIDADE_INGRESSO, 3)
        self.assertEqual(obj.ANO_INGRESSO, 2017)
        self.assertEqual(obj.CRA_PERIODO_INGRESSO, 8.5)
        self.assertEqual(obj.CRA_GERAL, 8.2)
        self.assertEqual(obj.FORMA_EVASAO, True)
