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

    def resolve_pk(self, args, context, info):
        return self.id


class CreateBuilding(graphene.Mutation):
    class Input:
        name = graphene.String(required=True)
        size = graphene.Int(required=True)

    ok = graphene.Boolean()
    building = graphene.Field(BuildingNode)

    @staticmethod
    def mutate(root, args, context, info):
        building = Building.objects.create(name=args.get('name'), size=args.get('size'), owner=context.user)
        ok = True
        return CreateBuilding(building=building, ok=ok)


class ModifyBuilding(graphene.Mutation):
    class Input:
        building_id = graphene.Int(required=True)
        new_name = graphene.String(required=True)
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


class FloorNode(DjangoObjectType):
    pk = graphene.Int()

    class Meta:
        model = Floor
        interfaces = (graphene.Node, )
        filter_fields = ['number']

    def resolve_pk(self, args, context, info):
        return self.id


class RoomNode(DjangoObjectType):
    pk = graphene.Int()

    class Meta:
        model = Room
        interfaces = (graphene.Node, )
        filter_fields = {
            'name': ['icontains']
        }

    def resolve_pk(self, args, context, info):
        return self.id


class Query(graphene.ObjectType):
    buildings = DjangoFilterConnectionField(BuildingNode)
    floors = DjangoFilterConnectionField(FloorNode)
    rooms = DjangoFilterConnectionField(RoomNode)
    building = graphene.Node.Field(BuildingNode)
    floor = graphene.Node.Field(FloorNode)
    room = graphene.Node.Field(RoomNode)

    def resolve_buildings(self, args, context, info):
        return Building.objects.filter(owner=context.user)


class Mutation(graphene.ObjectType):
    create_building = CreateBuilding.Field()
    modify_building = ModifyBuilding.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
