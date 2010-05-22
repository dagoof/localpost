from web import form

val_name=form.regexp(r'^(\w)+$', 'Username can only consist of letters and numbers')
val_pass=form.regexp(r'.{3,20}$', 'Must be between 3 and 20 chars')
post_form=form.Form(
    form.Textbox('username', val_name, description='Username'),
    form.Password('password', val_pass, description='Password'),
)
