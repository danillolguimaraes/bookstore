import factory
from product.models import Product, Category

class CategoryFactory(factory.django.DjangoModelFactory):
    title = factory.Faker('pystr')
    slug = factory.Faker('pystr')
    description = factory.Faker('pystr')
    active = factory.Iterator([True, False])

    class Meta:
        model = Category

class ProductFactory(factory.django.DjangoModelFactory):
    title = factory.Faker('pystr')
    # description = factory.Faker('text', max_nb_chars=500)
    price = factory.Faker('pyint', min_value=0)
    # active = factory.Iterator([True, False])
    category = factory.RelatedFactory(CategoryFactory, factory_related_name='product_set')

    @factory.post_generation
    def category(self, create, extracted, **kwargs):
        if not create:
            return
        
        if extracted:
            for category in extracted:
                self.category.add(category)

    class Meta:
        model = Product
