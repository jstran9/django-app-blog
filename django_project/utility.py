from blog.models import Post
from django.contrib.auth.models import User
from django.contrib.staticfiles.testing import StaticLiveServerTestCase


class TestDataGenerator:
    TEST_TITLE_ONE = "Test Post By Greg"
    TEST_TITLE_TWO = "Test Post By Snickers"
    TEST_CONTENT_ONE = "This is a post by Greg!"
    TEST_CONTENT_TWO = "This is a post by Snickerdoodle!"
    TEST_USERNAME_ONE = "greg"
    TEST_USERNAME_TWO = "snickers"
    TEST_USERNAME_THREE = "roxy"
    TEST_PASSWORD = "password321"
    TEST_EMAIL_ONE = "toddtran10@gmail.com"
    TEST_EMAIL_TWO = "wptran58@gmail.com"
    TEST_EMAIL_THREE = "toddtran9@gmail.com"
    TEST_EXPECTED_SIZE_ONE = 1
    TEST_EXPECTED_SIZE_TWO = 2
    TEST_EXPECTED_SIZE_THREE = 3

    def create_sample_data(self):
        user_one = User.objects.create_user(
            username=self.TEST_USERNAME_ONE,
            password=self.TEST_PASSWORD,
            first_name="greg",
            last_name="tran-ling",
            email=self.TEST_EMAIL_ONE,
        )
        user_two = User.objects.create_user(
            username=self.TEST_USERNAME_TWO,
            password=self.TEST_PASSWORD,
            first_name="snickerdoodle",
            last_name="tran-ling",
            email=self.TEST_EMAIL_TWO,
        )
        Post.objects.create(
            title=self.TEST_TITLE_ONE, content=self.TEST_CONTENT_ONE, author=user_one
        )
        Post.objects.create(
            title=self.TEST_TITLE_TWO, content=self.TEST_CONTENT_TWO, author=user_two
        )

    def delete_sample_data(self):
        user_one = User.objects.get(username=self.TEST_USERNAME_ONE)
        user_one.delete()
        user_two = User.objects.get(username=self.TEST_USERNAME_TWO)
        user_two.delete()

    def get_number_of_posts(self):
        return Post.objects.count()