class UserInfoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.user_info = {
            'user': request.user,
        }
        response = self.get_response(request)
        return response
