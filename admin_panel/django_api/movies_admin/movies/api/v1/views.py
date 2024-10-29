import enum
from django.contrib.postgres.aggregates import ArrayAgg
from django.http import JsonResponse
from django.views.generic.list import BaseListView
from django.views.generic.detail import BaseDetailView
from django.db.models import Q
from movies.models import FilmWork, Review, Comment
from movies.serializers import ReviewSerializer, CommentSerializer
from profiles.models import Profile

from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import PermissionDenied
from http import HTTPStatus


class Role(enum.Enum):
    actor = 'actor'
    director = 'director'
    writer = 'writer'


class MoviesApiMixin:
    model = FilmWork
    http_method_names = ['get']

    def get_queryset(self):
        return FilmWork.objects.values(
            'id',
            'title',
            'description',
            'creation_date',
            'rating',
            'type').annotate(
                genres=ArrayAgg(
                    'genres__name',
                    distinct=True,
                    default=[]
                ),
                actors=ArrayAgg(
                    'persons__full_name',
                    distinct=True,
                    filter=Q(personfilmwork__role=Role.actor.value),
                    default=[]
                ),
                directors=ArrayAgg(
                    'persons__full_name',
                    distinct=True,
                    filter=Q(personfilmwork__role=Role.director.value),
                    default=[]
                ),
                writers=ArrayAgg(
                    'persons__full_name',
                    distinct=True,
                    filter=Q(personfilmwork__role=Role.actor.value),
                    default=[]
                )
            )

    def render_to_response(self, context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset,
            self.paginate_by
        )

        return {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': page.previous_page_number() if page.has_previous() else None,
            'next': page.next_page_number() if page.has_next() else None,
            'results': list(queryset)
        }


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):
    context_object_name = 'movie'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context['movie']


class ReviewListCreateView(ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination

    def create(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            raise PermissionDenied("Anonymous users can't add reviews")
        data = dict(request.data)
        data['film_work'] = self.kwargs['pk']
        data["author"] = Profile.objects.get(user_id=request.user.id).id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        film_work = FilmWork.objects.get(id=self.kwargs['pk'])
        film_work.rating = film_work.get_average_rating();
        film_work.save()
        return Response(serializer.data, status=HTTPStatus.CREATED)

    def get_queryset(self):
        return Review.objects.filter(film_work_id=self.kwargs['pk'])


class ReviewDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def perform_update(self, serializer):
        review = Review.objects.get(id=self.kwargs['pk'])
        if review.author != Profile.objects.get(user_id=self.request.user.id):
            raise PermissionDenied("You can't edit this review")
        film_work = review.film_work
        serializer.save()
        film_work.rating = film_work.get_average_rating()
        film_work.save()

    def perform_destroy(self, instance):
        review = Review.objects.get(id=self.kwargs['pk'])
        if review.author != Profile.objects.get(user_id=self.request.user.id):
            raise PermissionDenied("You can't edit this review")
        film_work = review.film_work
        instance.delete()
        film_work.rating = film_work.get_average_rating();
        film_work.save()


class CommentListCreateView(ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination

    def create(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            raise PermissionDenied("Anonymous users can't add comments")
        data = dict(request.data)
        data['review'] = self.kwargs['pk']
        data["author"] = Profile.objects.get(user_id=request.user.id).id
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=HTTPStatus.CREATED)

    def get_queryset(self):
        return Comment.objects.filter(review_id=self.kwargs['pk'])


class CommentDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def perform_update(self, serializer):
        comment = Comment.objects.get(id=self.kwargs['pk'])
        if comment.author != Profile.objects.get(user_id=self.request.user.id):
            raise PermissionDenied("You can't edit this comment")
        serializer.save()

    def perform_destroy(self, instance):
        comment = Comment.objects.get(id=self.kwargs['pk'])
        if comment.author != Profile.objects.get(user_id=self.request.user.id):
            raise PermissionDenied("You can't edit this comment")
        instance.delete()
