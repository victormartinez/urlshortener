from datetime import datetime

import factory
from faker import Factory as FakerFactory

from urlshorten.db.models import DBShortenedUrl

faker = FakerFactory.create("pt_BR")


class DBShortenedUrlFactoryData(factory.Factory):
    class Meta:
        model = DBShortenedUrl

    id = factory.LazyFunction(lambda: faker.uuid4())
    destination_url = factory.LazyFunction(lambda: faker.url())
    enabled = True
    created_at = datetime.now()
    updated_at = datetime.now()
