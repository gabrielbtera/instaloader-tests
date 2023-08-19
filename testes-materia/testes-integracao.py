import unittest
from unittest import mock
import instaloader
import tempfile
import os
import shutil

from itertools import islice

from instaloader.instaloader import Instaloader
from instaloader.structures import Hashtag, Post

from .mockapi import mock_api

PERFIL_PUBLICO = 'neymarjr'
ID_PERFIL_PUBLICO = 26669533
EMPTY_PROFILE_ID = 1928659031
EMPTY_PROFILE = "not_public"

USUARIO_TESTE = 'kaell_andrade'
UBER_USER = "uber"
WINDOS = 'Windows'
UNIX = 'Unix'
PAGING_MAX_COUNT = 10

ratecontroller = None

mockapi =  mock_api()

#python3 -m testes-materia.testes-integracao


class IntegrationTests(unittest.TestCase):
    # Testes gabriel
    context = mock.Mock(Instaloader())
    def test_media_is_downloadable_video(self):
        context = mock.Mock(Instaloader())
        post = Post(context.context, mockapi)
        videos = [False, True]
        self.assertEquals(videos, post.get_is_videos())
       
    
    def test_get_user_downloadable_profile(self):
        context = mock.Mock(Instaloader())
        post = Post(context.context, mockapi)
        self.assertEqual(post.owner_username, 'instagram' )
        self.assertEqual(post.owner_id, '25025320')
    

    def test_downloadable_caption(self):
        context = mock.Mock(Instaloader())
        post = Post(context.context, mockapi)
        self.assertEqual(post.caption, "comentario da materia de testes @professorGlauco #testesIntegracao #ufs")
        self.assertEquals(post.tagged_users, ["gabrielsilva"])
        self.assertEquals(post.caption_hashtags, ['testesintegracao', 'ufs'])
        self.assertEquals(post.caption_mentions, ['professorglauco'])


    def test_count_views_and_media_interations(self):
        context = mock.Mock(Instaloader())
        post = Post(context.context, mockapi)
        self.assertEqual(post.video_view_count, 3000)
        self.assertEqual(post.mediacount, 2)
        self.assertEqual(post.comments, 19690)


    # Teste micael
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        os.chdir(self.dir)
        self.L = instaloader.Instaloader(download_geotags=True,
                                         download_comments=True,
                                         save_metadata=True)
        self.L.context.raise_all_errors = True
        if ratecontroller is not None:
            ratecontroller._context = self.L.context
            self.L.context._rate_controller = ratecontroller

    
    def test_get_username_id_by_username_public(self):
        self.assertEqual(ID_PERFIL_PUBLICO,
                         instaloader.Profile.from_username(self.L.context, PERFIL_PUBLICO).userid)
    
    def test_get_username_by_name_empty(self):
        self.assertEqual(EMPTY_PROFILE_ID,
                         instaloader.Profile.from_username(self.L.context, EMPTY_PROFILE).userid)
    
    # teste wilson
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
        self.post_paging_test(instaloader.Profile.from_username(self.L.context, UBER_USER).get_posts())



if __name__== '__main__':
    unittest.main()