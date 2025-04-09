from flask import redirect, url_for, request, flash
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from myapp import bcrypt
from wtforms import PasswordField
from wtforms.validators import DataRequired
from flask_admin import AdminIndexView, expose


class MyAdminIndexView(AdminIndexView):
    """Custom admin index (dashboard) view.
    
    Only accessible to users with the 'admin' role. Unauthorized users are 
    redirected to the login page with a flash message when accessing the dashboard.
    """
    
    @expose('/')
    def index(self):
        if not self.is_accessible():
            return self.inaccessible_callback(name='index')
        return super().index()

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role.lower() == 'admin'

    def inaccessible_callback(self, name, **kwargs):
        flash('You need admin access to view the dashboard.', 'warning')
        return redirect(url_for('users.login', next=request.url))


class AdminModelView(ModelView):
    """Custom base class for all admin model views.
    
    Restricts access to authenticated users with the 'admin' role.
    Protects admin URLs like /admin/model-name/ from unauthorized access.
    If unauthorized, redirects the user to the login page.
    """

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role.lower() == 'admin'
    
    def inaccessible_callback(self, name, **kwargs):
        flash("You must be an admin to access this page.", "warning")
        return redirect(url_for('users.login', next=request.url))


class UserView(AdminModelView):
    """Admin view for managing User models.

    Inherits access control from AdminModelView to ensure only admin users
    can create, edit, delete, or export User records from the admin panel.
    """

    can_create = True
    can_edit = True
    can_delete = True
    can_export = True
    
    form_columns = ["username", "email", "password", "image_file", "role"]

    column_list = ['id', 'username', 'email', 'password', 'image_file', 'role']
    column_labels = {'id': 'Id', 'username': 'Username', 'email': 'Email Address',
                      'password': 'Password', 'image_file': 'Image File', 'role': 'Role'}
    
    column_filters = ['id', 'username', 'email', 'image_file', 'role']
    column_editable_list = ['username', 'email', 'image_file', 'role']
    column_searchable_list = ['username', 'email', 'role']
    column_default_sort = 'id'  # use tuple to control ascending descending order. only string=>ascending, ('id', True) True=>decending order 
    
    column_formatters = dict(password=lambda v, c, m, p: m.password[:5] + '***********' + m.password[-5:])

    # Override the on_model_change method to hash the password
    def on_model_change(self, form, model, is_created):
        model.password = bcrypt.generate_password_hash(model.password).decode('utf-8')

    form_extra_fields = {
        'password': PasswordField('Password', validators=[DataRequired()])
    }


class PostView(AdminModelView):
    """Admin view for managing Post models.

    Extends AdminModelView to restrict access to admin users only.
    Allows creating, editing, deleting, and exporting post records
    within the admin interface.
    """
       
    can_create = True
    can_delete = True
    can_edit = True
    page_size = 10  # the number of entries to display on the list view
    can_export = True   # export all rows by default. export_max_rows to set rows allowed
    

    column_list = ["title", "date_posted", "content", "author"]
    column_labels = {'title': 'Title', 'date_posted': 'Date Posted', 'content': 'Content', 'author': 'Author'}
    column_filters = ('title', 'author', 'date_posted')
    column_searchable_list = ('title', 'author.username', 'date_posted', 'content')
    column_default_sort = ('id', True)   # tuple to control ascending descending order. ('id', True) True=>decending order 

    def _format_author(view, context, model, name): # or use v,c,m,p as argument
        return f"id: {model.author.id} ({model.author.username})"

    column_formatters = {"author": _format_author, "content" : lambda v, c, m, p: m.content[:500] + '......'}   #  truncates the content column to 500 characters and adds an ellipsis
    
    form_columns = ["title", "date_posted", "content", "user_id"]

