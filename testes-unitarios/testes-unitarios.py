import os
import unittest
import datetime
import shutil
import tempfile

from itertools import islice
from unittest.mock import patch
from unittest import mock
from datetime import datetime, timezone
from instaloader import instaloader
from instaloader.structures import Post
from instaloader import instaloadercontext
from instaloader.exceptions import InvalidArgumentException
from instaloader.instaloadercontext import InstaloaderContext
from instaloader.instaloader import Instaloader
from instaloader.structures import Post, Profile

USUARIO_TESTE = 'kaell_andrade'
WINDOS = 'Windows'
UNIX = 'Unix'
PAGING_MAX_COUNT = 10

ratecontroller = None


"""
Para executar esse teste, faz-se necessario estar no diretorio instaloader-tests e executar o comando:

python3 -m testes-unitarios.testes-unitarios

para a cobertura 

python -m coverage run -m unittest testes-unitarios/testes-unitarios.py

obter html 

python -m coverage html


linha de comando

python -m coverage report --omit="testes-unitarios/*”
"""



class MockTestsPost:
    def __init__(self) -> None:
        self.instaLoader = Instaloader()
        self.user = 'ufsoficial'
        self.timestamp = 1687140049
        

    def __initializeInstaloader(self) -> None:
        # self.instaLoader.login(self.user, '')
        post = Post.from_shortcode(self.instaLoader.context, 'Cs894TXOetY')
        profile = Profile.from_username(self.instaLoader.context, self.user )

        post2 = Post(self.instaLoader.context, self.mockpost)
        # print(profile, post2)
        # print('aqui', post.shortcode)
        # print('title', post2.title)
        print('post')
        print( post2.title)
    
    def util_datetime(self):
        return datetime.datetime.fromtimestamp(self.timestamp)
    
    @property
    def mockpost(self):
        return  {   
                'owner': 'gabriel', 
                'shortcode': 'shortcode123', #Cs894TXOetY
                'code': 'shortcode123',
                'id': '1234', 
                'title': 'post da ufs', 
                'date': self.timestamp, 
                'taken_at_timestamp': self.timestamp
                }
    





