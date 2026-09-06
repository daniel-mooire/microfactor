from microfactor.core import MicroshareDataProvider
from microfactor.core.protocols import DataProvider, IndustrySource, UniverseSource


class _FakePro:
    def universe(self, *, universe=None, start_date=None, end_date=None, fields=None):
        raise NotImplementedError

    def index_member_all(self, fields=None):
        raise NotImplementedError


def test_microshare_provider_satisfies_data_provider():
    assert isinstance(MicroshareDataProvider(pro=None), DataProvider)


def test_fake_pro_satisfies_source_protocols():
    assert isinstance(_FakePro(), UniverseSource)
    assert isinstance(_FakePro(), IndustrySource)
