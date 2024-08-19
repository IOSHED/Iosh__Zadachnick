
def user_directory_path(user, filename):
    # MEDIA_ROOT/user_<id>/<filename>
    return 'files/user_{0}/{1}'.format(user.email, filename)
