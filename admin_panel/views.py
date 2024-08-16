from django.http import HttpResponse


def welcome(request):
    return HttpResponse("""
        <h1>Welcome to Home Page</h1>
        <p>To log in, visit:
                    <a href="/admin/">http://127.0.0.1:8000/admin/</a></p>
    """)
