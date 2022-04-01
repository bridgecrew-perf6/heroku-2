from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets


from users.models import User
from users.api.serializers import UserSerializer,UserListSerializer,updateUserSerializer,PasswordSerializer

#Test Git

class UserViewSet(viewsets.GenericViewSet):
    model = User
    serializer_class = UserSerializer
    list_serializer_class = UserListSerializer
    queryset = None

    def get_object(self,pk):
        return get_object_or_404(self.model,pk= pk)
    
    def get_queryset(self):
      if self.queryset is None:
          self.queryset = self.model.objects\
            .filter(is_active = True)\
            .values('id','username','email','name','last_name','phone','password')
      return self.queryset

    def list(self,request):
      users = self.get_queryset()
      users_serializer = self.list_serializer_class(users, many= True)
      return Response(users_serializer.data,status= status.HTTP_200_OK)
    
    def create(self,request):
      user_serializer = self.serializer_class(data= request.data)
      if user_serializer.is_valid():
          user_serializer.save()
          return Response({'message':'Usuario registrado correctamente.'},status=status.HTTP_201_CREATED)
      return Response({'message':'Hay errores en el registro','errors':user_serializer.errors},status= status.HTTP_400_BAD_REQUEST)

    
    def retrieve(self, request, pk=None):
      user = self.get_object(pk)
      user_serializer = self.serializer_class(user)
      return Response(user_serializer.data)
    
    def update(self,request,pk=None):
      user = self.get_object(pk)
      user_serializer = updateUserSerializer(user,data=request.data)
      if user_serializer.is_valid():
         user_serializer.save()
         return Response({'message': 'Registro actualizado'},status= status.HTTP_200_OK)
      return Response({'message': 'Hay errores favor verificar'},status= status.HTTP_400_BAD_REQUEST)
   
    def destroy(self, request,pk=None):
      user_destroy = self.model.objects.filter(id=pk).update(is_active = False)
      if user_destroy == 1:
          return Response({'messagge':'Usuario eliminado'})
      return Response({'message':'No existe el usuario'},status= status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def set_password(self,request,pk=None):
        user = self.get_object(pk)
        password_serializer = PasswordSerializer(data=request.data)
        
        if password_serializer.is_valid():
          user.set_password(password_serializer.validated_data['password'])
          user.save()
          return Response({'message': 'Contraseña actualizada correctamente'},status= status.HTTP_200_OK)
        
        return Response({'message': 'Hay errores en la informacion enviada','errors': password_serializer.errors},status=status.HTTP_400_BAD_REQUEST) 
    
    
    @action(detail=False,methods=['POST'])
    def test_ws(self,request):
  
      return Response({"message": "Probando WS", "Name": request.data['name'],"last_name": request.data['lastname']})


