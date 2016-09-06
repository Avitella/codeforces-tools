import scipy.stats

def likes_vs_dislikes_rank(likes, dislikes):
    THRESHOLD = 0.95
    return scipy.stats.beta.ppf(THRESHOLD, likes + 1, dislikes + 1)
