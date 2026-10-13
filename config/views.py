def custom_403(request, exception=None):
     return render(request, 'blog/403.html', status=403)