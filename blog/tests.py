from django.test import TestCase, Client
from .models import Post
from django.contrib.auth.models import User
from django_project.utility import TestDataGenerator
from django.http import HttpResponse
from django.http.response import (
    HttpResponseBase,
    HttpResponseRedirect,
    HttpResponseNotFound,
)

from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver
import os


class PostTestCase(TestCase, TestDataGenerator):
    def setUp(self):
        super().create_sample_data()

    def test_posts_have_title(self):
        post_one = Post.objects.get(title=self.TEST_TITLE_ONE)
        post_two = Post.objects.get(title=self.TEST_TITLE_TWO)
        self.assertEqual(post_one.title, self.TEST_TITLE_ONE)
        self.assertEqual(post_two.title, self.TEST_TITLE_TWO)

    def test_posts_have_content(self):
        post_one = Post.objects.get(title=self.TEST_TITLE_ONE)
        post_two = Post.objects.get(title=self.TEST_TITLE_TWO)
        self.assertEqual(post_one.content, self.TEST_CONTENT_ONE)
        self.assertEqual(post_two.content, self.TEST_CONTENT_TWO)

    def test_posts_has_author(self):
        user_one = User.objects.get(username=self.TEST_USERNAME_ONE)
        user_two = User.objects.get(username=self.TEST_USERNAME_TWO)
        post_one = Post.objects.get(author=user_one)
        post_two = Post.objects.get(author=user_two)
        self.assertEqual(post_one.author, user_one)
        self.assertEqual(post_two.author, user_two)

    def test_get_single_post(self):
        c = Client()
        user = User.objects.filter(username=self.TEST_USERNAME_ONE).first()
        post = Post.objects.filter(author=user).first()
        response = c.get(f"/post/{post.id}/")
        self.assertEquals(response.status_code, HttpResponseBase.status_code)

    def test_get_nonexistant_post(self):
        c = Client()
        response = c.get(f"/post/0/")
        self.assertEquals(response.status_code, HttpResponseNotFound.status_code)

    def test_create_post_logged_in(self):
        c = Client()
        c.login(username=self.TEST_USERNAME_ONE, password=self.TEST_PASSWORD)
        post_count = Post.objects.count()
        self.assertEquals(self.TEST_EXPECTED_SIZE_TWO, post_count)
        c.post(
            "/post/new/", {"title": "Test Title", "content": "Test Content"},
        )
        new_post_count = Post.objects.count()
        self.assertNotEquals(post_count, new_post_count)
        self.assertEquals(self.TEST_EXPECTED_SIZE_THREE, new_post_count)

    def test_create_post_not_logged_in(self):
        c = Client()
        post_count = Post.objects.count()
        self.assertEquals(self.TEST_EXPECTED_SIZE_TWO, post_count)
        c.post(
            "/post/new/", {"title": "Test Title", "content": "Test Content"},
        )
        new_post_count = Post.objects.count()
        self.assertEquals(self.TEST_EXPECTED_SIZE_TWO, new_post_count)

    def test_delete_post_logged_in(self):
        c = Client()
        c.login(username=self.TEST_USERNAME_ONE, password=self.TEST_PASSWORD)
        user = User.objects.filter(username=self.TEST_USERNAME_ONE).first()
        post_count = Post.objects.count()
        self.assertEquals(self.TEST_EXPECTED_SIZE_TWO, post_count)
        post = Post.objects.filter(author=user).first()
        c.delete(f"/post/{post.id}/delete/")
        new_post_count = Post.objects.count()
        self.assertNotEquals(post_count, new_post_count)
        self.assertEquals(self.TEST_EXPECTED_SIZE_ONE, new_post_count)

    def test_delete_post_not_logged_in(self):
        c = Client()
        user = User.objects.filter(username=self.TEST_USERNAME_ONE).first()
        post_count = Post.objects.count()
        self.assertEquals(self.TEST_EXPECTED_SIZE_TWO, post_count)
        post = Post.objects.filter(author=user).first()
        c.delete(f"/post/{post.id}/delete/")
        new_post_count = Post.objects.count()
        self.assertEquals(self.TEST_EXPECTED_SIZE_TWO, new_post_count)

    def test_update_post_logged_in(self):
        c = Client()
        c.login(username=self.TEST_USERNAME_ONE, password=self.TEST_PASSWORD)
        user = User.objects.filter(username=self.TEST_USERNAME_ONE).first()
        post = Post.objects.filter(author=user).first()
        new_title = f"{post.title}123"
        content = {"title": new_title, "content": post.content}
        c.post(f"/post/{post.id}/update/", content)
        updated_post = Post.objects.filter(id=post.id).first()
        self.assertEquals(new_title, updated_post.title)

    def test_update_post_not_logged_in(self):
        c = Client()
        user = User.objects.filter(username=self.TEST_USERNAME_ONE).first()
        post = Post.objects.filter(author=user).first()
        new_title = f"{post.title}123"
        content = {"title": new_title, "content": post.content}
        c.post(f"/post/{post.id}/update/", content)
        updated_post = Post.objects.filter(id=post.id).first()
        self.assertNotEquals(new_title, updated_post.title)


