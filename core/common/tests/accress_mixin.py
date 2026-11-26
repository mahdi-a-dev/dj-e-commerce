
from django.urls import reverse


class BaseAccessTestMixin:
    url_name = None
    valid_data = {}
    
    def get_url_kwargs(self):
        return {}
    
    def get_url(self):
        return reverse(
            self.url_name,
            kwargs=self.get_url_kwargs()
        )

class AnonymousUserAccessMixin(BaseAccessTestMixin):
    """
    Test anonymous user accessibility.
    """
    def test_anonymous_get(self):
        """
        Test anonymous user get redirect to login with GET method
        """
        response = self.client.get(
            self.get_url()
        )
        
        self.assertEqual(response.status_code, 302)


    def test_anonymous_post(self):
        """
        Test anonymous user get redirect to login with POST method
        """
        
        response = self.client.post(
            self.get_url(),
            data=self.valid_data.copy()
        )
        
        self.assertEqual(response.status_code, 302)
    

class AuthenticatedUserAccessMixin(BaseAccessTestMixin):
    """
    Test athenticated user accessibility.
    """
    expected_get_status = 200
    expected_post_status = 302
    
    def test_authenticated_get(self):
        """
        Test regular user can access with GET method
        """
        self.client.force_login(self.user)
        
        response = self.client.get(
            self.get_url()
        )
        
        self.assertEqual(
            response.status_code,
            self.expected_get_status
        )

    def test_authenticated_post(self):
        """
        Test regular user can access with POST method
        """
        self.client.force_login(self.user)
        
        response = self.client.post(
            self.get_url(),
            data=self.valid_data.copy()
        )
        
        self.assertEqual(
            response.status_code,
            self.expected_post_status
        )