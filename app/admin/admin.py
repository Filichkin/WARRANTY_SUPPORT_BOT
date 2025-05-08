from fastapi_admin.app import app
from fastapi_admin.resources import Model
from fastapi_admin.widgets import filters

from app.users.models import User


@app.register
class UserResource(Model):
    label = 'Users'
    model = User
    fields = [
        'id',
        'phone_number',
        'first_name',
        'last_name',
        'dealer_code',
        'email',
        'password'
    ]
    filters = [
        filters.Search(
            name='dealer_code',
            label='Dealer code',
            search_mode='contains',
            placeholder='Search by Dealer code',
        ),
        filters.Date(name='created_at', label='CreatedAt'),
    ]
