import json
from django.views.generic import View
from django.http import HttpResponse
from updates.models import Update as UpdateModel

from config.mixins import HttpResponseMixin

from .forms import UpdateModelForm
from updates.models import Update as UpdateModel

from .mixins import CSRFExemptMixin


class UpdateModelDetailAPIView(HttpResponseMixin,
                                CSRFExemptMixin,
                                View):
    is_json = True

    def get_object(selfself, id=None):
        qs = UpdateModel.objects.filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def get(self, reqeust,id, *args, **kwargs):
        obj = UpdateModel.objects.get(id=id)
        json_data = obj.serialize()
        return self.render_to_response(json_data)

    def post(self, request, *args, **kwargs):
        json_data = json.dumps(
            {
                "message": "Not allowed, please use the /api/updates/endpoint"
            }
        )
        return self.render_to_response(json_data, status=403)

    def put(self, request, *args, **kwargs):
        json_data = {}
        return self.render_to_response(json_data)

    def delete(self, request, *args, **kwargs):
        json_data= {}
        return self.render_to_response(
            json_data,
            status=403
        )


class UpdateModelListAPIView(HttpResponseMixin,
                             CSRFExemptMixin,
                             View):
    '''
    List View
    Create View
    '''
    def get(self, request, *args, **kwargs):
        qs = UpdateModel.objects.all()
        json_data = qs.serialize()
        return self.render_to_response(json_data)

    def post(self, request, *args, **kwargs):
        form = UpdateModelForm(request.POST)
        print(form)
        if form.is_valid():
            obj = form.save(commit=True)
            obj_data = obj.serialize()
            return self.render_to_response(obj_data, status=201)
        if form.errors:
            data = json.dumps(form.errors)
            print("kwon")
            return self.render_to_response(data, status=400)
        data = {"message": "Not Allowed"}
        return self.render_to_response(data, status=400)

    def delete (self, request, *args, **kwargs):
        data = json.dumps({"message": "You cannot delete an entire list."})
        return self.render_to_response(data, status=403)