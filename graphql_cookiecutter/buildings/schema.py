import graphene

from graphene_django.types import DjangoObjectType

from .models import Building, Floor, Room


class BuildingType(DjangoObjectType):
    class Meta:
        model = Building


class FloorType(DjangoObjectType):
    class Meta:
        model = Floor


class RoomType(DjangoObjectType):
    class Meta:
        model = Room


class BuildingQuery(graphene.AbstractType):
    buildings = graphene.List(BuildingType, name=graphene.String())
    floors = graphene.List(FloorType)
    rooms = graphene.List(RoomType)
    building = graphene.Field(BuildingType, id=graphene.Int())
    floor = graphene.Field(FloorType, id=graphene.Int())
    room = graphene.Field(RoomType, id=graphene.Int())

    def resolve_buildings(self, args, context, info):
        if args.get('name'):
            return Building.objects.filter(name__icontains=args.get('name'))
        return Building.objects.all()

    def resolve_building(self, args, context, info):
        id = args.get('id')
        if id is not None:
            return Building.objects.get(pk=id)
        return None

    def resolve_floors(self, args, context, info):
        return Floor.objects.select_related('building').all()

    def resolve_floor(self, args, context, info):
        id = args.get('id')
        if id is not None:
            return Floor.objects.get(pk=id)
        return None

    def resolve_rooms(self, args, context, info):
        return Room.objects.select_related('floor').all()


class Query(BuildingQuery, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass

schema = graphene.Schema(query=Query)
