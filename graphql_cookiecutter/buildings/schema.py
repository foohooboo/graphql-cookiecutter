import graphene

from graphene_django.filter import DjangoFilterConnectionField
from graphene_django.types import DjangoObjectType
from graphql_relay.node.node import from_global_id

from .models import Building, Floor, Room


class BuildingNode(DjangoObjectType):
    pk = graphene.Int()

    class Meta:
        model = Building
        interfaces = (graphene.Node, )
        filter_fields = {
            'name': ['icontains'],
            'size': ['gte', 'lte']
        }

    def resolve_real_id(self, args, context, info):
        return self.id


class FloorNode(DjangoObjectType):
    pk = graphene.Int()

    class Meta:
        model = Floor
        interfaces = (graphene.Node, )
        filter_fields = ['number']

    def resolve_real_id(self, args, context, info):
        return self.id


class RoomNode(DjangoObjectType):
    pk = graphene.Int()

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
    floors = DjangoFilterConnectionField(FloorNode)
    rooms = DjangoFilterConnectionField(RoomNode)
    building = graphene.Field(BuildingNode, id=graphene.Int())
    floor = graphene.Field(FloorNode, id=graphene.Int())
    room = graphene.Field(RoomNode, id=graphene.Int())

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


class ModifyBuilding(graphene.Mutation):
    class Input:
        building_id = graphene.Int()
        new_name = graphene.String()
        #size = graphene.Int()

    ok = graphene.Boolean()
    building = graphene.Field(BuildingNode)

    @staticmethod
    def mutate(root, args, context, info):
        building_to_modify = Building.objects.get(pk=args.get('building_id'))
        building_to_modify.name = args.get('new_name')
        #building_to_modify.size = args.get('size')
        ok = True
        return ModifyBuilding(building=building_to_modify, ok=ok)


class Query(BuildingQuery, graphene.ObjectType):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass

class Mutations(graphene.ObjectType):
    modify_building = ModifyBuilding.Field()


schema = graphene.Schema(query=Query, mutation=Mutations)