class UserViewTestCase(TestCase, TestDataGenerator):
    def setUp(self):
        super().create_sample_data()

    def test_view_profile_as_logged_in(self):
        c = Client()
        c.login(username=self.TEST_USERNAME_ONE, password=self.TEST_PASSWORD)
        response = c.get("/profile/")
        self.assertEqual(HttpResponseBase.status_code, response.status_code)

    def test_view_profile_as_not_logged_in(self):
        c = Client()
        response = c.get("/profile/")
        self.assertEqual(HttpResponseRedirect.status_code, response.status_code)


# TODO: will need to rename this once I write a few tests using it.
class MySeleniumTests(StaticLiveServerTestCase, TestDataGenerator):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def setUp(self):
        super().create_sample_data()

    def tearDown(self):
        super().delete_sample_data()

    def login_helper(self):
        self.selenium.get("%s%s" % (self.live_server_url, "/login/"))
        username_input = self.selenium.find_element_by_name("username")
        username_input.send_keys(self.TEST_USERNAME_ONE)
        password_input = self.selenium.find_element_by_name("password")
        password_input.send_keys(self.TEST_PASSWORD)
        self.selenium.find_element_by_xpath(
            "/html/body/main/div/div[1]/div/form/div/button"
        ).click()

    def test_navbar_content(self):
        self.login_helper()
        profile_link = self.selenium.find_element_by_xpath(
            '//*[@id="navbarToggle"]/div[2]/a[2]'
        )
        self.assertEqual(profile_link.text, "Profile")
        new_post_link = self.selenium.find_element_by_xpath(
            "/html/body/header/nav/div/div/div[2]/a[1]"
        )
        self.assertEqual(new_post_link.text, "New Post")
        log_out_link = self.selenium.find_element_by_xpath(
            "/html/body/header/nav/div/div/div[2]/a[3]"
        )
        self.assertEqual(log_out_link.text, "Logout")

    def test_create_post(self):
        self.login_helper()
        self.selenium.find_element_by_xpath('//*[@id="navbarToggle"]/div[2]/a[1]').click()
        title = f"{self.TEST_TITLE_ONE} Two"
        content = f"{self.TEST_CONTENT_ONE} Two"
        title_input = self.selenium.find_element_by_name("title")
        title_input.send_keys(title)
        content_input = self.selenium.find_element_by_name("content")
        content_input.send_keys(content)

    def test_delete_post(self):
        self.login_helper()
        self.selenium.find_element_by_link_text(self.TEST_TITLE_ONE).click()
        self.selenium.find_element_by_link_text('Delete').click()
        self.selenium.find_element_by_xpath('/html/body/main/div/div[1]/div/form/div/button').click()

    def test_update_post(self):
        self.login_helper()
        self.selenium.find_element_by_link_text(self.TEST_TITLE_ONE).click()
        self.selenium.find_element_by_link_text('Update').click()
        title_input = self.selenium.find_element_by_name('title')
        title_input.send_keys(" New Update")
        self.selenium.find_element_by_xpath('/html/body/main/div/div[1]/div/form/div/button').click()

    def test_update_profile_picture(self):
        self.login_helper()
        self.selenium.find_element_by_xpath('//*[@id="navbarToggle"]/div[2]/a[2]').click()
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        image_path = f"{base_dir}/media/profile_pics/large.jpg"
        upload_field = self.selenium.find_element_by_id("id_image")
        upload_field.send_keys(image_path)
        self.selenium.find_element_by_xpath('/html/body/main/div/div[1]/div/form/div/button').click()