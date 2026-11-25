
from django.urls import reverse


class AccessTestMixin:
    """
    Access test mixin.
    Test anonymous and authenticated user accessibility.
    """
    
    url_name = None
    valid_data = {}
    
    def get_url_kwargs(self):
        return {}
    
    def get_url(self):
        return reverse(
            self.url_name,
            kwargs=self.get_url_kwargs()
        )
    
    def test_anonymous_get_(self):
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
            data=self.valid_data
        )
        
        self.assertEqual(response.status_code, 302)

    
    def test_authenticated_get(self):
        """
        Test regular user can access with GET method
        """
        self.client.force_login(self.user)
        
        response = self.client.get(
            self.get_url()
        )
        
        self.assertNotEqual(response.status_code, 403)

    def test_authenticated_post(self):
        """
        Test regular user can access with POST method
        """
        self.client.force_login(self.user)
        
        response = self.client.post(
            self.get_url(),
            data=self.valid_data
        )
        
        self.assertNotEqual(response.status_code, 403)
