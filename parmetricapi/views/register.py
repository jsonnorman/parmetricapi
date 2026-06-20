"""Register and login users"""

import json
from django.http import HttpResponse, HttpResponseNotAllowed
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.authtoken.models import Token


@csrf_exempt
def login_user(request):
    """Handles the authentication of a user"""

    if request.method == "POST":
        body = request.body.decode("utf-8")
        req_body = json.loads(body)

        username = req_body["username"]
        password = req_body["password"]

        authenticated_user = authenticate(username=username, password=password)

        if authenticated_user is not None:
            token = Token.objects.get(user=authenticated_user)

            data = json.dumps(
                {"valid": True, "token": token.key, "id": authenticated_user.id}
            )

            return HttpResponse(data, content_type="application/json")

        data = json.dumps({"valid": False})
        return HttpResponse(data, content_type="application/json")

    return HttpResponseNotAllowed(permitted_methods=["POST"])


@csrf_exempt
def register_user(request):
    """Handles the creation of a new user for authentication"""

    if request.method == "POST":
        req_body = json.loads(request.body.decode("utf-8"))

        new_user = User.objects.create_user(
            username=req_body["username"],
            email=req_body["email"],
            password=req_body["password"],
            first_name=req_body["first_name"],
            last_name=req_body["last_name"],
        )

        token = Token.objects.create(user=new_user)

        data = json.dumps({"token": token.key, "id": new_user.id})

        return HttpResponse(
            data, content_type="application/json", status=status.HTTP_201_CREATED
        )

    return HttpResponseNotAllowed(permitted_methods=["POST"])
