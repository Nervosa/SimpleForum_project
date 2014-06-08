from rest_framework.authentication import BasicAuthentication

class BasicForumAuthentication(BasicAuthentication):

    def authenticate_header(self, request):
        return 'xBasic realm="%s"' % self.www_authenticate_realm