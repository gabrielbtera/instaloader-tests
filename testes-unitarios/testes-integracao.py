import unittest
from unittest import mock


from instaloader.instaloader import Instaloader
from instaloader.structures import Hashtag, Post

from .mockapi import mock_api



mockapi =  mock_api()

# execute python3 -m testes-unitarios.testes-integracaoz


class IntegrationTests(unittest.TestCase):
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

    
    

    




    


if __name__== '__main__':
    unittest.main()