class TestesUnitarios(unittest.TestCase):

    data_tests = MockTestsPost()
    mockpost = data_tests.mockpost
    timestamp = data_tests.timestamp
    # context = data_tests.instaLoader.context

    context = mock.Mock(spec=Instaloader)

    @patch('platform.system')
    def test_windows_localappdata_get_config_dir(self, mock_system):
        mock_system.return_value = WINDOS
        os.environ["LOCALAPPDATA"] = "C:\\Users\\{}\\AppData\\Local".format(USUARIO_TESTE)
        expected_dir = os.path.normpath("C:\\Users\\{}\\AppData\\Local/Instaloader".format(USUARIO_TESTE))
        self.assertEqual(instaloader._get_config_dir(), expected_dir)
    
    @patch('platform.system')
    def test_unix_get_config_dir(self, mock_system):
        mock_system.return_value = UNIX
        os.environ["XDG_CONFIG_HOME"] = "/home/{}/.config".format(USUARIO_TESTE)
        expected_dir = "/home/{}/.config/instaloader".format(USUARIO_TESTE)
        self.assertEqual(instaloader._get_config_dir(), expected_dir)
    
    @patch('platform.system')
    def test_windows_get_default_session_filename(self, mock_system):
        mock_system.return_value = WINDOS
        os.environ["LOCALAPPDATA"] = "C:\\Users\\testuser\\AppData\\Local"
        expected_filename = "C:\\Users\\testuser\\AppData\\Local/Instaloader/session-{}".format(USUARIO_TESTE)
        self.assertEqual(instaloader.get_default_session_filename(USUARIO_TESTE), expected_filename)

    @patch('platform.system')
    def test_unix_get_default_session_filename(self, mock_system):
        mock_system.return_value = UNIX
        os.environ["XDG_CONFIG_HOME"] = "/home/testuser/.config"
        expected_filename = "/home/testuser/.config/instaloader/session-{}".format(USUARIO_TESTE)
        self.assertEqual(instaloader.get_default_session_filename(USUARIO_TESTE), expected_filename)

    def test_has_rigth_amount_valid_graphql_types(self):
        len_graphql_types_subject = len(Post.supported_graphql_types())

        self.assertEqual(len_graphql_types_subject, 3)
    
    def test_supported_graphql_types_contains_image_video_sidecar(self):
        expected_graphql_types = ["GraphImage", "GraphVideo", "GraphSidecar"]
        graphql_types = Post.supported_graphql_types()  
        
        has_all_graphql_types = all(
            graphql_type in expected_graphql_types
                for graphql_type in graphql_types)

        self.assertTrue(has_all_graphql_types)
    
    def test_default_user_agent_equals_mozilla(self):
        expected_user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 ' \
           '(KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
        
        user_agent_subject = instaloadercontext.default_user_agent()

        self.assertEqual(user_agent_subject, expected_user_agent)
    
    def test_too_long_media_id_should_raise_invalid_argument_exception(self):
        invalid_media_id = 10 ** 100

        self.assertRaises(InvalidArgumentException, lambda: Post.mediaid_to_shortcode(invalid_media_id))
    
    def test_none_media_id_should_raise_attribute_error(self):
        invalid_media_id = None

        self.assertRaises(AttributeError, lambda: Post.mediaid_to_shortcode(invalid_media_id))
    
    def test_negative_media_id_should_raise_invalid_argument_exception(self):
        invalid_media_id = -1

        self.assertRaises(OverflowError, lambda: Post.mediaid_to_shortcode(invalid_media_id))
    
    def test_valid_mediaid_to_shortcode(self):
        result = Post.mediaid_to_shortcode(1)

        self.assertEqual(result, 'B')
    
    def test_too_long_shortcode_should_raise_invalid_argument_exception(self):
        invalid_shortcode = "XXXXXXXXXXXX"

        self.assertRaises(InvalidArgumentException, lambda: Post.shortcode_to_mediaid(invalid_shortcode))

    def test_valid_shortcode_to_mediaid(self):
        result = Post.shortcode_to_mediaid("X")

        self.assertEqual(result, 23)

    def test_none_shortcode_to_mediaid_should_raise_type_error(self):
        self.assertRaises(TypeError, lambda: Post.shortcode_to_mediaid(None))
    

    # /////// Tests dinamics properties


    def test_local_date_with_date_key(self):
        print('test_local_date_with_date_key')
        with mock.patch.object(self.data_tests, 'util_datetime', return_value=datetime.now(timezone.utc)):
            post = Post(self.context, self.mockpost)
            expected_date = datetime.fromtimestamp(self.data_tests.timestamp, timezone.utc)
            self.assertEqual(post.date_local, expected_date)

    def test_local_date_without_date_key(self):
        print('test_local_date_without_date_key')
        copy_date = self.mockpost.copy()
        del copy_date['date']
        with mock.patch.object(self.data_tests, 'util_datetime', return_value=datetime.now(timezone.utc)):
            post = Post(self.context, self.mockpost)
            expected_date = datetime.fromtimestamp(self.data_tests.timestamp, timezone.utc)
            self.assertEqual(post.date_local, expected_date)

    def test_with_title_post(self):
        print('test_with_title_post')
        title = 'post da ufs'
        post = Post(self.context, self.mockpost)
        self.assertEqual(post.title, title)

    def test_without_title_post(self):
        print('test_without_title_post')
        title = None
        copymock = self.mockpost.copy()
        del copymock['title']
        post = Post(self.context, copymock)
        post._full_metadata_dict = {'teste': 'title'}
        self.assertEqual(post.title, title)

    def test_media_id(self):
        print('test_media_id')
        mediaid = 1234
        post = Post(self.context, self.mockpost)
        self.assertEqual(mediaid, post.mediaid)

    def test_shortcode_with_shortcode_key(self):
        print('test_shortcode_with_shortcode_key')
        shortcode = 'shortcode123'
        post = Post(self.context, self.mockpost)
        self.assertEqual(post.shortcode, shortcode)

    def test_shortcode_without_shortcode_key(self):
        print('test_shortcode_without_shortcode_key')
        shortcode = 'shortcode123'
        copymock = self.mockpost.copy()
        del copymock['shortcode']
        post = Post(self.context, copymock)
        self.assertEqual(post.shortcode, shortcode)


class TesteIntegracao(unittest.TestCase):

    def post_paging_test(self, iterator):
        previous_post = None
        for post in islice(iterator, PAGING_MAX_COUNT):
            print(post)
            if previous_post:
                self.assertTrue(post.date_utc < previous_post.date_utc)
            previous_post = post

    def setUp(self):
        self.dir = tempfile.mkdtemp()
        print("Testing in {}".format(self.dir))
        os.chdir(self.dir)
        self.L = instaloader.Instaloader(download_geotags=True,
                                         download_comments=True,
                                         save_metadata=True)
        self.L.context.raise_all_errors = True
        if ratecontroller is not None:
            # pylint:disable=protected-access
            ratecontroller._context = self.L.context
            self.L.context._rate_controller = ratecontroller

    def tearDown(self):
        # pylint:disable=global-statement,protected-access
        global ratecontroller
        ratecontroller = self.L.context._rate_controller
        self.L.close()
        os.chdir('/')
        print("Removing {}".format(self.dir))
        shutil.rmtree(self.dir)

    def test_profile_pic_download(self):
        self.L.download_profiles({self.L.check_profile_id(USUARIO_TESTE)}, posts=False, raise_errors=True)

    def test_public_profile_paging(self):
        self.post_paging_test(instaloader.Profile.from_username(self.L.context, USUARIO_TESTE).get_posts())

if __name__ == '__main__':

    unittest.main()