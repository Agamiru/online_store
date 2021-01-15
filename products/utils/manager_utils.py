from typing import Union, Type, List
from django.db import models
from django.db.models import QuerySet


# Types
queryset = Type[Union[Type[QuerySet], QuerySet]]    # Can be Subtype or Instance of Queryset
django_model = Type[models.Model]     # Subtype of models.Model


class SearchResult:
    """
    A class to store information about the details of a search operation.
    All manger functions with name '**_search' return this result.
    """
    def __init__(self, results, query_field: str, query_type="get", **kwargs):
        self.results: Union[queryset, List[django_model]] = results
        self.query_field = query_field
        self.query_type = query_type
        if kwargs:
            self.kwargs = kwargs
            for k, v in kwargs.items():
                setattr(self, k, v)
        else:
            self.kwargs = None

    def __bool__(self):
        return True if self.results else False

    def __eq__(self, other):
        return True if self.results == other.query_set else False

    def __repr__(self):
        return "<{cls}: query_set: {q_set} <query_type: {q_type}> <query_field: {q_field}>>" \
                .format(
                        cls=self.__class__.__name__, q_set=self.results, q_type=self.query_type,
                        q_field=self.query_field
                )

    def __str__(self):
        return self.__repr__()
