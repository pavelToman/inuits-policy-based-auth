from .policy_loader import load_policies
from flask import Flask, make_response
from flask_restful import Api, Resource, request
from inuits_policy_based_auth import PolicyFactory, RequestContext
from logging import Logger


app = Flask(__name__)
api = Api(app)

policy_factory = PolicyFactory(Logger(""))
load_policies(policy_factory)


class Entity(Resource):
    @policy_factory.apply_policies(RequestContext(request))
    def get(self):
        user_context = policy_factory.get_user_context()
        response_body = {
            "auth_objects": user_context.auth_objects,
            "email": user_context.email,
            "tenant": user_context.tenant,
            "roles": user_context.roles,
            "scopes": user_context.scopes,
        }
        return make_response(response_body, 200)

    @policy_factory.apply_policies(RequestContext(request))
    def post(self):
        user_context = policy_factory.get_user_context()
        response_body = {
            "auth_objects": user_context.auth_objects,
            "email": user_context.email,
            "tenant": user_context.tenant,
            "roles": user_context.roles,
            "scopes": user_context.scopes,
        }
        return make_response(response_body, 201)


api.add_resource(Entity, "/")
