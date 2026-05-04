from rest_framework.views import APIView
from rest_framework.response import Response

from access.permissions import HasRBACPermission


class ReportsView(APIView):
    permission_classes = [HasRBACPermission]
    resource = "reports"

    def get(self, request):
        self.action_name = "read"
        return Response([
            {"id": 1, "title": "Sales report"},
            {"id": 2, "title": "Users report"},
        ])

    def post(self, request):
        self.action_name = "create"
        return Response({"detail": "Report created"})


class OrdersView(APIView):
    permission_classes = [HasRBACPermission]
    resource = "orders"
    action_name = "read"

    def get(self, request):
        return Response([
            {"id": 1, "name": "Order #1"},
            {"id": 2, "name": "Order #2"},
        ])
        
        
class ReportsListView(APIView):
    permission_classes = [HasRBACPermission]
    resource = "reports"
    action_name = "read"

    def get(self, request):
        return Response([
            {"id": 1, "title": "Sales report"},
            {"id": 2, "title": "Users report"},
        ])


class ReportsCreateView(APIView):
    permission_classes = [HasRBACPermission]
    resource = "reports"
    action_name = "create"

    def post(self, request):
        return Response({"detail": "Report created"})