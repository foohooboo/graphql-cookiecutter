import graphene

from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from graphql_relay.node.node import from_global_id

from .models import Building, Floor, Room


class BuildingNode(DjangoObjectType):
    real_id = graphene.Int()

    class Meta:
        model = Building
        interfaces = (graphene.Node, )
        filter_fields = {
            'name': ['icontains']
        }

    def resolve_real_id(self, args, context, info):
        return self.id


class FloorNode(DjangoObjectType):
    real_id = graphene.Int()

    class Meta:
        model = Floor
        interfaces = (graphene.Node, )
        filter_fields = ['number']

    def resolve_real_id(self, args, context, info):
        return self.id


class RoomNode(DjangoObjectType):
    real_id = graphene.Int()

    class Meta:
        model = Room
        interfaces = (graphene.Node, )
        filter_fields = {
            'name': ['icontains']
        }

    def resolve_real_id(self, args, context, info):
        return self.id


class BuildingQuery(graphene.AbstractType):
    buildings = DjangoFilterConnectionField(BuildingNode)
    # buildings = graphene.List(BuildingNode, name=graphene.String())
    floors = DjangoFilterConnectionField(FloorNode)
    # floors = graphene.List(FloorNode)
    rooms = DjangoFilterConnectionField(RoomNode)
    # rooms = graphene.List(RoomNode)
    building = graphene.Field(BuildingNode, id=graphene.Int())
    floor = graphene.Field(FloorNode, id=graphene.Int())
    room = graphene.Field(RoomNode, id=graphene.Int())

    # def resolve_buildings(self, args, context, info):
    #     if args.get('name'):
    #         return Building.objects.filter(name__icontains=args.get('name'))
    #     return Building.objects.all()

    def resolve_floors(self, args, context, info):
        return Floor.objects.select_related('building').all()

    def resolve_rooms(self, args, context, info):
        return Room.objects.select_related('floor').all()

    def resolve_building(self, args, context, info):
        id = args.get('id')
        if id is not None:
            return Building.objects.get(pk=id)
        return None

    def resolve_floor(self, args, context, info):
        id = args.get('id')
        if id is not None:
            return Floor.objects.get(pk=id)
        return None

class Query(BuildingQuery, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass

schema = graphene.Schema(query=Query)
