from typing import Union, Type, Tuple

from django.db import models
from django.db.models import ObjectDoesNotExist as doesnt_exist
from django.contrib.postgres.search import TrigramSimilarity, TrigramDistance
from django.db.models import CharField
from django.db.models.functions import Cast
from django.db.models import QuerySet, Func, F

from .utils.manager_utils import SearchResult

# Types
queryset = Union[Type[QuerySet], QuerySet]    # Can be Subtype or Instance of Queryset
django_model = Type[models.Model]     # Subtype of models.Model


class ProductManager(models.Manager):

    # def search_product_names(self, value: str):
    #     results = self.filter(full_name__trigram_similar=value)
    #     return results

    def trigram_similarity_search(
            self, value, sim_value: float = 0.5, field="full_name"
    ) -> SearchResult:
        if sim_value > 1 or sim_value < 0:
            raise ValueError("similarity must be greater > 0 but <= 1")
        res = self.annotate(
            similarity=TrigramSimilarity(field, value),
        ).filter(similarity__gt=sim_value).order_by("-similarity")

        return SearchResult(res, field, "trigram", similarity=sim_value)

    def trigram_distance_search(
            self, value, dist_value: float = 0.7, field="full_name"
    ) -> SearchResult:
        """
        Returns a queryset of values not really similar to query but not totally DISIMILAR.
        """
        if dist_value > 1 or dist_value < 0:
            raise ValueError("distance must be greater > 0 but <= 1")
        res = self.annotate(
            distance=TrigramDistance(field, value),
        ).filter(distance_gt=dist_value).filter(distance_lt=1).order_by("-distance")
        return SearchResult(res, field, "trigram", distance=dist_value)

    def get_obj_or_none(self, value, field="full_name") -> Union[django_model, None]:
        dict_ = {field: value}
        try:
            obj = self.get(**dict_)
        except doesnt_exist:
            return None
        else:
            return obj

    @staticmethod
    def filter_available(query_set: queryset) -> queryset:
        return query_set.filter(available=True)

    def full_search(self, value) -> Union[SearchResult, None]:
        # Search for exact object if user is knowledgeable of item
        res = self.filter_available(self.filter(full_name=value))
        if res:
            return SearchResult(res, "full_name")
        # Search for objects that contain values
        res = self.filter(full_name__icontains=value)
        if res:
            return SearchResult(self.filter_available(res), "full_name", "icontains")
        # Search for similar items
        sim_values = (0.75, 0.5, 0.3)
        for sim_val in sim_values:
            res = self.trigram_similarity_search(value, sim_val)
            if res:
                query_set = self.filter_available(res.results)
                return SearchResult(query_set, res.query_field, "trigram", similarity=sim_val)
        # Suggestions
        res = res.results.exclude(similarity=0)
        if res:
            return SearchResult(self.filter_available(res), "full_name", "trigram", suggestions=True)


class CategoryManagers(models.Manager):
    def trigram_similarity_search(
            self, value, sim_value: float = 0.5, field="name"
    ) -> SearchResult:

        if sim_value > 1 or sim_value < 0:
            raise ValueError("similarity must be greater > 0 but <= 1")
        res = self.annotate(
            similarity=TrigramSimilarity(field, value),
        ).filter(similarity__gt=sim_value).order_by("-similarity")
        return SearchResult(res, field, "trigram", similarity=sim_value)

    def trigram_distance_search(
            self, value, dist_value: float = 0.7, field="name"
    ) -> SearchResult:
        """
        Returns a queryset of values not really similar to query but not totally DISIMILAR.
        """
        if dist_value > 1 or dist_value < 0:
            raise ValueError("distance must be greater > 0 but <= 1")
        res = self.annotate(
            distance=TrigramDistance(field, value),
        ).filter(distance_gt=dist_value).filter(distance_lt=1).order_by("-distance")
        return SearchResult(res, field, "trigram", distance=dist_value)

    def get_obj_or_none(self, value, field="name"):
        dict_ = {field: value}
        try:
            obj = self.get(**dict_)
        except doesnt_exist:
            return None
        else:
            return obj

    def full_search(self, value) -> Union[SearchResult, None]:
        # Search for exact object if user is knowledgeable of item
        res = self.filter(name=value)
        if res:
            return SearchResult(res, "name")
        # Search for objects that contain values
        res = self.filter(name__icontains=value)
        if res:
            return SearchResult(res, "name", "icontains")
        # Search for similar items
        sim_values = (0.75, 0.5, 0.3)
        for sim_val in sim_values:
            res = self.trigram_similarity_search(value, sim_val)
            if res:
                return res
        # Search Alias
        res = self.exclude(alias=[""]) \
            .annotate(unnest=Func(F('alias'), function='unnest')) \
            .annotate(similar=TrigramSimilarity('unnest', value))
        # Manually filter queryset objects
        similar, suggestions = [], []
        if res:
            for obj in res:
                for sim_val in sim_values:
                    if obj.similar >= sim_val:
                        similar.append(obj)
                if 0 < obj.similar < 0.3:
                    suggestions.append(obj)
        # Suggestions
        if similar:
            return SearchResult(similar, "alias", "trigram")
        else:
            return SearchResult(suggestions, "alias", "trigram", suggestions=True) \
                        if suggestions else None

