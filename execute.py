import praw
from praw.helpers import flatten_tree
import pickle


def extract_comments(comments_raw):
    _comments = [ [comment] + flatten_tree(comment.replies) for comment in comments_raw ]
    comments = []
    for obj in _comments:
        inner_comments = []
        for obj_item in obj:
            try:
                inner_comments.append({ 'body' : obj_item.body,
                                        'score' : obj_item.score
                                        })
            except AttributeError:
                pass
        comments.append(inner_comments)
    return comments

def get_posts(name='machinelearning', limit=5):
    # get subreddit
    subreddit = r.get_subreddit("machinelearning")
    # list of posts
    posts = []
    for post in subreddit.get_hot(limit=limit): # get from hot tag
        # create a post dict
        post = {'title' : post.title,
                'text' : post.selftext,
                'score' : post.score,
                'url' : post.url,
                'comments' : extract_comments(post.comments)
                }
        # add to list
        posts.append(post)
    return posts

def save_posts(posts, name='ml_test'):
    with open(name+'.pkl', 'wb') as f:
        pickle.dump(posts, f)
    print('>> Saved to {}'.format(name+'.pkl'))

def load_posts(filename):
    with open(filename, 'rb') as f:
        posts = pickle.load(f)
    return posts


if __name__ == '__main__':
    # set user agent
    user_agent = "TickFaw 0.2"
    # create reddit handle
    r = praw.Reddit(user_agent=user_agent)
    # get posts
    posts = get_posts(name='machinelearning', limit=10)
    # write to file
    save_posts(posts, name='ml_test')
