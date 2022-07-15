from rest_framework import generics,status

# Create your views here.
class OrderListView(generics.ListCreateAPIView):
    pass
    # queryset = Note.objects.all().order_by('-updated')
    # serializer_class = NoteSerializer