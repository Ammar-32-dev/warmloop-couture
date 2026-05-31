from .models import Category

def myapp_globals(request):
    """
    Global context processor injecting available categories for the storefront dropdown menu.
    """
    return {
        'global_categories': Category.objects.all(),
    }
