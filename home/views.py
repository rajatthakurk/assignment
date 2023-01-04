from rest_framework.views import APIView
from .serializers import BlogSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Blog

class BlogView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self ,request):     #get 
        try:
            blogs = Blog.objects.filter(user=request.user)
            serializer = BlogSerializer(blogs , many =True)
            return Response({
                'data' : serializer.data,
                'message' : 'blog data get'
            },status = status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            return Response({
                'data' : {},
                'message' : 'something went wrong',
            },status = status.HTTP_400_BAD_REQUEST)

    def post(self,request):   # post
        try:
            data = request.data
            print(request.user)
            data['user'] = request.user.id
            serializer = BlogSerializer(data = data)
            if not serializer.is_valid():
                return Response({
                    'data' : serializer.errors,
                    'message' : 'something went wrong',
                },status = status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response({
                'data' : serializer.data,
                'message' : 'Your blog is Created'
            },status = status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            return Response({
                'data' : {},
                'message' : 'something went wrong',
            },status = status.HTTP_400_BAD_REQUEST)


    def patch(self, request):   #update
        try:
            data = request.data
            blog = Blog.objects.filter(uid = data.get('uid'))
            if not blog.exists():
                return Response({
                    'data':{},
                    'message':'invalid blog uid'
                },status = status.HTTP_400_BAD_REQUEST)
            if request.user != blog[0].user:
                return Response({
                    'data':{},
                    'message':'you are not authorized'
                },status = status.HTTP_400_BAD_REQUEST)
            serializer = BlogSerializer(blog[0],data = data,partial = True)

            if not serializer.is_valid():
                return Response({
                    'data' : serializer.errors,
                    'message' : 'something went wrong',
                },status = status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response({
                'data' : serializer.data,
                'message' : 'Your blog is updated'
            },status = status.HTTP_201_CREATED)

        except Exception as e:
            return Response({
                'data' : {},
                'message' : 'something went wrong',
            },status = status.HTTP_400_BAD_REQUEST)
            
    def delete(self, request):   # delete
        try:
            data = request.data
            blog = Blog.objects.filter(uid = data.get('uid'))
            if not blog.exists():
                return Response({
                    'data':{},
                    'message':'invalid blog uid'
                },status = status.HTTP_400_BAD_REQUEST)
            if request.user != blog[0].user:
                return Response({
                    'data':{},
                    'message':'you are not authorized'
                },status = status.HTTP_400_BAD_REQUEST)

            blog[0].delete()
            return Response({
                'data' : {},
                'message' : 'Your blog is deleted'
            },status = status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                'data' : {},
                'message' : 'something went wrong',
            },status = status.HTTP_400_BAD_REQUEST)
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]

    # def post(self , request):
    #     try:
    #         data = request.data
 #           print("#########")
 #           print(request.user)
 #           print("#########")

        #     data['user'] = request.user.id
        #     serializer = BlogSerializer(data = data)
            
        #     if not serializer.is_valid():
        #         return Response({
        #             'data' : serializer.errors,
        #             'message' : 'something went wrong',
        #         },status = status.HTTP_400_BAD_REQUEST)
                
        #     serializer.save()

        #     return Response({
        #             'data' : serializer.data,
        #             'message' : 'Your blog is Created'
        #         },status = status.HTTP_201_CREATED)

        # except Exception as e:
        #     print(e)
        #     return Response({
        #         'data' : {},
        #         'message' : 'something went wrong',
        #     },status = status.HTTP_400_BAD_REQUEST)
